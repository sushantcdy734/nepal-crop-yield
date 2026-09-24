-- ============================================================
-- Nepal Agriculture Analysis — SQL Queries
-- Author: Sushant Chaudhary
-- Database: data/nepal_agriculture.db
-- ============================================================

-- Query 1: Average yield for each crop across all years
-- Answer: which crop has the highest average yield?
SELECT
    crop,
    ROUND(AVG(yield_kg_per_ha), 1) AS avg_yield,
    ROUND(MIN(yield_kg_per_ha), 1) AS min_yield,
    ROUND(MAX(yield_kg_per_ha), 1) AS max_yield,
    COUNT(*) AS years_of_data
FROM crop_yields
GROUP BY crop
ORDER BY avg_yield DESC;


-- Query 2: Top 5 years with highest monsoon rainfall
-- Answer: which years were the wettest?
SELECT
    year,
    ROUND(monsoon_rainfall, 0) AS monsoon_mm,
    ROUND(total_rainfall, 0) AS total_mm
FROM rainfall_yearly
ORDER BY monsoon_rainfall DESC
LIMIT 5;


-- Query 3: Join crops with rainfall — average yield by rainfall bucket
-- Answer: does higher rainfall correlate with higher yield?
SELECT
    crop,
    CASE
        WHEN monsoon_rainfall < 90000 THEN 'Low (<90k)'
        WHEN monsoon_rainfall < 110000 THEN 'Medium (90k-110k)'
        ELSE 'High (>110k)'
    END AS rainfall_bucket,
    COUNT(*) AS num_years,
    ROUND(AVG(yield_kg_per_ha), 1) AS avg_yield
FROM crop_yields c
JOIN rainfall_yearly r ON c.year = r.year
GROUP BY crop, rainfall_bucket
ORDER BY crop, rainfall_bucket;


-- Query 4: Year-over-year yield change for Maize
-- Answer: which years saw the biggest jumps/drops in maize yield?
SELECT
    year,
    ROUND(yield_kg_per_ha, 1) AS yield,
    ROUND(yield_kg_per_ha - LAG(yield_kg_per_ha) OVER (ORDER BY year), 1) AS yoy_change
FROM crop_yields
WHERE crop = 'Maize (corn)'
ORDER BY year;


-- Query 5: Best year for each crop (highest yield)
-- Answer: what was the single best year per crop?
WITH ranked AS (
    SELECT
        crop,
        year,
        yield_kg_per_ha,
        ROW_NUMBER() OVER (PARTITION BY crop ORDER BY yield_kg_per_ha DESC) AS rn
    FROM crop_yields
)
SELECT crop, year, ROUND(yield_kg_per_ha, 1) AS best_yield
FROM ranked
WHERE rn = 1
ORDER BY best_yield DESC;