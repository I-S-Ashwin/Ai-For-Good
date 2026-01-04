# ============================================================================
# SAFEHAVEN AI - BACKEND LOGIC
# PART 2A: VALIDATION LAYER
# ============================================================================

import json
from typing import Optional
from pydantic import BaseModel, ValidationError

class DefectModel(BaseModel):
    """
    Pydantic model to strictly validate the structure of the AI's response.
    Ensures that downstream applications (like the UI) don't crash due to malformed JSON.
    """
    defect: str
    severity: int  # 0-100
    visual_description: str
    recommended_fix: str

def validate_cortex_output(json_str: str) -> dict:
    """
    Parses and validates the JSON string returned by Snowflake Cortex AI.
    
    Args:
        json_str (str): The raw string output from the LLM.
        
    Returns:
        dict: A valid dictionary matching DefectModel, or a safe fallback.
    """
    try:
        # Cortex might sometimes wrap the JSON in markdown code blocks (e.g., ```json ... ```)
        # We clean this up just in case.
        cleaned_str = json_str.replace("```json", "").replace("```", "").strip()
        data = json.loads(cleaned_str)
        
        # Validate using Pydantic
        model = DefectModel(**data)
        return model.model_dump()
        
    except (json.JSONDecodeError, ValidationError) as e:
        # ERROR SUPPRESSION & SELF-CORRECTION
        # If the AI hallucinates bad JSON, we return a safe fallback object 
        # so the application UI continues to function ("Anti-Gravity" reliability).
        print(f"Validation Error: {e}") # Log for debugging
        return {
            "defect": "Analysis Pending / Format Error",
            "severity": 0,
            "visual_description": "The system could not automatically parse the defect details. Manual review required.",
            "recommended_fix": "Please consult a human inspector."
        }
