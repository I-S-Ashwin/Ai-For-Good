# ============================================================================
# SAFEHAVEN AI - BACKEND LOGIC
# PART 4A: SMART COST ESTIMATOR (ALGORITHM)
# ============================================================================

from typing import Dict, Tuple

class CostEstimator:
    """
    Intelligent Cost Estimation Engine for Home Repairs.
    Uses generic baseline data adjusted by severity and regional factors.
    """
    
    # Baseline costs (avg per unit or per fix)
    BASELINE_COSTS = {
        "water_damage": 500.0,      # Per sq ft impact base
        "electrical_issue": 250.0,  # Per outlet/fixture
        "structural_crack": 1500.0, # Per linear foot of repair
        "mold_remediation": 800.0,  # Base room treatment
        "roof_leak": 1200.0         # Patch repair base
    }
    
    # Severity Multiplier: (0-100 score) -> Multiplier
    # 0-20: Minor (1.0x) | 21-50: Moderate (1.5x) | 51-80: Serious (2.5x) | 81-100: Critical (4.0x)
    
    @staticmethod
    def _get_severity_multiplier(severity_score: int) -> float:
        if severity_score <= 20: return 1.0
        if severity_score <= 50: return 1.5
        if severity_score <= 80: return 2.5
        return 4.0

    @staticmethod
    def estimate_repair(defect_type: str, severity: int, region_factor: float = 1.0) -> Dict[str, float]:
        """
        Calculates the estimated repair cost range.
        
        Args:
            defect_type (str): Key matching BASELINE_COSTS (e.g., 'water_damage').
            severity (int): 0-100 severity score.
            region_factor (float): Multiplier for expensive markets (e.g., NY=1.5, TX=1.0).
            
        Returns:
            dict: {min_estimate, max_estimate, confidence_level}
        """
        base = CostEstimator.BASELINE_COSTS.get(defect_type, 300.0) # Fallback $300
        multiplier = CostEstimator._get_severity_multiplier(severity)
        
        # Calculate algorithmic cost
        estimated_cost = base * multiplier * region_factor
        
        # Create a range (+/- 15%)
        cost_min = round(estimated_cost * 0.85, 2)
        cost_max = round(estimated_cost * 1.15, 2)
        
        return {
            "min_estimate_usd": cost_min,
            "max_estimate_usd": cost_max,
            "severity_multiplier": multiplier,
            "calculation_note": f"Base ${base} x Severity {multiplier}x"
        }
