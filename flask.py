from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import boto3
import json

app = Flask(__name__)

# Configuration for your PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://YOURUSER:YOURPASSWORD@YOUR_LAPTOP_IP/YOURDATABASE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define your data model
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_complaint = db.Column(db.String(255))
    timestamp = db.Column(db.String(50))
    name = db.Column(db.String(50))
    address = db.Column(db.String(255))
    geocode = db.Column(db.String(50))
    email = db.Column(db.String(255))
    telephone = db.Column(db.String(50))
    category = db.Column(db.String(50))
    summary = db.Column(db.String(255))
    urgency = db.Column(db.Integer)


# Initialize the NLP model client
models = ["mistral.mistral-7b-instruct-v0:2", "anthropic.claude-3-sonnet-20240229-v1:0",
          "mistral.mixtral-8x7b-instruct-v0:1", "mistral.mistral-large-2402-v1:0"]

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="eu-west-3",
    aws_access_key_id="YOUR_AWS_ACCESS_KEY_ID",
    aws_secret_access_key="YOUR_AWS_SECRET_ACCESS_KEY"
)


# Function to get the prompt for the NLP model
def get_prompt(complaint: str) -> str:
    prompt: str = f"""You are an assistant to the council, tasked with categorizing residents' complaints by urgency. Choose the urgency level of the resident complaint after <<<>>> into one of the following predefined categories. It is essential not to provide any explanation to your response:

1) No Urgency: No action required from council.
2) Least Urgent: Complaint is not time-sensitive and not important but must eventually be addressed.
3) Somewhat Urgent: Complaint is not time-sensitive but important.
4) Urgent: Complaint is time-sensitive and must be addressed promptly.
5) Incredibly Urgent: Complaint must be addressed immediately to ensure resident safety.
Respond with the urgency level number as a single character, followed by a one-sentence summary of the complaint.

####
Here is an example:
Complaint: The community garden's watering system has developed a leak, causing water wastage and damaging the nearby path. It's essential to repair this issue promptly to prevent further damage and save water.
4 
Leak in community garden's watering system.

<<<
Complaint: {complaint}
>>>"""
    return prompt


# Function to get kwargs for the NLP model request
def get_kwargs(complaint: str, modelId: str) -> dict:
    prompt: str = get_prompt(complaint)
    body = json.dumps({
        "prompt": f"<s>[INST]{prompt}[/INST]",
        "max_tokens": 30,
        "temperature": 0.0,
        "top_p": 0.9,
        "top_k": 50
    })

    kwargs: dict = {
        "modelId": modelId,
        "contentType": "application/json",
        "accept": "application/json",
        "body": body
    }

    return kwargs


# Function to call NLP model and get complaint info
def get_complaint_info(complaint: str, modelId: str) -> tuple[int, str]:
    kwargs: dict = get_kwargs(complaint, modelId)
    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        try:
            response = bedrock_runtime.invoke_model(**kwargs)
            response_body = json.loads(response.get('body').read())
            text = response_body['outputs'][0]['text'].strip()
            urgency = int(text[0])
            summary = text[1:].strip()
            summary = summary[:summary.find('\n')]
            return urgency, summary
        except (ValueError, KeyError, IndexError):
            attempts += 1
            if attempts >= max_attempts:
                raise Exception(f"Failed to get complaint info after {max_attempts} attempts")
    return -1, "Failed to process complaint"


# Endpoint to submit data
@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    modelId = models[0]
    try:
        urgency, summary = get_complaint_info(data['full_complaint'], modelId)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    new_complaint = Complaint(
        full_complaint=data['full_complaint'],
        timestamp=data['timestamp'],
        name=data['name'],
        address=data['address'],
        geocode=json.dumps(data['geocode']),
        email=data['email'],
        telephone=data['telephone'],
        category=data['category'],
        summary=summary,
        urgency=urgency
    )

    db.session.add(new_complaint)
    db.session.commit()

    return jsonify({"message": "Complaint submitted successfully", "summary": summary, "urgency": urgency}), 200


# Endpoint to retrieve data
# @app.route('/data', methods=['GET'])
# def get_data():
#     filters = request.args
#     query = Complaint.query
#
#     if 'category' in filters:
#         query = query.filter(Complaint.category == filters['category'])
#
#     data = query.all()
#
#     result = [
#         {
#             "full_complaint": d.full_complaint,
#             "timestamp": d.timestamp,
#             "name": d.name,
#             "address": d.address,
#             "geocode": json.loads(d.geocode),
#             "email": d.email,
#             "telephone": d.telephone,
#             "category": d.category,
#             "summary": d.summary,
#             "urgency": d.urgency
#         }
#         for d in data
#     ]

#    return jsonify(result), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #   app.run(debug=True)

