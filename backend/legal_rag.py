# ============================================================================
# SAFEHAVEN AI - BACKEND LOGIC
# PART 2C: LEGAL SHIELD RAG
# ============================================================================

from snowflake.snowpark import Session
import json

def get_legal_context(session: Session, defect_description: str) -> str:
    """
    Retrieves relevant building code citations for a given defect using Snowflake Cortex Search.
    
    Args:
        session (Session): The active Snowpark session.
        defect_description (str): The text description of the defect from the image analysis.
        
    Returns:
        str: A formatted string containing the legal citation and context.
    """
    try:
        # Construct the prompt for Cortex Search or RAG
        # We query the BUILDING_CODES_CHUNKS table (Vector Store).
        
        # Note: In a full implementation, we'd use SNOWFLAKE.CORTEX.EMBED_TEXT
        # to vectorize the query and perform cosine similarity against the table.
        # Below is a simulation of that logic using a SQL query execution from Python.
        
        query = f"""
        SELECT 
            SECTION_TITLE, 
            CHUNK_TEXT 
        FROM BUILDING_CODES_CHUNKS
        ORDER BY VECTOR_L2_DISTANCE(
            SNOWFLAKE.CORTEX.EMBED_TEXT_768('snowflake-arctic-embed-m', '{defect_description}'),
            SNOWFLAKE.CORTEX.EMBED_TEXT_768('snowflake-arctic-embed-m', CHUNK_TEXT)
        ) ASC
        LIMIT 1;
        """
        
        # Exponential backoff retry logic is implicitly handled by Snowflake driver 
        # but can be explicit here if needed.
        
        result = session.sql(query).collect()
        
        if result:
            row = result[0]
            title = row['SECTION_TITLE']
            text = row['CHUNK_TEXT']
            return f"**Building Code Violation Potential:**\n> **{title}**: \"{text}\"\n\n*Consult a certified inspector for official verification.*"
        else:
            return "No specific building code citation found for this issue."

    except Exception as e:
        # Safe fallback
        return f"Legal Shield RAG Service Unavailable. (Error: {str(e)})"
