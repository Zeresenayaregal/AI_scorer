from flask import Flask, request, jsonify
import json
import google.generativeai as genai
import os
import logging
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)

# Check for required environment variables
API_KEY = os.getenv('GEM_API')
if not API_KEY:
    raise ValueError("The GEM_API environment variable is not set.")

# Configure the Generative AI model
genai.configure(api_key=API_KEY)

@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate_applicants():
    logging.info("Received request to evaluate applicants.")
    data = request.get_json()

    if not data or 'applicants' not in data:
        return jsonify({"error": "Invalid input data"}), 400

    applicants_data = data['applicants']

    # Input validation (ensure applicants_data is a list of dictionaries)
    if not isinstance(applicants_data, list) or not all(isinstance(applicant, dict) for applicant in applicants_data):
        return jsonify({"error": "Invalid applicants data format"}), 400

    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

    try:
        response = model.generate_content({
            "parts": [
                {
                    "text": f"Please score {applicants_data} out of 100 using the standard of tech companies. "
                            f"Make the keys on {applicants_data} as standard and score it out of hundred. "
                            f"Give the response as JSON format with only the applicant_name key and score key."
                }
            ]
        })

        answer_array = response.text.split("\n")
        
        # Ensure response is in the expected format
        if len(answer_array) < 2:
            return jsonify({"error": "Invalid response format from the model"}), 500
        
        result = json.loads(answer_array[1])

        # Validate the result structure
        if not isinstance(result, dict) or 'applicant_name' not in result or 'score' not in result:
            return jsonify({"error": "Response does not contain required keys"}), 500

        return jsonify(result)

    except (IndexError, json.JSONDecodeError):
        return jsonify({"error": "Invalid response format from the model"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on all interfaces for accessibility