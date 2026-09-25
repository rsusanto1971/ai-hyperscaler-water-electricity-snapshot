# AI Hyperscaler Water and Electricity Snapshot

A scored comparison of Google, Microsoft, Amazon (AWS), Meta, and OpenAI on data center water use, electricity use, and how honest each company's own disclosures are about it. Compiled September 2026, using each company's own most recent sustainability report. No paid ESG data providers were used.

## Ranked scorecard

| Rank | Company | Water Efficiency | Disclosure Quality | Trend Direction | Total |
|---|---|---|---|---|---|
| 1 | Amazon (AWS) | 5 | 4 | 4 | 13 |
| 2 | Meta | 4 | 5 | 3 | 12 |
| 3 | Microsoft | 3 | 3 | 5 | 11 |
| 4 | Google | 2 | 3 | 2 | 7 |
| 5 | OpenAI | 1 | 1 | 1 | 3 |

Each category is scored 1 to 5 and weighted equally. Total is out of 15.

## Water and electricity figures

| Company | Year | Water Withdrawn | Water Consumed | WUE (L/kWh) | Electricity (TWh) | Renewable Match (%) |
|---|---|---|---|---|---|---|
| Amazon (AWS) | 2025 | 2.5B gal | not disclosed | 0.12 | not disclosed | 100 |
| Meta | 2024 | 3,881,000 m3 | 3,123,000 m3 | 0.18 | 18.4 | 100 |
| Microsoft | FY2025 | not disclosed | not disclosed | 0.27 | not disclosed | 100 |
| Google | 2025 | not disclosed | 10.9B gal | not disclosed | 42.0 | 100 |
| OpenAI | n/a | not disclosed | 0.000085 gal/query | n/a | not disclosed | not disclosed |

Notes:
- Each company reports on its own fiscal or calendar year. Google and Amazon report calendar 2025 (published mid-2026). Microsoft reports fiscal year 2025, ended June 2025, published June 2026. Meta reports calendar 2024, published September 2025, its most recent report so far. Years are not aligned across companies because the companies do not align them either.
- Microsoft says it replenished more than 14.2 million cubic meters of water in FY2025, more than it withdrew, but does not publish the withdrawal total itself.
- OpenAI's figure is a single unaudited number from a founder's personal blog post, not a company disclosure with a defined boundary or year. It is included for completeness, not as a comparable metric.
- Meta is the only company in this set that also discloses indirect water intensity from purchased electricity: 3.92 L/kWh for 2024, up from 3.62 in 2023.
- Google separately publishes a per-prompt figure for its Gemini Apps: 0.24 Wh energy and 0.26 mL water per median text prompt (May 2025 data). That number comes from a technical blog post, not the audited environmental report, and is the only metric in this set tied to an AI workload rather than the data center fleet as a whole.

## Scoring rubric

**Water efficiency (weight: 1/3)** is based on Water Usage Effectiveness (WUE, in L/kWh) where a company discloses it. A company with no fleet-wide WUE cannot be verified as efficient, whatever else it claims, and is capped low regardless of its other numbers.

**Disclosure quality (weight: 1/3)** looks at whether the company publishes a named methodology, gets third-party review, and, most importantly, whether it accounts for indirect water: the water used by power plants to generate the electricity these companies buy, not just on-site cooling.

**Trend direction (weight: 1/3)** looks at whether usage or intensity is improving or worsening year over year, and whether that direction, good or bad, is reported plainly rather than buried or omitted.

Disclosure quality and trend direction involve judgment calls that cannot be reduced to a single number pulled from a database. The reasoning behind every one of those scores is written out in `scripts/scoring.py` and stored alongside the scores in the database, so it can be checked.

Two patterns held across all five companies. First, none publish a verified, methodology-backed water or energy figure tied to a specific AI workload, query, or model. Google's per-prompt Gemini figure comes closest, and even that is a separate blog disclosure, not part of its audited report. Second, only Meta quantifies indirect water. Google, Microsoft, and Amazon all report on-site water only. Amazon at least acknowledges the gap in writing; Google and Microsoft do not address it at all.

"Renewable matched" in the table above means annual, market-based matching: purchased renewable energy contracts equal in volume to a year of consumption. It is not a real-time, hour-by-hour match to the actual electricity each company draws off the grid.

## The OpenAI gap

OpenAI is not comparable to the other four companies in this table, and that gap is the finding, not a footnote. Google, Microsoft, Amazon, and Meta each publish an annual sustainability report with a defined reporting boundary, a named methodology, and in most cases outside accountant review. OpenAI publishes none of this. Its only public figure, roughly 0.000085 gallons and 0.34 watt-hours per ChatGPT query, comes from a June 2025 personal blog post by Sam Altman, not a company report. OpenAI has never defined what an "average query" is, never named which model the estimate covers, and never released a methodology behind it. In September 2026, Altman made a second public claim on a podcast, that 38,000 ChatGPT queries use the same water as growing one California almond, which PolitiFact rated "Mostly False" within days. A company running some of the largest AI compute buildouts in the world, including the Stargate data center program, has disclosed less about its resource use than any traditional cloud provider discloses about a single one of its buildings.

## What we checked against the original starting numbers

| Company | Metric | Starting Figure | Verified Figure |
|---|---|---|---|
| Google | Water consumed 2025, billion gal | 10.9 | 10.9 |
| Amazon | Water withdrawn 2025, billion gal | 2.5 | 2.5 |
| Amazon | WUE, L/kWh | 0.12 | 0.12 |
| Microsoft | WUE, L/kWh | 0.046 | 0.27 |
| Meta | Water consumed 2024, m3 | 3,123,000 | 3,123,000 |
| Meta | Indirect water intensity, L/kWh | 3.92 | 3.92 |
| OpenAI | Water per query, gal | 0.000085 | 0.000085 |

The Microsoft WUE figure was the one correction. 0.046 L/kWh traces back to a third-party analytics index, not to anything Microsoft itself has published. Microsoft's own disclosed figure, in its FY2025 Environmental Sustainability Report, is 0.27 L/kWh. Its water-positive claim for FY2025 is accurate as originally given.

## Sources

- Google: 2026 Environmental Report (covers 2025), sustainability.google
- Microsoft: 2026 Environmental Sustainability Report (covers FY2025), microsoft.com
- Amazon: 2025 Amazon Sustainability Report and Water Positive Methodology, aboutamazon.com
- Meta: 2025 Sustainability Report and Environmental Data Index (covers FY2024), sustainability.atmeta.com
- OpenAI: "The Gentle Singularity," blog.samaltman.com, June 2025

## Files in this repo

- `data/water_electricity_snapshot.db` - the SQLite database (metrics and scores tables)
- `sql/queries.sql` - the queries used to pull every number in this writeup
- `scripts/build_database.py` - loads the raw, sourced metrics into the database
- `scripts/scoring.py` - applies the rubric above and writes the scores table, with the reasoning for each judgment-based score written inline
- `data/report.html` - the published, formatted version of this writeup
