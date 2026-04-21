import logging

logger = logging.getLogger(__name__)


CLINICAL_RECOMMENDATION_RULES = {
    "Severe Anaemia": {
        "clinical": [
            "Urgent: Order iron studies (serum iron, ferritin, TIBC, transferrin saturation)",
            "Order reticulocyte count and peripheral blood smear",
            "Consider haematology referral if no improvement in 4 weeks",
        ],
        "patient": [
            "Your blood levels are significantly low. This means your body is not producing enough healthy red blood cells.",
            "Include iron-rich foods: spinach, lentils, red meat, dates, and jaggery in your diet.",
            "Take iron supplements as prescribed by your doctor — preferably with vitamin C (orange juice) for better absorption.",
        ],
    },
    "Moderate Anaemia": {
        "clinical": [
            "Order iron studies (serum iron, ferritin, TIBC)",
            "Repeat CBC in 4–6 weeks to assess response",
            "Evaluate for underlying causes if iron studies are normal",
        ],
        "patient": [
            "Your blood levels are moderately low, which may cause tiredness and weakness.",
            "Try including iron-rich foods like spinach, lentils, dates, pomegranate, and beetroot in your daily diet.",
            "Ensure adequate sleep and hydration.",
        ],
    },
    "Mild Anaemia": {
        "clinical": [
            "Recommend iron studies and repeat CBC in 4–6 weeks",
            "Dietary counselling for iron-rich foods",
        ],
        "patient": [
            "Your blood levels are slightly low, which may mean your body needs more iron.",
            "Try including spinach, lentils, dates, and green leafy vegetables in your diet.",
            "Stay well-hydrated and get regular exercise.",
        ],
    },
    "Microcytic Anaemia": {
        "clinical": [
            "Order iron studies (serum iron, ferritin, TIBC, transferrin saturation)",
            "Consider thalassemia screening (Hb electrophoresis) if iron stores are normal",
            "Repeat CBC in 6–8 weeks post-treatment",
        ],
        "patient": [
            "Your red blood cells are smaller than normal, often linked to low iron.",
            "Eat iron-rich foods and avoid tea/coffee with meals as they reduce iron absorption.",
        ],
    },
    "Macrocytic Anaemia": {
        "clinical": [
            "Order Vitamin B12 and folate levels",
            "Consider thyroid function tests",
            "Review medications (metformin, anticonvulsants can cause B12 deficiency)",
        ],
        "patient": [
            "Your red blood cells are larger than normal, which can be caused by vitamin deficiencies.",
            "Foods rich in Vitamin B12 (dairy, eggs, fish) and folate (green vegetables, legumes) may help.",
        ],
    },
    "Diabetes Mellitus": {
        "clinical": [
            "Confirm with repeat HbA1c or fasting glucose",
            "Order fasting lipid profile and renal function tests",
            "Consider endocrinology referral if HbA1c remains elevated above 8%",
            "Screen for diabetic complications: retinopathy, nephropathy, neuropathy",
        ],
        "patient": [
            "Your blood sugar levels indicate diabetes. This means your body has difficulty controlling sugar levels.",
            "Reduce sugar and refined carbohydrate intake. Choose whole grains over white rice/bread.",
            "Regular exercise (30 minutes daily walking) can significantly help control blood sugar.",
            "Monitor your blood sugar regularly as advised by your doctor.",
        ],
    },
    "Pre-Diabetes": {
        "clinical": [
            "Repeat HbA1c in 3 months",
            "Lifestyle modification counselling",
            "Monitor fasting glucose quarterly",
        ],
        "patient": [
            "Your blood sugar is slightly higher than normal but not yet diabetic.",
            "This is reversible with lifestyle changes — reduce sugar intake, exercise regularly, and maintain a healthy weight.",
            "Include more vegetables, whole grains, and fibre in your diet.",
        ],
    },
    "Impaired Fasting Glucose": {
        "clinical": [
            "Repeat fasting glucose in 3 months",
            "Order HbA1c for comprehensive assessment",
            "Lifestyle counselling",
        ],
        "patient": [
            "Your fasting blood sugar is slightly elevated. Small dietary changes can help.",
            "Reduce sugary drinks and processed foods. Walk for 30 minutes daily.",
        ],
    },
    "Chronic Kidney Disease": {
        "clinical": [
            "Urgent: Order eGFR calculation, urine albumin-creatinine ratio",
            "Refer to nephrologist",
            "Review all medications for nephrotoxicity",
            "Monitor blood pressure closely",
        ],
        "patient": [
            "Your kidney function test shows significant impairment.",
            "Reduce salt intake and stay well-hydrated (unless advised otherwise by your doctor).",
            "Avoid self-medication, especially painkillers (NSAIDs) which can harm kidneys.",
        ],
    },
    "Renal Impairment": {
        "clinical": [
            "Repeat renal function tests in 4–6 weeks",
            "Check urine for proteinuria",
            "Ensure adequate hydration",
        ],
        "patient": [
            "Your kidney function is slightly reduced.",
            "Drink adequate water, reduce salt, and avoid unnecessary painkillers.",
        ],
    },
    "Significant Hepatitis / Liver Injury": {
        "clinical": [
            "Urgent: Order hepatitis panel (HBsAg, Anti-HCV), liver function panel",
            "Ultrasound abdomen",
            "Consider gastroenterology/hepatology referral",
        ],
        "patient": [
            "Your liver enzymes are significantly elevated, indicating liver stress.",
            "Avoid alcohol completely. Reduce fatty and fried foods.",
            "Consult your doctor promptly for further evaluation.",
        ],
    },
    "Elevated Liver Enzymes": {
        "clinical": [
            "Repeat liver function tests in 4–6 weeks",
            "Review medications for hepatotoxicity",
            "Screen for hepatitis B and C if not done",
        ],
        "patient": [
            "Your liver enzymes are mildly elevated.",
            "Limit alcohol, reduce fatty foods, and maintain a balanced diet.",
        ],
    },
    "Hypercholesterolaemia": {
        "clinical": [
            "Order fasting lipid profile if not done",
            "Assess 10-year cardiovascular risk",
            "Consider statin therapy based on risk stratification",
        ],
        "patient": [
            "Your cholesterol levels are high, which increases heart disease risk.",
            "Reduce fried foods, butter, and red meat. Choose olive oil and fish.",
            "Regular exercise (brisk walking, swimming) helps lower cholesterol.",
        ],
    },
    "High LDL Cholesterol": {
        "clinical": [
            "Lifestyle modification as first line",
            "Repeat lipid profile in 3 months",
        ],
        "patient": [
            "Your 'bad' cholesterol (LDL) is elevated.",
            "Include oats, nuts, and fibre-rich foods. Reduce saturated fats.",
        ],
    },
    "Hypertriglyceridaemia": {
        "clinical": [
            "Dietary modification",
            "Check for secondary causes (diabetes, hypothyroidism, alcohol)",
            "Consider fibrate therapy if >500 mg/dL",
        ],
        "patient": [
            "Your triglyceride levels are high.",
            "Reduce sugar, alcohol, and refined carbs. Include omega-3 rich foods like fish and flaxseeds.",
        ],
    },
    "Hypothyroidism": {
        "clinical": [
            "Confirm with Free T3 and Free T4 if not done",
            "Initiate thyroid hormone replacement",
            "Repeat TSH in 6–8 weeks after starting treatment",
        ],
        "patient": [
            "Your thyroid is underactive, which can cause tiredness, weight gain, and feeling cold.",
            "Take thyroid medication on an empty stomach, 30 minutes before breakfast.",
        ],
    },
    "Subclinical Hypothyroidism": {
        "clinical": [
            "Repeat TSH with Free T4 in 6–8 weeks",
            "Monitor symptoms",
            "Consider treatment if TSH >10 or symptomatic",
        ],
        "patient": [
            "Your thyroid hormone levels are slightly off. This may not need treatment yet.",
            "Regular monitoring is important. Eat a balanced diet with adequate iodine (iodized salt).",
        ],
    },
    "Hyperthyroidism": {
        "clinical": [
            "Order Free T3, Free T4, and thyroid antibodies (TSI/TRAb)",
            "Refer to endocrinologist",
            "Consider thyroid ultrasound",
        ],
        "patient": [
            "Your thyroid is overactive, which can cause weight loss, rapid heartbeat, and anxiety.",
            "Avoid excessive caffeine and iodine-rich supplements until you see your doctor.",
        ],
    },
    "Subclinical Hyperthyroidism": {
        "clinical": [
            "Repeat thyroid function tests in 6–8 weeks",
            "Monitor for atrial fibrillation in elderly patients",
        ],
        "patient": [
            "Your thyroid levels are slightly elevated. Regular monitoring is advised.",
        ],
    },
    "Hyponatraemia": {
        "clinical": [
            "Check serum osmolality, urine sodium, and urine osmolality",
            "Review medications (diuretics, SSRIs)",
            "Assess fluid status",
        ],
        "patient": [
            "Your sodium level is low. This can cause dizziness and confusion.",
            "Avoid excessive water intake. Follow your doctor's fluid recommendations.",
        ],
    },
    "Severe Hyponatraemia": {
        "clinical": [
            "URGENT: Immediate medical evaluation required",
            "Check serum osmolality and urine electrolytes",
            "Consider nephrology consultation",
        ],
        "patient": [
            "Your sodium level is dangerously low. Seek medical attention immediately.",
        ],
    },
    "Hyperkalaemia": {
        "clinical": [
            "Repeat potassium level to confirm (exclude haemolysis)",
            "Order ECG",
            "Review medications (ACE inhibitors, ARBs, potassium-sparing diuretics)",
        ],
        "patient": [
            "Your potassium level is elevated. This needs monitoring.",
            "Limit high-potassium foods: bananas, oranges, potatoes, tomatoes.",
        ],
    },
    "Hypokalaemia": {
        "clinical": [
            "Check magnesium levels",
            "Order ECG",
            "Review diuretic therapy",
        ],
        "patient": [
            "Your potassium level is low.",
            "Include potassium-rich foods: bananas, coconut water, sweet potatoes, spinach.",
        ],
    },
}

DEFAULT_CLINICAL = [
    "Follow-up with primary care physician in 4–6 weeks",
    "Repeat relevant investigations to monitor progress",
]
DEFAULT_PATIENT = [
    "Follow your doctor's advice and attend all scheduled appointments.",
    "Maintain a balanced diet, stay hydrated, and get regular exercise.",
]


def generate_recommendations(diagnoses, risk_level):
    """
    Generate clinician-facing next steps and patient-friendly guidance.
    """
    clinical_recs = []
    patient_guidance = []
    red_flags = []

    disclaimer = (
        "This is not a medical diagnosis. Please consult a qualified "
        "healthcare professional for proper evaluation and treatment."
    )

    if not diagnoses:
        return {
            "clinical_recommendations": ["All parameters within normal limits. Routine follow-up recommended."],
            "patient_guidance": [
                "Your test results appear normal. Continue maintaining a healthy lifestyle with balanced diet and regular exercise."
            ],
            "red_flags": [],
            "disclaimer": disclaimer,
        }

    seen_clinical = set()
    seen_patient = set()

    for diagnosis in (diagnoses or [])[:3]:
        rules = CLINICAL_RECOMMENDATION_RULES.get(diagnosis)
        if not rules:
            for rec in DEFAULT_CLINICAL:
                if rec not in seen_clinical:
                    clinical_recs.append(rec)
                    seen_clinical.add(rec)
            for guidance in DEFAULT_PATIENT:
                if guidance not in seen_patient:
                    patient_guidance.append(guidance)
                    seen_patient.add(guidance)
            continue

        for rec in rules.get("clinical", []):
            if rec not in seen_clinical:
                clinical_recs.append(rec)
                seen_clinical.add(rec)
        for guidance in rules.get("patient", []):
            if guidance not in seen_patient:
                patient_guidance.append(guidance)
                seen_patient.add(guidance)

    if risk_level in ("High", "Critical"):
        red_flags.append("Your results show significant abnormalities. Please consult a doctor immediately.")
        if risk_level == "Critical":
            red_flags.append("URGENT: Some values are in the critical range. Seek immediate medical attention.")

    if risk_level == "Critical" and "URGENT" not in " ".join(clinical_recs):
        clinical_recs.insert(0, "URGENT: Critical values detected — immediate clinical review required.")

    return {
        "clinical_recommendations": clinical_recs,
        "patient_guidance": patient_guidance,
        "red_flags": red_flags,
        "disclaimer": disclaimer,
    }
