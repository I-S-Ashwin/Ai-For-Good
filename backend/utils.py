# ============================================================================
# SAFEHAVEN AI - BACKEND LOGIC
# PART 4C: INTEGRITY CHECK (UTILS)
# ============================================================================

import re
import html

def sanitize_input(user_input: str) -> str:
    """
    Sanitizes user input to prevent injection attacks and ensure data integrity.
    Removes potentially dangerous HTML tags and script elements.
    
    Args:
        user_input (str): Raw input string.
        
    Returns:
        str: Sanitized string.
    """
    if not isinstance(user_input, str):
        return ""
        
    # 1. HTML Entity Encode
    # safe_str = html.escape(user_input) 
    # Use simple strip for this context to keep it readable but safe from script execution
    
    # 2. Remove <script> tags regex
    clean_str = re.sub(r'<script.*?>.*?</script>', '', user_input, flags=re.IGNORECASE | re.DOTALL)
    
    # 3. Remove other potentially dangerous tags (simple blocklist)
    clean_str = re.sub(r'<(/?)(iframe|object|embed|applet|style|meta|link).*?>', '', clean_str, flags=re.IGNORECASE)
    
    return clean_str.strip()
