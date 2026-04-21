import logging

from modules.validation import (
    CLINICAL_INFERENCE_RULES,
    LAB_REFERENCE_RANGES,
    extract_lab_value,
)

logger = logging.getLogger(__name__)


DIAGNOSIS_PARAMETER_MAP = {
    "Severe Anaemia": {"params": ["haemoglobin"], "group": "anaemia"},
    "Moderate Anaemia": {"params": ["haemoglobin"], "group": "anaemia"},
    "Mild Anaemia": {"params": ["haemoglobin"], "group": "anaemia"},
    "Microcytic Anaemia": {"params": ["haemoglobin", "mcv", "rdw"], "group": "anaemia_type"},
    "Macrocytic Anaemia": {"params": ["haemoglobin", "mcv"], "group": "anaemia_type"},
    "Diabetes Mellitus": {"params": ["hba1c", "glucose"], "group": "diabetes"},
    "Pre-Diabetes": {"params": ["hba1c", "glucose"], "group": "diabetes"},
    "Impaired Fasting Glucose": {"params": ["glucose"], "group": "diabetes"},
    "Chronic Kidney Disease": {"params": ["creatinine", "urea"], "group": "kidney"},
    "Renal Impairment": {"params": ["creatinine", "urea"], "group": "kidney"},
    "Significant Hepatitis / Liver Injury": {"params": ["sgpt", "sgot", "bilirubin_total"], "group": "liver_enzyme"},
    "Elevated Liver Enzymes": {"params": ["sgpt", "sgot"], "group": "liver_enzyme"},
    "Hypercholesterolaemia": {"params": ["cholesterol", "ldl"], "group": "lipids"},
    "High LDL Cholesterol": {"params": ["ldl", "cholesterol"], "group": "lipids"},
    "Hypertriglyceridaemia": {"params": ["triglycerides"], "group": "lipids"},
    "Hypothyroidism": {"params": ["tsh"], "group": "thyroid"},
    "Subclinical Hypothyroidism": {"params": ["tsh"], "group": "thyroid"},
    "Hyperthyroidism": {"params": ["tsh"], "group": "thyroid"},
    "Subclinical Hyperthyroidism": {"params": ["tsh"], "group": "thyroid"},
    "Severe Hyponatraemia": {"params": ["sodium"], "group": "sodium"},
    "Hyponatraemia": {"params": ["sodium"], "group": "sodium"},
    "Severe Hypernatraemia": {"params": ["sodium"], "group": "sodium"},
    "Hypernatraemia": {"params": ["sodium"], "group": "sodium"},
    "Hypokalaemia": {"params": ["potassium"], "group": "potassium"},
    "Hyperkalaemia": {"params": ["potassium"], "group": "potassium"},
}


def _get_reference_range(param_name):
    ref = LAB_REFERENCE_RANGES.get(param_name)
    if not ref:
        return None, None, None
    return ref[0], ref[1], ref[4]


def _get_rules_for_diagnosis(diagnosis):
    rules = []
    for group_rules in CLINICAL_INFERENCE_RULES.values():
        for param_name, direction, threshold, condition in group_rules:
            if condition == diagnosis:
                rules.append((param_name, direction, threshold))
    return rules


def _severity_bucket(score):
    if score > 0.30:
        return "High"
    if score > 0.10:
        return "Medium"
    return "Low"


def _determine_confidence(diagnosis, lab_text):
    rules = _get_rules_for_diagnosis(diagnosis)
    if not rules:
        info = DIAGNOSIS_PARAMETER_MAP.get(diagnosis, {})
        primary_param = (info.get("params") or [None])[0]
        if not primary_param:
            return "Medium"
        value, _ = extract_lab_value(lab_text, primary_param)
        if value is None:
            return "Low"
        low, high, _ = _get_reference_range(primary_param)
        if low is None or high is None:
            return "Medium"
        if value < low and low:
            return _severity_bucket((low - value) / low)
        if value > high and high:
            return _severity_bucket((value - high) / high)
        return "Low"

    strongest = 0.0
    matched = False
    for param_name, direction, threshold in rules:
        value, _ = extract_lab_value(lab_text, param_name)
        if value is None:
            continue
        if direction == "low" and value < threshold and threshold:
            strongest = max(strongest, (threshold - value) / threshold)
            matched = True
        elif direction == "high" and value > threshold and threshold:
            strongest = max(strongest, (value - threshold) / threshold)
            matched = True

    if matched:
        return _severity_bucket(strongest)

    info = DIAGNOSIS_PARAMETER_MAP.get(diagnosis, {})
    primary_param = (info.get("params") or [None])[0]
    if not primary_param:
        return "Medium"
    value, _ = extract_lab_value(lab_text, primary_param)
    if value is None:
        return "Low"
    low, high, _ = _get_reference_range(primary_param)
    if low is None or high is None:
        return "Medium"
    if value < low and low:
        return _severity_bucket((low - value) / low)
    if value > high and high:
        return _severity_bucket((value - high) / high)
    return "Low"


def _format_reason_part(param_name, value, unit, low, high, direction=None, threshold=None):
    display_unit = unit or ""
    param_display = param_name.replace("_", " ").title()
    range_text = ""
    if low is not None and high is not None:
        range_text = f"; normal {low}-{high} {display_unit}".rstrip()

    if direction == "low":
        return f"low {param_display} ({value} {display_unit}{range_text})".strip()
    if direction == "high":
        return f"high {param_display} ({value} {display_unit}{range_text})".strip()

    status = None
    if low is not None and value < low:
        status = "low"
    elif high is not None and value > high:
        status = "high"

    if status:
        return f"{status} {param_display} ({value} {display_unit}{range_text})".strip()
    if threshold is not None:
        return f"{param_display} ({value} {display_unit}; threshold {threshold} {display_unit})".strip()
    return f"{param_display} ({value} {display_unit}{range_text})".strip()


def generate_diagnosis_explanations(diagnoses, lab_text):
    """
    Build structured reasoning blocks for validated diagnoses.
    Returns at most 3 explanations with actual extracted lab values only.
    """
    if not diagnoses or not lab_text:
        return []

    explanations = []
    for diagnosis in (diagnoses or [])[:3]:
        info = DIAGNOSIS_PARAMETER_MAP.get(diagnosis)
        if not info:
            explanations.append({
                "diagnosis": diagnosis,
                "confidence": "Medium",
                "reason": f"{diagnosis} identified based on clinical assessment."
            })
            continue

        rules_by_param = {}
        for param_name, direction, threshold in _get_rules_for_diagnosis(diagnosis):
            rules_by_param.setdefault(param_name, []).append((direction, threshold))

        reason_parts = []
        seen_parts = set()
        for param_name in info["params"]:
            value, extracted_unit = extract_lab_value(lab_text, param_name)
            if value is None:
                continue

            low, high, ref_unit = _get_reference_range(param_name)
            unit = ref_unit or extracted_unit or ""
            added = False

            for direction, threshold in rules_by_param.get(param_name, []):
                fires = (
                    direction == "low" and value < threshold
                ) or (
                    direction == "high" and value > threshold
                )
                if not fires:
                    continue
                part = _format_reason_part(param_name, value, unit, low, high, direction, threshold)
                if part not in seen_parts:
                    reason_parts.append(part)
                    seen_parts.add(part)
                added = True

            if added:
                continue

            outside_reference = (
                low is not None and value < low
            ) or (
                high is not None and value > high
            )
            if outside_reference or not reason_parts:
                part = _format_reason_part(param_name, value, unit, low, high)
                if part not in seen_parts:
                    reason_parts.append(part)
                    seen_parts.add(part)

        if reason_parts:
            reason = f"{', '.join(reason_parts)} — consistent with {diagnosis.lower()}."
        else:
            reason = f"{diagnosis} identified based on available lab parameters."

        explanations.append({
            "diagnosis": diagnosis,
            "confidence": _determine_confidence(diagnosis, lab_text),
            "reason": reason,
        })

    return explanations
