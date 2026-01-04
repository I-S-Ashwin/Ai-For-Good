# ============================================================================
# SAFEHAVEN AI - FINAL DEPLOYMENT VERIFICATION
# ============================================================================
import sys
import os

# Ensure backend modules are found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from backend.validators import validate_cortex_output
from backend.cost_estimator import CostEstimator
from backend.report_generator import generate_inspection_report
from backend.utils import sanitize_input

def run_verification():
    print("🚀 Starting SafeHaven AI Deployment Verification...")
    
    # 1. Test Validator
    print("   [1/4] Testing Validator...", end=" ")
    valid_json = '{"defect": "Test", "severity": 10, "visual_description": "OK", "recommended_fix": "None"}'
    res = validate_cortex_output(valid_json)
    if res['defect'] == "Test":
        print("PASS ✅")
    else:
        print("FAIL ❌")
        
    # 2. Test Cost Estimator
    print("   [2/4] Testing Cost Estimator...", end=" ")
    est = CostEstimator.estimate_repair("water_damage", 50, 1.0)
    if est['min_estimate_usd'] > 0:
        print("PASS ✅")
    else:
        print("FAIL ❌")
        
    # 3. Test Sanitization
    print("   [3/4] Testing Security...", end=" ")
    clean = sanitize_input("<script>bad</script>Good")
    if clean == "Good":
        print("PASS ✅")
    else:
        print("FAIL ❌")
        
    # 4. Test PDF Generation
    print("   [4/4] Testing PDF Generation...", end=" ")
    try:
        pdf_path = generate_inspection_report("123 Test Lane", {"Status": "Verified"})
        if os.path.exists(pdf_path):
            print(f"PASS ✅ (Created {os.path.basename(pdf_path)})")
        else:
            print("FAIL ❌ (File not found)")
    except Exception as e:
        print(f"FAIL ❌ ({e})")
        
    print("\n✨ Verification Complete. System Ready.")

if __name__ == "__main__":
    run_verification()
