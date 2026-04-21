import logging

from modules.audit import get_patient_history
from modules.validation import LAB_REFERENCE_RANGES

logger = logging.getLogger(__name__)


TRACKED_PARAMETERS = [
    "haemoglobin", "wbc", "platelets", "glucose", "hba1c",
    "creatinine", "cholesterol", "tsh", "sgpt", "sgot",
    "sodium", "potassium", "bilirubin_total", "ldl", "hdl", "triglycerides",
]


def _determine_trend_status(values):
    if len(values) < 2:
        return "Stable"
    first_val = values[0][1]
    last_val = values[-1][1]
    if first_val == 0:
        return "Stable"
    change_pct = ((last_val - first_val) / abs(first_val)) * 100
    if abs(change_pct) < 5:
        return "Stable"
    if change_pct > 5:
        return "Increasing"
    return "Decreasing"


def analyze_patient_trends(patient_name, current_lab_values):
    """
    Compare current lab values against previous audited reports.
    """
    if not patient_name or patient_name.strip().lower() in ("unknown", "", "null", "none"):
        return {
            "trend_summary": "No previous data available.",
            "trend_status": "Stable",
            "trend_insight": "First report for this patient. No historical comparison possible.",
        }

    history = get_patient_history(patient_name)
    if not history:
        return {
            "trend_summary": "No previous data available.",
            "trend_status": "Stable",
            "trend_insight": "No prior records found for this patient.",
        }

    trend_lines = []
    worsening_params = []
    improving_params = []
    stable_params = []

    for param in TRACKED_PARAMETERS:
        current_val = current_lab_values.get(param)
        if current_val is None:
            continue

        historical = []
        for entry in history:
            lab_values = entry.get("lab_values", {})
            value = lab_values.get(param)
            if value is not None:
                historical.append((entry["timestamp"], value))

        if not historical:
            continue

        prev_val = historical[-1][1]
        param_display = param.replace("_", " ").title()
        trend_lines.append(f"{param_display}: {prev_val} → {current_val}")

        direction = _determine_trend_status(historical + [("current", current_val)])
        if direction == "Stable":
            stable_params.append(param_display)
            continue

        if param == "hdl":
            if current_val > prev_val:
                improving_params.append(param_display)
            else:
                worsening_params.append(param_display)
            continue

        ref = LAB_REFERENCE_RANGES.get(param)
        if ref:
            midpoint = (ref[0] + ref[1]) / 2
            if abs(current_val - midpoint) < abs(prev_val - midpoint):
                improving_params.append(param_display)
            else:
                worsening_params.append(param_display)
        elif direction == "Decreasing":
            improving_params.append(param_display)
        else:
            worsening_params.append(param_display)

    if not trend_lines:
        return {
            "trend_summary": "Previous records exist but no comparable lab values found.",
            "trend_status": "Stable",
            "trend_insight": f"{len(history)} previous report(s) on file. Different test parameters in prior reports.",
        }

    if len(worsening_params) > len(improving_params):
        overall_status = "Worsening"
    elif len(improving_params) > len(worsening_params):
        overall_status = "Improving"
    else:
        overall_status = "Stable"

    trend_summary = "; ".join(trend_lines[:5])

    insight_parts = []
    if improving_params:
        insight_parts.append(f"{', '.join(improving_params[:3])} showing improvement.")
    if worsening_params:
        insight_parts.append(f"{', '.join(worsening_params[:3])} trending unfavorably.")
    if stable_params and not improving_params and not worsening_params:
        insight_parts.append("Parameters remain stable.")
    insight = " ".join(insight_parts) if insight_parts else "Trends within expected variation."

    return {
        "trend_summary": trend_summary,
        "trend_status": overall_status,
        "trend_insight": f"Based on {len(history)} previous report(s). {insight}",
    }
