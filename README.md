# ai-hyperscaler-water-electricity-snapshot

A scored comparison of how honest Google, Microsoft, Amazon, Meta, and OpenAI are about the water and electricity their AI data centers use. Each company is rated 1 to 5 on water efficiency, disclosure quality, and year-over-year trend, using only their own published sustainability reports, no paid ESG data. The raw numbers live in a SQLite database, the scoring logic is a plain Python script with its reasoning written inline, and the findings are written up in `WRITEUP.md` and as a formatted page in `data/report.html`.

See `WRITEUP.md` for the ranked table and full writeup, and `sql/queries.sql` for the queries used to pull the numbers.
