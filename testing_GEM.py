import google.generativeai as genai
import os



genai.configure(api_key=os.getenv('GEM_API'))

applicants_data = {
    "applicants": [
        {
            "applicant_name": "John Doe",
            "description": {
                "aboutJob": "The Software Developer will be responsible...",
                "requirements": "A bachelor's degree in Computer Science...",
                "responsibilities": "Develop and maintain software applications...",
                "additional": "Familiarity with Agile methodologies..."
            },
            "education": [
                {
                    "schoolName": "University of Technology",
                    "degree": "Bachelor of Science",
                    "fieldOfStudy": "Computer Science",
                    "startYear": 2015,
                    "endYear": 2019
                }
            ],
            "experience": [
                {
                    "title": "Software Developer",
                    "company": "Tech Solutions Inc.",
                    "location": "San Francisco, CA",
                    "startDate": "2020-06-01",
                    "endDate": "2023-09-01",
                    "description": "Worked on developing and maintaining enterprise-level software..."
                }
            ],
            "skills": [
                "Java",
                "Python",
                "SQL",
                "Git",
                "Agile"
            ]
        }
    ]
}

model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

try:
    response = model.generate_content({
        "parts": [
            {
                "text": f"Please score {applicants_data} out of 100 using the standard of tech companies. I know it is impossible but make the keys on {applicants_data} as standard and score it out of hundred. And give me your response as json format with only the applicant_name key and score key along with there value. I don't need any explantion."
            }
        ]
    })
    print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
