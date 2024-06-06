from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
import boto3
import json
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from datetime import timedelta




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

#Configuration for your PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:B0nnie7Clyde@146.169.235.36/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define your data model
class Complaint(db.Model):
    complaint_id = db.Column(db.Integer, primary_key=True)
    complaint_text = db.Column(db.String)
    time_stamp = db.Column(db.DateTime, default=func.now())
    title = db.Column(db.String(10))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    address = db.Column(db.String(255))
    email = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    category = db.Column(db.String(100))
    summary = db.Column(db.String)
    urgency = db.Column(db.Integer)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

# Initialize the NLP model client
models = ["mistral.mistral-7b-instruct-v0:2", "anthropic.claude-3-sonnet-20240229-v1:0",
          "mistral.mixtral-8x7b-instruct-v0:1", "mistral.mistral-large-2402-v1:0"]

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="eu-west-3",
    aws_access_key_id="AKIA4MTWHQBQDC75SMWG",
    aws_secret_access_key="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"
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


def get_geocode(address: str, api_key: str) -> tuple[float, float]:
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "OK":
        # Extract latitude and longitude from the response
        location = data["results"][0]["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        return latitude, longitude
    else:
        print("Geocoding request failed:", data["status"])
        return 0, 0


# Endpoint to submit data
@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    modelId = models[0]
    latitude, longitude = get_geocode(data['address'], 'AIzaSyDa3XR-yUCXjf7QRLYuSDj1K6YNYNdGP4Q')
    try:
        urgency, summary = get_complaint_info(data['complaint_text'], modelId)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    new_complaint = Complaint(
        complaint_text=data['complaint_text'],
        #time_stamp=data['time_stamp'],
        title=data['title'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        address=data['address'],
        longitude=longitude,
        latitude=latitude,
        email=data['email'],
        telephone=data['telephone'],
        category=data['category'],
        summary=summary,
        urgency=urgency
    )

    db.session.add(new_complaint)
    db.session.commit()

    return jsonify({"message": "Complaint submitted successfully", "summary": summary, "urgency": urgency}), 200


#Endpoint to retrieve data
@app.route('/data', methods=['GET'])
def get_data():
    query = Complaint.query
    # Get filters from query parameters
    urgency = request.args.get('urgency')
    category = request.args.get('category')
    age = request.args.get('age')

    if urgency:
        query = query.filter(Complaint.urgency == int(urgency))
    if category:
        query = query.filter(Complaint.category.ilike(f"%{category}%"))
    if age:
        try:
            days = int(age)
            cutoff_date = func.now() - timedelta(days=days)
            query = query.filter(Complaint.time_stamp >= cutoff_date)
        except ValueError:
            pass

    data = query.all()

    result = {
        f"complaint{index + 1}": {
            "full_complaint": d.complaint_text,
            "timestamp": d.time_stamp.isoformat(),  # Convert timestamp to ISO format
            "name": f"{d.first_name} {d.last_name}",
            "address": d.address,
            "geocode": [d.latitude, d.longitude],
            "email": d.email,
            "telephone": d.telephone,
            "category": d.category,
            "summary": d.summary,
            "sentiment": str(d.urgency) # Assuming urgency is the sentiment
        }
        for index, d in enumerate(data)
    }
    return jsonify(result), 200


if __name__ == '__main__':
    # with app.app_context():
    #     try:
    #         default_complaint = Complaint(
    #             complaint_text="3rd June default complaint text",
    #             title="miss",
    #             first_name="Default",
    #             last_name="User",
    #             address="Default Address",
    #             email="default@example.com",
    #             telephone="1234567890",
    #             category="Default Category",
    #             summary="Default summary",
    #             urgency=1  # Default urgency
    #         )
    #         db.session.add(default_complaint)
    #         db.session.commit()
    #         print("Default complaint inserted successfully")
    #     except Exception as e:
    #         db.session.rollback()
    #         print("Error inserting default complaint:", e)
    app.run(host='0.0.0.0', port=5000, debug=True)
