#!/usr/bin/env python3
import json
from googletrans import Translator




# read json file and store in list
def read_json(file):
    diseases = []
    with open(file) as f:
        data = json.load(f)
        for disease in data:
            diseases.append(disease)
    return diseases

def write_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def translate(disease, lang):
    translator = Translator()
    disease_name_ar = translator.translate(disease['disease_name'], dest=lang)
    causes = [] 
    for cause in disease['causes']:
        cause_name_ar = translator.translate_text(cause['cause_name'], lang).text
        causes.append({'cause_id': cause['cause_id'], 'cause_name': cause_name_ar})
    risks = []
    for risk in disease['risks']:
        risk_name_ar = translator.translate_text(risk['risk_name'], lang).text
        risks.append({'risk_id': risk['risk_id'], 'risk_name': risk_name_ar})
    
    return {'disease_id': disease['disease_id'], 'disease_name': disease_name_ar.text, 'causes': causes, 'risks': risks}

