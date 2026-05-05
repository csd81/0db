-- ──────────────────────────────────────────────────────────────────────────────
-- seed_capacity.sql
--
-- Batch-update EuropeRoad.Capacity based on CrossingType.
-- Run once against EuropeGraph after importing the road network.
--
-- CrossingType values:
--   0 = land road / highway     → 1000 units  (trucks/hour equivalent)
--   1 = ferry crossing          →  200 units  (vessel capacity)
--   2 = ocean corridor          →  100 units  (bottleneck shipping lane)
-- ──────────────────────────────────────────────────────────────────────────────

USE EuropeGraph;
GO

-- 1. Ensure the Capacity column exists (idempotent)
IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('dbo.EuropeRoad') AND name = 'Capacity'
)
BEGIN
    ALTER TABLE dbo.EuropeRoad
        ADD Capacity INT NULL DEFAULT 100;
    PRINT 'Capacity column added.';
END
ELSE
BEGIN
    PRINT 'Capacity column already exists — skipping ALTER.';
END
GO

-- 2. Set capacity by road type
UPDATE dbo.EuropeRoad
SET Capacity = CASE
    WHEN CrossingType = 2 THEN 100    -- Ocean corridor (bottleneck)
    WHEN CrossingType = 1 THEN 200    -- Ferry crossing
    ELSE                       1000   -- Land highway
END;

PRINT CONCAT('Updated ', @@ROWCOUNT, ' road segments.');
GO

-- 3. Verify distribution
SELECT
    CrossingType,
    CASE CrossingType
        WHEN 0 THEN 'Land / Highway'
        WHEN 1 THEN 'Ferry'
        WHEN 2 THEN 'Ocean'
        ELSE        'Unknown'
    END                           AS RoadType,
    Capacity,
    COUNT(*)                      AS NumSegments
FROM dbo.EuropeRoad
GROUP BY CrossingType, Capacity
ORDER BY CrossingType;
GO
