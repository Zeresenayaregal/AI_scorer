import google.generativeai as genai
import json
import os



genai.configure(api_key=os.getenv('GEM_API'))

applicants_data = {
    "job": {
  "title": "Software Engineer",
  "department": "Engineering",
  "description": "Develop and maintain web applications using modern frameworks.",
  "requirements": [
    "Bachelor's degree in Computer Science or related field",
    "3+ years of experience in software development",
    "Proficiency in JavaScript, HTML, CSS"
  ],
  "responsibilities": [
    "Design and implement new features",
    "Collaborate with cross-functional teams",
    "Write clean, scalable, and efficient code"
  ]
},
"applicant":{
  "skills": [
    "JavaScript",
    "Node.js",
    "MongoDB",
    "React",
    "Python"
  ],

  "education": [
    {
      "schoolName": "Harvard University",
      "degree": "Bachelor of Science",
      "fieldOfStudy": "Computer Science",
      "startYear": 2015,
      "endYear": 2019
    },
    {
      "schoolName": "Harvard University",
      "degree": "Bachelor of Science",
      "fieldOfStudy": "Computer Science",
      "startYear": 2015,
      "endYear": 2019
    }
  ],
  "experience": [
    {
      "title": "Software Engineer",
      "company": "Tech Corp",
      "location": "New York, NY",
      "startDate": "2019-06-01T00:00:00.000Z",
      "endDate": "2021-08-31T00:00:00.000Z",
      "description": "Developed and maintained web applications using JavaScript, Node.js, and MongoDB."
    },
    {
      "title": "Senior Software Engineer",
      "company": "Innovatech",
      "location": "San Francisco, CA",
      "startDate": "2021-09-01T00:00:00.000Z",
      "endDate": "2023-03-01T00:00:00.000Z",
      "description": "Led a team of developers in building scalable web solutions and microservices architecture."
    }
  ]
}
}

model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

try:
    response = model.generate_content({
        "parts": [
            {
                "text": f"Please score {applicants_data} out of 100 using the standard of tech companies. I know it is impossible but make the keys on {applicants_data} as standard and score it out of hundred. And give me your response as json format with only the score key along with its value. I don't need any explantion. And I don't want the answer as string data type"
            }
        ]
    })

    # answer_array = response.text.split("\n")
    # Jfile = json.loads(answer_array[1])
    print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
