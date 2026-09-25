"""
Populates the raw metrics table from company sustainability disclosures.

Run this first, then run scripts/scoring.py to add the scores table.
Every row traces back to a source_url. Where a company does not disclose
a figure, value is NULL and disclosed = 'no', rather than guessing.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "water_electricity_snapshot.db")
DB_PATH = os.path.abspath(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS metrics")
cur.execute("""
CREATE TABLE metrics (
    company TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    value REAL,
    unit TEXT,
    year INTEGER,
    source_url TEXT,
    disclosed TEXT CHECK(disclosed IN ('yes','no')) NOT NULL,
    note TEXT
)
""")

GOOGLE_SRC = "https://sustainability.google/google-2026-environmental-report/"
MSFT_SRC = "https://www.microsoft.com/en-us/corporate-responsibility/sustainability/report/"
AMZN_SRC = "https://sustainability.aboutamazon.com/2025-amazon-sustainability-report.pdf"
META_SRC = "https://sustainability.atmeta.com/2025-sustainability-report/"
OPENAI_SRC = "https://blog.samaltman.com/the-gentle-singularity"

rows = [
    # --- Google (FY2025, published June 2026) ---
    ("Google", "water_consumption", 10.9e9, "gallons", 2025, GOOGLE_SRC, "yes", "Total operational consumption (data centers + offices), up 34% YoY"),
    ("Google", "water_withdrawal", None, "gallons", 2025, GOOGLE_SRC, "no", "Not confirmed for FY2025; FY2024 figure was 7.8B gallons"),
    ("Google", "wue", None, "L/kWh", 2025, GOOGLE_SRC, "no", "Google does not publish a fleet-wide WUE"),
    ("Google", "indirect_water_disclosed", 0, "boolean", 2025, GOOGLE_SRC, "yes", "No quantified indirect/electricity-generation water disclosure"),
    ("Google", "methodology_published", 1, "boolean", 2025, GOOGLE_SRC, "yes", "Third-party limited assurance letter on select GHG/energy/water metrics"),
    ("Google", "ai_specific_metric", 1, "boolean", 2025, "https://cloud.google.com/blog/products/infrastructure/measuring-the-environmental-impact-of-ai-inference", "yes", "0.24 Wh energy / 0.26 mL water per median Gemini Apps text prompt (May 2025)"),
    ("Google", "electricity_consumption", 42.0, "TWh", 2025, GOOGLE_SRC, "yes", "Up 37% YoY"),
    ("Google", "renewable_match_pct", 100.0, "percent", 2025, GOOGLE_SRC, "yes", "Annual renewable matching, 9th consecutive year; 24/7 CFE was 66% for FY2024"),
    ("Google", "water_positive_claim", 0, "boolean", 2025, GOOGLE_SRC, "yes", "No water-positive claim; targets 120% replenishment by 2030 (78% achieved in 2025)"),

    # --- Microsoft (FY25, published June 2026) ---
    ("Microsoft", "water_withdrawal", None, "m3", 2025, MSFT_SRC, "no", "Absolute figure not confirmed; Microsoft states it replenished more than it withdrew (14.2M m3 replenished)"),
    ("Microsoft", "wue", 0.27, "L/kWh", 2025, MSFT_SRC, "yes", "Fleet-wide average, down from 2.3 L/kWh in the early 2000s"),
    ("Microsoft", "indirect_water_disclosed", 0, "boolean", 2025, "https://www.latitudemedia.com/news/data-centers-hidden-water-footprint-is-linked-to-the-grid/", "yes", "Not disclosed"),
    ("Microsoft", "methodology_published", 1, "boolean", 2025, MSFT_SRC, "yes", "Deloitte & Touche limited assurance review; methodology changed from direct measurement to modeled estimates, which weakens YoY comparability"),
    ("Microsoft", "ai_specific_metric", 0, "boolean", 2025, MSFT_SRC, "yes", "Not disclosed"),
    ("Microsoft", "electricity_consumption", None, "TWh", 2025, MSFT_SRC, "no", "Absolute figure not found; 100% of FY25 electricity matched with renewables via 400+ PPAs"),
    ("Microsoft", "renewable_match_pct", 100.0, "percent", 2025, MSFT_SRC, "yes", "Market-based matching, FY25"),
    ("Microsoft", "water_positive_claim", 1, "boolean", 2025, MSFT_SRC, "yes", "Claims water positive achieved in FY25, five years ahead of its 2030 target"),

    # --- Amazon / AWS (2025, published June 2026) ---
    ("Amazon", "water_withdrawal", 2.5e9, "gallons", 2025, AMZN_SRC, "yes", "First-ever absolute company-wide disclosure"),
    ("Amazon", "wue", 0.12, "L/kWh", 2025, AMZN_SRC, "yes", "Down 20% vs 2024, down 52% since 2021; Amazon cites industry average of 0.84 L/kWh"),
    ("Amazon", "indirect_water_disclosed", 0, "boolean", 2025, "https://sustainability.aboutamazon.com/water-positive-methodology.pdf", "yes", "Acknowledged qualitatively in narrative text but not quantified"),
    ("Amazon", "methodology_published", 1, "boolean", 2025, "https://sustainability.aboutamazon.com/water-positive-methodology.pdf", "yes", "Published Water Positive Methodology; third-party assurance and project-level audits"),
    ("Amazon", "ai_specific_metric", 0, "boolean", 2025, AMZN_SRC, "yes", "Not disclosed"),
    ("Amazon", "electricity_consumption", None, "TWh", 2025, AMZN_SRC, "no", "Absolute figure not disclosed; PUE of 1.14 reported instead"),
    ("Amazon", "renewable_match_pct", 100.0, "percent", 2025, AMZN_SRC, "yes", "Third consecutive year of 100% matching; 42 GW carbon-free portfolio"),
    ("Amazon", "water_positive_claim", 0, "boolean", 2025, AMZN_SRC, "yes", "Not yet claimed; more than halfway to its 2030 water-positive goal per its own methodology"),

    # --- Meta (FY2024, published Sept 2025) ---
    ("Meta", "water_withdrawal", 3881000, "m3", 2024, META_SRC, "yes", "Up ~7% YoY"),
    ("Meta", "water_consumption", 3123000, "m3", 2024, META_SRC, "yes", "Net consumption figure"),
    ("Meta", "wue", 0.18, "L/kWh", 2024, META_SRC, "yes", "Improved from 0.20 L/kWh in FY2023"),
    ("Meta", "indirect_water_disclosed", 1, "boolean", 2024, META_SRC, "yes", "Only hyperscaler in this set quantifying indirect water from purchased electricity"),
    ("Meta", "indirect_water_intensity", 3.92, "L/kWh", 2024, META_SRC, "yes", "Up from 3.62 L/kWh in FY2023; modeled estimate using regional grid water-intensity factors"),
    ("Meta", "methodology_published", 1, "boolean", 2024, "https://sustainability.atmeta.com/asset/2023-environmental-metrics-methodology/", "yes", "Published Environmental Metrics Methodology; EY limited-assurance review under AT-C 105/210"),
    ("Meta", "ai_specific_metric", 0, "boolean", 2024, META_SRC, "yes", "Not disclosed"),
    ("Meta", "electricity_consumption", 18.4, "TWh", 2024, META_SRC, "yes", "Up from 15.3 TWh in FY2023"),
    ("Meta", "renewable_match_pct", 100.0, "percent", 2024, META_SRC, "yes", "Market-based matching (RECs/PPAs) since 2020, not a physical hourly match"),
    ("Meta", "water_positive_claim", 0, "boolean", 2024, META_SRC, "yes", "No water-positive claim made"),

    # --- OpenAI (no formal report) ---
    ("OpenAI", "water_per_query", 0.000085, "gallons/query", 2025, OPENAI_SRC, "yes", "Sam Altman blog post 'The Gentle Singularity', June 10 2025; single unaudited figure, no defined 'average query'"),
    ("OpenAI", "energy_per_query", 0.34, "Wh/query", 2025, OPENAI_SRC, "yes", "Same source as water-per-query figure"),
    ("OpenAI", "wue", None, "L/kWh", None, OPENAI_SRC, "no", "Not applicable; OpenAI does not operate disclosed data center fleet metrics"),
    ("OpenAI", "indirect_water_disclosed", 0, "boolean", None, OPENAI_SRC, "yes", "Not disclosed"),
    ("OpenAI", "methodology_published", 0, "boolean", None, OPENAI_SRC, "yes", "No methodology, no defined average query, no named model(s)"),
    ("OpenAI", "ai_specific_metric", 0, "boolean", None, OPENAI_SRC, "yes", "The one public number has no supporting methodology, so it cannot function as a comparable metric"),
    ("OpenAI", "electricity_consumption", None, "TWh", None, OPENAI_SRC, "no", "Not disclosed"),
    ("OpenAI", "water_positive_claim", 0, "boolean", None, OPENAI_SRC, "yes", "No claim made"),
]

cur.executemany(
    "INSERT INTO metrics (company, metric_name, value, unit, year, source_url, disclosed, note) VALUES (?,?,?,?,?,?,?,?)",
    rows,
)

conn.commit()
cur.execute("SELECT COUNT(*) FROM metrics")
print(f"metrics table populated: {cur.fetchone()[0]} rows -> {DB_PATH}")
conn.close()
