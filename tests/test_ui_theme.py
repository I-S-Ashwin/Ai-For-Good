import re
import os

def test_nike_theme_integrity():
    """
    Simulates a 'Visual Regression Test' by scanning the style.css 
    for the critical 'Nike Theme' tokens requested by the user.
    """
    css_path = 'frontend/style.css'
    
    assert os.path.exists(css_path), "style.css must exist"
    
    with open(css_path, 'r') as f:
        css_content = f.read()
        
    # 1. Check for 'Oswald' Typography (Bold/Aggressive)
    assert 'Oswald' in css_content, "Theme must use Oswald font for headers"
    
    # 2. Check for 'Volt' Accent Color (#D0FF00)
    assert '#D0FF00' in css_content, "Theme must use Nike Volt (#D0FF00) accent"
    
    # 3. Check for 3D Perspective Properties
    assert 'perspective' in css_content, "Theme must define 3D perspective"
    assert 'transform-style: preserve-3d' in css_content, "Theme must use preserve-3d"
    assert 'rotateX' in css_content, "Theme must use 3D rotation transforms"
    
    # 4. Check for 'Glassmorphism' elements
    assert 'backdrop-filter' in css_content, "Theme must use glassmorphism blur"
    
    print("✅ Nike 3D Theme Verification Passed: Colors, Fonts, and 3D Engine detected.")

if __name__ == "__main__":
    test_nike_theme_integrity()
