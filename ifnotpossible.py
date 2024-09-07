from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)


API_KEY = os.getenv('GEM_API')

GEMINI_URL = "https://europe-west1-aiplatform.googleapis.com/v1/projects/micro-cacao-434818-h2/locations/europe-west1/publishers/google/models/gemini-1.5-flash-001:generateContent"

@app.route('/evaluate', methods=['GET','POST'])
def evaluate_applicants():
    data = request.get_json()

    applicants = data.get('applicants', [])

  
    request_payload = {
        "prompt": "Evaluate the following applicant data and return a score between 0 and 100.",
        "applicants": applicants
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(GEMINI_URL, json=request_payload, headers=headers)

    if response.status_code == 200:
        scores = response.json().get('scores', [])
        applicant_name = response.json().get('applicant_name', [])
        return jsonify({"applicant_name": applicant_name,"scores": scores})
    else:
        return jsonify({"error": "Failed to evaluate applicants"}), 500

if __name__ == '__main__':
    app.run(debug=True)
