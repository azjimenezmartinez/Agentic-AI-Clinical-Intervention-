clinical_symptom_ontology = {
    "Cardiovascular": {
        "common_symptoms": ["chest pain", "palpitations", "shortness of breath", "edema", "syncope"],
        "severity_indicators": ["persistent chest pain", "severe dyspnea", "cyanosis"],
        "red_flags": ["crushing chest pain", "sudden loss of consciousness", "severe hypotension"],
        "likely_differentials": ["myocardial infarction", "angina", "arrhythmia", "heart failure", "pericarditis"],
        "risk_factors": ["hypertension", "diabetes", "smoking", "family history"],
        "symptom_clusters": [["chest pain", "radiation to arm", "diaphoresis"], ["palpitations", "dizziness"]],
        "progression_patterns": ["gradual onset", "sudden onset", "intermittent"]
    },
    "Respiratory": {
        "common_symptoms": ["cough", "dyspnea", "wheezing", "hemoptysis", "chest tightness"],
        "severity_indicators": ["respiratory distress", "cyanosis", "stridor"],
        "red_flags": ["severe shortness of breath", "inability to speak", "accessory muscle use"],
        "likely_differentials": ["asthma", "COPD", "pneumonia", "pulmonary embolism", "tuberculosis"],
        "risk_factors": ["smoking", "occupational exposure", "immunosuppression"],
        "symptom_clusters": [["cough", "fever", "sputum"], ["wheezing", "chest tightness"]],
        "progression_patterns": ["acute", "chronic", "episodic"]
    },
    "Gastrointestinal": {
        "common_symptoms": ["abdominal pain", "nausea", "vomiting", "diarrhea", "constipation", "hematemesis"],
        "severity_indicators": ["severe pain", "persistent vomiting", "hematochezia"],
        "red_flags": ["rigid abdomen", "bloody stools", "severe dehydration"],
        "likely_differentials": ["gastroenteritis", "appendicitis", "peptic ulcer", "hepatitis", "bowel obstruction"],
        "risk_factors": ["alcohol use", "NSAID use", "recent travel"],
        "symptom_clusters": [["abdominal pain", "fever", "vomiting"], ["diarrhea", "dehydration"]],
        "progression_patterns": ["acute", "chronic", "waxing and waning"]
    },
    "Neurological": {
        "common_symptoms": ["headache", "dizziness", "weakness", "numbness", "seizures", "confusion"],
        "severity_indicators": ["sudden onset", "loss of consciousness", "focal deficits"],
        "red_flags": ["sudden severe headache", "new weakness", "seizure"],
        "likely_differentials": ["stroke", "migraine", "epilepsy", "meningitis", "brain tumor"],
        "risk_factors": ["hypertension", "trauma", "infection"],
        "symptom_clusters": [["headache", "nausea", "photophobia"], ["weakness", "numbness"]],
        "progression_patterns": ["sudden", "progressive", "recurrent"]
    },
    "Endocrine": {
        "common_symptoms": ["polyuria", "polydipsia", "weight change", "fatigue", "heat/cold intolerance"],
        "severity_indicators": ["altered mental status", "severe dehydration", "coma"],
        "red_flags": ["unconsciousness", "severe hypoglycemia", "DKA signs"],
        "likely_differentials": ["diabetes", "thyroid disorders", "adrenal crisis", "Cushing's syndrome"],
        "risk_factors": ["family history", "autoimmune disease"],
        "symptom_clusters": [["polyuria", "polydipsia", "weight loss"], ["fatigue", "cold intolerance"]],
        "progression_patterns": ["gradual", "acute", "fluctuating"]
    },
    "Musculoskeletal": {
        "common_symptoms": ["joint pain", "swelling", "stiffness", "muscle weakness", "deformity"],
        "severity_indicators": ["inability to bear weight", "severe pain", "deformity"],
        "red_flags": ["open fracture", "loss of limb function", "severe swelling"],
        "likely_differentials": ["arthritis", "fracture", "sprain", "osteomyelitis", "rhabdomyolysis"],
        "risk_factors": ["trauma", "overuse", "infection"],
        "symptom_clusters": [["joint pain", "swelling", "redness"], ["muscle pain", "weakness"]],
        "progression_patterns": ["acute", "chronic", "intermittent"]
    },
    "Dermatologic": {
        "common_symptoms": ["rash", "itching", "redness", "swelling", "blisters"],
        "severity_indicators": ["rapid spread", "painful lesions", "systemic symptoms"],
        "red_flags": ["necrotic skin", "bullae", "systemic toxicity"],
        "likely_differentials": ["eczema", "cellulitis", "psoriasis", "herpes zoster", "impetigo"],
        "risk_factors": ["allergies", "immunosuppression", "contact exposure"],
        "symptom_clusters": [["rash", "fever", "swelling"], ["itching", "redness"]],
        "progression_patterns": ["acute", "chronic", "recurrent"]
    },
    "Psychiatric": {
        "common_symptoms": ["depressed mood", "anxiety", "insomnia", "hallucinations", "agitation"],
        "severity_indicators": ["suicidal ideation", "psychosis", "violent behavior"],
        "red_flags": ["suicidal intent", "homicidal intent", "catatonia"],
        "likely_differentials": ["depression", "anxiety disorder", "schizophrenia", "bipolar disorder", "PTSD"],
        "risk_factors": ["family history", "substance abuse", "trauma"],
        "symptom_clusters": [["depressed mood", "insomnia"], ["anxiety", "agitation"]],
        "progression_patterns": ["gradual", "episodic", "acute"]
    },
    "Genitourinary": {
        "common_symptoms": ["dysuria", "hematuria", "frequency", "urgency", "pelvic pain"],
        "severity_indicators": ["severe pain", "fever", "urinary retention"],
        "red_flags": ["anuria", "gross hematuria", "sepsis"],
        "likely_differentials": ["UTI", "pyelonephritis", "renal stones", "prostatitis", "STD"],
        "risk_factors": ["sexual activity", "catheter use", "diabetes"],
        "symptom_clusters": [["dysuria", "frequency", "fever"], ["pelvic pain", "hematuria"]],
        "progression_patterns": ["acute", "chronic", "recurrent"]
    },
    "Infectious Disease": {
        "common_symptoms": ["fever", "chills", "malaise", "rash", "lymphadenopathy"],
        "severity_indicators": ["persistent fever", "sepsis", "shock"],
        "red_flags": ["septic shock", "altered mental status", "multiorgan failure"],
        "likely_differentials": ["viral infection", "bacterial infection", "malaria", "HIV", "tuberculosis"],
        "risk_factors": ["immunosuppression", "recent travel", "exposure history"],
        "symptom_clusters": [["fever", "rash", "lymphadenopathy"], ["chills", "malaise"]],
        "progression_patterns": ["acute", "chronic", "progressive"]
    },
    "Pregnancy": {
        "common_symptoms": ["nausea", "vomiting", "fatigue", "abdominal pain", "vaginal bleeding", "swelling", "headache"],
        "severity_indicators": ["severe abdominal pain", "persistent vomiting", "high blood pressure", "visual changes"],
        "red_flags": ["heavy vaginal bleeding", "severe abdominal pain", "seizure", "loss of fetal movement", "preterm labor"],
        "likely_differentials": ["normal pregnancy", "ectopic pregnancy", "pre-eclampsia", "placental abruption", "miscarriage", "gestational diabetes"],
        "risk_factors": ["advanced maternal age", "hypertension", "diabetes", "previous pregnancy complications", "multiple gestation"],
        "symptom_clusters": [["nausea", "vomiting", "fatigue"], ["abdominal pain", "vaginal bleeding"]],
        "progression_patterns": ["first trimester", "second trimester", "third trimester", "postpartum"]
    }
}
