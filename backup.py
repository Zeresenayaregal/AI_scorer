import torch
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

llama3_pipeline = pipeline('text-generation', model='flyingfishinwater/chinese-baby-llama2', device=0 if torch.cuda.is_available() else -1)

def evaluate_applicant_llama3(applicant):
    prompt = f"""
    Evaluate the following applicant for a software developer role:
    
    Applicant Name: {applicant['applicant_name']}
    
    Job Description:
    {applicant['description']['aboutJob']}
    
    Requirements:
    {applicant['description']['requirements']}
    
    Responsibilities:
    {applicant['description']['responsibilities']}
    
    Additional Information:
    {applicant['description'].get('additional', '')}
    
    Applicant's Education:
    {', '.join([f"{edu['degree']} in {edu['fieldOfStudy']} from {edu['schoolName']} ({edu['startYear']}-{edu['endYear']})" for edu in applicant['education']])}
    
    Applicant's Experience:
    {', '.join([f"{exp['title']} at {exp['company']} ({exp['startDate']} to {exp['endDate']})" for exp in applicant['experience']])}
    
    Applicant's Skills:
    {', '.join(applicant['skills'])}
    
    Please provide a score out of 100 for this applicant.
    """
    
    response = llama3_pipeline(prompt, max_length=50)
    
    try:
        score = int(response[0]['generated_text'].split()[-1])
    except ValueError:
        score = 0  

    return score

@app.route('/evaluate_applicant', methods=['POST'])
def evaluate_applicant():
    applicant = request.json.get('applicant')

    if not applicant:
        return jsonify({"error": "No applicant data provided"}), 400

    try:
        score = evaluate_applicant_llama3(applicant)
        
        return jsonify({
            "applicant_name": applicant['applicant_name'],
            "score": score
        })

    except Exception as e:
        return jsonify({"error": f"Failed to evaluate applicant: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)