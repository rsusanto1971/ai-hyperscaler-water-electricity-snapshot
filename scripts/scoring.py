"""
Scores each company 1-5 in three equally weighted categories and writes
the scores table. Run scripts/build_database.py first.

Water efficiency is derived automatically from disclosed WUE (Water Usage
Effectiveness, L/kWh) values pulled straight out of the metrics table:
lower WUE ranks higher, and a company with no disclosed fleet-wide WUE
cannot be verified as efficient no matter what else it publishes, so it
is capped at 2.

Disclosure quality and trend direction cannot be reduced to a single
number pulled from the database (they depend on things like "did they
name a methodology" and "was a worsening number reported plainly or
buried"), so those two are scored by hand below, with the reasoning
written out next to each score. Anyone can check that reasoning against
the sourced rows in the metrics table.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "water_electricity_snapshot.db")
DB_PATH = os.path.abspath(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# --- 1. Water efficiency: derived from disclosed WUE ---------------------
cur.execute("SELECT company, value FROM metrics WHERE metric_name = 'wue' AND disclosed = 'yes'")
wue_by_company = dict(cur.fetchall())
# Lower L/kWh is better. Sorted ascending = best first.
ranked_by_wue = sorted(wue_by_company.items(), key=lambda kv: kv[1])

water_efficiency_scores = {}
# 5 companies total; best disclosed WUE gets 5, next 4, etc. No disclosed
# WUE at all (Google, OpenAI) is capped at 2: you cannot verify efficiency
# you cannot measure, whatever else the company claims.
efficiency_scale = [5, 4, 3]
for (company, _), score in zip(ranked_by_wue, efficiency_scale):
    water_efficiency_scores[company] = score
for company in ["Google", "Microsoft", "Amazon", "Meta", "OpenAI"]:
    water_efficiency_scores.setdefault(company, 2 if company != "OpenAI" else 1)

# OpenAI's 0.000085 gal/query is not a WUE and is not audited, so it does
# not count as a verifiable efficiency figure at all.
water_efficiency_scores["OpenAI"] = 1

# --- 2. Disclosure quality: manual, reasoning below -----------------------
disclosure_quality_scores = {
    "Meta": (5, "Only company quantifying indirect water from purchased "
                "electricity (3.92 L/kWh); publishes a named methodology "
                "doc; EY limited-assurance review."),
    "Amazon": (4, "Published Water Positive Methodology with third-party "
                  "assurance and project-level audits; acknowledges the "
                  "indirect-water gap in writing but does not quantify it."),
    "Microsoft": (3, "Deloitte limited assurance review exists, but "
                     "Microsoft changed its water methodology from direct "
                     "measurement to modeled estimates, which weakens "
                     "year-over-year comparability; no indirect water "
                     "disclosure."),
    "Google": (3, "Third-party assurance letter on select metrics; GHG "
                  "Protocol-aligned; but no fleet-wide WUE, no indirect "
                  "water disclosure, and its headline water figure mixes "
                  "data centers with offices."),
    "OpenAI": (1, "No annual report, no named methodology, no defined "
                  "'average query', no model named. A single blog-post "
                  "number is not a disclosure system."),
}

# --- 3. Trend direction: manual, reasoning below --------------------------
trend_direction_scores = {
    "Microsoft": (5, "Claims water positive achieved in FY2025, five years "
                     "ahead of its 2030 target, and reports it plainly."),
    "Amazon": (4, "WUE down 20% year over year and down 52% since 2021; "
                  "trend is clearly improving and clearly reported."),
    "Meta": (3, "Mixed: WUE improved slightly (0.20 to 0.18 L/kWh) but "
                "indirect water intensity worsened (3.62 to 3.92 L/kWh) "
                "and withdrawal rose 7%. Reported candidly either way, "
                "including the worsening number."),
    "Google": (2, "Water consumption up 34% year over year, more than "
                  "double 2021 levels. Reported transparently, but the "
                  "underlying trend is clearly worsening."),
    "OpenAI": (1, "No year-over-year data exists at all, so trend cannot "
                  "be assessed in either direction."),
}

companies = ["Google", "Microsoft", "Amazon", "Meta", "OpenAI"]
totals = {}
for company in companies:
    we = water_efficiency_scores[company]
    dq = disclosure_quality_scores[company][0]
    td = trend_direction_scores[company][0]
    totals[company] = we + dq + td

ranked = sorted(companies, key=lambda c: totals[c], reverse=True)

cur.execute("DROP TABLE IF EXISTS scores")
cur.execute("""
CREATE TABLE scores (
    company TEXT NOT NULL,
    water_efficiency INTEGER NOT NULL,
    disclosure_quality INTEGER NOT NULL,
    trend_direction INTEGER NOT NULL,
    total INTEGER NOT NULL,
    rank INTEGER NOT NULL,
    disclosure_quality_note TEXT,
    trend_direction_note TEXT
)
""")

for rank, company in enumerate(ranked, start=1):
    cur.execute(
        """INSERT INTO scores
           (company, water_efficiency, disclosure_quality, trend_direction,
            total, rank, disclosure_quality_note, trend_direction_note)
           VALUES (?,?,?,?,?,?,?,?)""",
        (
            company,
            water_efficiency_scores[company],
            disclosure_quality_scores[company][0],
            trend_direction_scores[company][0],
            totals[company],
            rank,
            disclosure_quality_scores[company][1],
            trend_direction_scores[company][1],
        ),
    )

conn.commit()

print(f"{'Rank':<5}{'Company':<12}{'WaterEff':<10}{'Disclosure':<12}{'Trend':<8}{'Total'}")
for rank, company in enumerate(ranked, start=1):
    print(f"{rank:<5}{company:<12}{water_efficiency_scores[company]:<10}"
          f"{disclosure_quality_scores[company][0]:<12}"
          f"{trend_direction_scores[company][0]:<8}{totals[company]}")

conn.close()
