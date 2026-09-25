-- Queries used to build the ranked table and writeup.
-- Run against data/water_electricity_snapshot.db, e.g.:
--   sqlite3 data/water_electricity_snapshot.db < sql/queries.sql

-- 1. Final ranked scorecard
SELECT rank, company, water_efficiency, disclosure_quality, trend_direction, total
FROM scores
ORDER BY rank;

-- 2. Why each company got its disclosure quality and trend scores
SELECT company, disclosure_quality, disclosure_quality_note,
       trend_direction, trend_direction_note
FROM scores
ORDER BY rank;

-- 3. Water withdrawn, consumed, and WUE per company
SELECT
    company,
    MAX(CASE WHEN metric_name = 'water_withdrawal' THEN value END)   AS water_withdrawn,
    MAX(CASE WHEN metric_name = 'water_withdrawal' THEN unit END)    AS withdrawn_unit,
    MAX(CASE WHEN metric_name = 'water_consumption' THEN value END)  AS water_consumed,
    MAX(CASE WHEN metric_name = 'water_consumption' THEN unit END)   AS consumed_unit,
    MAX(CASE WHEN metric_name = 'wue' THEN value END)                AS wue_l_per_kwh,
    MAX(CASE WHEN metric_name = 'water_withdrawal' THEN year
             WHEN metric_name = 'water_consumption' THEN year END)   AS year
FROM metrics
WHERE metric_name IN ('water_withdrawal', 'water_consumption', 'wue')
GROUP BY company;

-- 4. Electricity use and renewable matching per company
SELECT
    company,
    MAX(CASE WHEN metric_name = 'electricity_consumption' THEN value END) AS electricity_twh,
    MAX(CASE WHEN metric_name = 'renewable_match_pct' THEN value END)     AS renewable_match_pct
FROM metrics
WHERE metric_name IN ('electricity_consumption', 'renewable_match_pct')
GROUP BY company;

-- 5. Indirect water disclosure (water used generating purchased electricity)
SELECT company, value AS discloses_indirect_water, note, source_url
FROM metrics
WHERE metric_name = 'indirect_water_disclosed'
ORDER BY value DESC;

-- 6. Published methodology, by company
SELECT company, value AS methodology_published, note, source_url
FROM metrics
WHERE metric_name = 'methodology_published'
ORDER BY value DESC;

-- 7. AI-specific water/energy metrics (expected: mostly none)
SELECT company, value AS has_ai_specific_metric, note
FROM metrics
WHERE metric_name = 'ai_specific_metric'
ORDER BY value DESC;

-- 8. Water-positive claims
SELECT company, value AS claims_water_positive, note
FROM metrics
WHERE metric_name = 'water_positive_claim'
ORDER BY value DESC;

-- 9. Every metric a company did NOT disclose (the disclosure gaps)
SELECT company, metric_name, unit, note
FROM metrics
WHERE disclosed = 'no'
ORDER BY company, metric_name;

-- 10. Full scorecard joined with its underlying WUE, for a sanity check
--     that water efficiency scores track the raw numbers
SELECT s.rank, s.company, s.water_efficiency, m.value AS wue_l_per_kwh
FROM scores s
LEFT JOIN metrics m ON m.company = s.company AND m.metric_name = 'wue'
ORDER BY s.rank;
