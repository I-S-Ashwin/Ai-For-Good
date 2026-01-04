-- ============================================================================
-- SAFEHAVEN AI - SNOWFLAKE NATIVE APP SETUP
-- PART 1: DATABASE ARCHITECTURE
-- ============================================================================

-- 1. SETUP DATABASE & SCHEMA
CREATE DATABASE IF NOT EXISTS SAFEHAVEN_DB;
USE DATABASE SAFEHAVEN_DB;

CREATE SCHEMA IF NOT EXISTS APP;
USE SCHEMA APP;

-- 2. CREATE INTERNAL STAGE FOR MULTIMODAL ASSETS
-- This stage will store images and audio uploaded from the Streamlit UI.
-- Directory table enabled for easy querying and file listing.
CREATE OR REPLACE STAGE INSPECTION_ASSETS
    DIRECTORY = (ENABLE = TRUE)
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- 3. VECTOR STORE FOR BUILDING CODES (RAG)
-- Stores chunks of building codes for the Legal Shield features.
CREATE OR REPLACE TABLE BUILDING_CODES_CHUNKS (
    CHUNK_ID STRING DEFAULT UUID_STRING(),
    SECTION_TITLE STRING,
    CHUNK_TEXT STRING, -- The actual code text
    METADATA VARIANT   -- Additional info like source, year
);

-- Mock Data Insertion (IBC Section 101 - Structural Safety)
INSERT INTO BUILDING_CODES_CHUNKS (SECTION_TITLE, CHUNK_TEXT, METADATA) VALUES
('IBC Section 101.5', 'Structural Integrity: All modifications to load-bearing walls must be certified by a licensed structural engineer. Unpermitted removal of studs poses a collapse risk.', {'source': 'IBC 2024', 'category': 'Structural'}),
('NEC Article 210', 'Electrical Wiring: In kitchen wall receptacles, GFCI protection is required for all outlets that serve partial countertop surfaces.', {'source': 'NEC 2023', 'category': 'Electrical'}),
('IRC Section R302', 'Fire-Resistant Construction: Garage-dwelling separation requires not less than 1/2-inch gypsum board applied to the garage side.', {'source': 'IRC 2021', 'category': 'Fire Safety'});

-- 4. INTELLIGENT PIPELINE (DYNAMIC TABLE)
-- Triggers every 1 minute to process new images found in the directory table.
-- extracting defects, severity, visual description, and fixes using Llama-3.2-90b-vision.

CREATE OR REPLACE DYNAMIC TABLE DT_INSPECTION_ANALYSIS
    TARGET_LAG = '1 minute'
    WAREHOUSE = 'COMPUTE_WH' -- Assumes default warehouse exists
AS
SELECT 
    RELATIVE_PATH AS FILE_NAME,
    GET_PRESIGNED_URL(@INSPECTION_ASSETS, RELATIVE_PATH) AS FILE_URL,
    -- Call Snowflake Cortex AI (Llama 3.2 Vision)
    -- We prompt the model to return a strict JSON structure.
    SNOWFLAKE.CORTEX.AI_COMPLETE(
        'llama-3.2-90b-vision', 
        {
            'image': FILE_URL,
            'prompt': 'Analyze this home inspection image. Identify any defects. Return ONLY a JSON object with this structure: {"defect": "name of defect", "severity": 0-100, "visual_description": "detailed description", "recommended_fix": "how to fix"}. Do not add any markdown formatting.'
        }
    ) AS AI_ANALYSIS_RAW,
    -- Metadata from the file (e.g., upload time)
    LAST_MODIFIED
FROM DIRECTORY(@INSPECTION_ASSETS)
WHERE RELATIVE_PATH LIKE '%.jpg' OR RELATIVE_PATH LIKE '%.png' OR RELATIVE_PATH LIKE '%.jpeg';

-- Add a comment to describe the table
COMMENT ON TABLE DT_INSPECTION_ANALYSIS IS 'Automated inspection analysis pipeline using Snowflake Cortex Vision.';
