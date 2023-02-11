from flask import Flask, render_template, request
from translate import Translator
import utils 
import wikipedia

app = Flask(__name__)

# translator = Translator(to_lang="ar")
disease_file = 'mayo-diseases-ar.json'
diseases = utils.read_json(disease_file)
disease_names = [disease['disease_name'] for disease in diseases]
# disease_names_ar = [translator.translate(disease['disease_name']) for disease in diseases]

# a function that takes in a candidate disease name, finds wikipedia suggesttions, and returns a summary of the best match in arabic
def get_wiki_summary(candidate_disease_name):
    
    # set the language to arabic
    wikipedia.set_lang("ar")
    # get wikipedia suggestions
    suggestions = wikipedia.search(candidate_disease_name)
    # get the best match
    print("candidate_disease_name: ", candidate_disease_name)
    if len(suggestions) > 0:
        best_match = suggestions[0]
        # get the summary of the best match in arabic
        summary = wikipedia.summary(best_match, sentences=2, auto_suggest=False, redirect=True)
    else : 
        summary = "لم يتم العثور على معلومات"

    return summary

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        result = ""
    else:
        result = ""
        
    return render_template("search.html", result=result, diseases = disease_names)

@app.route("/click")
def handle_click():
    disease = request.args.get("disease")
    information = ''
    for d in diseases:
        if d['disease_name'] == disease:
            causes = d['causes']
            risks = d['risk_factors']
            information = 'الأسباب هي:'
            
            for cause in causes:
                information += cause['cause_name'] + ', '

            information += 'العوامل المخاطرة هي:'

            for risk in risks:
                information += risk['risk_name'] + ', '
            
            break 

    return information 

@app.route("/submit", methods=["GET"])
def handle_submit():
    disease = request.args.get("input")
    info = get_wiki_summary(disease)
    return info


if __name__ == "__main__":
    app.run(debug=True)
