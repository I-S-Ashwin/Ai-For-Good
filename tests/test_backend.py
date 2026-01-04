# ============================================================================
# SAFEHAVEN AI - TESTING SUITE
# PART 5: FRONTEND/BACKEND TESTS
# ============================================================================

import pytest
import sys
import os
import json

# Add parent dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.validators import validate_cortex_output
from backend.cost_estimator import CostEstimator
from backend.utils import sanitize_input

# 1. Test Validators
def test_validate_cortex_output_valid():
    valid_json = '{"defect": "Crack", "severity": 50, "visual_description": "Bad crack", "recommended_fix": "Fill it"}'
    result = validate_cortex_output(valid_json)
    assert result['defect'] == "Crack"
    assert result['severity'] == 50

def test_validate_cortex_output_invalid():
    invalid_json = '{"defect": "Crack", "severity": "HIGH"}' # Severity should be int
    result = validate_cortex_output(invalid_json)
    assert result['defect'] == "Analysis Pending / Format Error"

# 2. Test Cost Estimator
def test_cost_estimator_logic():
    # Base for water_damage is 500
    # Severity 10 (multiplier 1.0)
    # Region 1.0
    # Expected: 500 * 1.0 * 1.0 = 500
    # Range: 425 - 575
    
    est = CostEstimator.estimate_repair("water_damage", 10, 1.0)
    assert est['min_estimate_usd'] == 425.0
    assert est['max_estimate_usd'] == 575.0

def test_cost_estimator_high_severity():
    # Base 500
    # Severity 90 (multiplier 4.0) -> 2000
    est = CostEstimator.estimate_repair("water_damage", 90, 1.0)
    midpoint = (est['min_estimate_usd'] + est['max_estimate_usd']) / 2
    assert midpoint == 2000.0

# 3. Test Sanitization
def test_sanitize_input():
    dirty = "Hello <script>alert('xss')</script> World"
    clean = sanitize_input(dirty)
    assert clean == "Hello  World" or clean == "Hello World" # Regex might leave double space
