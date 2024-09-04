import requests
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Assuming you have a LLaMA 3 pipeline set up
llama3_pipeline = pipeline('text-generation', model='LLaMA-3')

def evaluate_applicant_llama3(applicant):
    # Prepare the prompt for LLaMA 3
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
    
    # Generate the evaluation using LLaMA 3
    response = llama3_pipeline(prompt, max_length=50)
    
    # Extract the score from the response (assuming the model outputs a score at the end)
    try:
        score = int(response[0]['generated_text'].split()[-1])  # Extract the last word and convert to int
    except ValueError:
        score = 0  # If parsing fails, assign a default score

    return score

@app.route('/process_applicants', methods=['POST'])
def process_applicants():
    data = request.json
    applicant_api_url = data.get('applicant_api_url')

    if not applicant_api_url:
        return jsonify({"error": "No applicant API URL provided"}), 400

    try:
        # Fetch applicants from the provided API
        response = requests.get(applicant_api_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        applicants = response.json().get('applicants', [])

        if not applicants:
            return jsonify({"error": "No applicants found"}), 404

        results = []

        for applicant in applicants:
            score = evaluate_applicant_llama3(applicant)
            results.append({
                "applicant_name": applicant['applicant_name'],
                "score": score
            })

        # Return the processed scores
        return jsonify({"scores": results})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch applicants: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
