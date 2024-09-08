from flask import Flask, request, jsonify
import json
import google.generativeai as genai
import os

app = Flask(__name__)


genai.configure(api_key=os.getenv('GEM_API'))

@app.route('/evaluate', methods=['POST'])
def evaluate_applicant():
    data = request.get_json()

    if not data or 'applicant' not in data:
        return jsonify({"error": "Invalid input data"}), 400

    applicant_data = data['applicant']

    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

    try:
        response = model.generate_content({
            "parts": [
                {
                    "text": f"Please score {applicant_data} out of 100 using the standard of tech companies. I know it is impossible but make the keys on {applicant_data} as standard and score it out of hundred. And give me your response as json format with only the applicant_name key and score key along with their value. I don't need any explanation."
                }
            ]
        })

        answer_array = response.text.split("\n")
        result = json.loads(answer_array[1])
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
