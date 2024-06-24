from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
import boto3
import json
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from datetime import timedelta
from flask_migrate import Migrate


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

#Configuration for your PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:B0nnie7Clyde@146.169.232.121/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate


# Define your data model
class Complaint(db.Model):
    complaint_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
available_models = ["mistral.mistral-7b-instruct-v0:2", "anthropic.claude-3-sonnet-20240229-v1:0",
          "mistral.mixtral-8x7b-instruct-v0:1", "mistral.mistral-large-2402-v1:0"]

chosen_model = available_models[2]

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
def get_complaint_info(complaint: str, modelId: str) -> tuple[int, str, str]:
    kwargs: dict = get_kwargs(complaint, modelId)
    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        try:
            response = bedrock_runtime.invoke_model(**kwargs)
            response_body = json.loads(response.get('body').read())
            text = response_body['outputs'][0]['text'].strip()
            urgency: int = int(text[0])
            text: str = text[1:].strip()
            split_index: int = text.find('\n')
            summary: str = text[:split_index]
            category: str = text[split_index + 1:]
            newline_index = category.find('\n')
            if newline_index != -1:
                category = category[:newline_index]
            if category[-1] == '.':
                print(category)
                category = category[:-1]
            return urgency, summary, category
        except (ValueError, KeyError, IndexError):
            attempts += 1
            if attempts >= max_attempts:
                raise Exception(f"Failed to get complaint info after {max_attempts} attempts")
    return -1, "Failed to process complaint", "failed category"


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
    modelId = chosen_model
    latitude, longitude = get_geocode(data['address'], 'AIzaSyDa3XR-yUCXjf7QRLYuSDj1K6YNYNdGP4Q')
    try:
        urgency, summary, category = get_complaint_info(data['complaintBody'], modelId)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    new_complaint = Complaint(
        complaint_text=data['complaintBody'],
        #time_stamp=data['time_stamp'],
        title=data['title'],
        first_name=data['firstName'],
        last_name=data['surname'],
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
            "sentiment": str(d.urgency)  # Assuming urgency is the sentiment
        }
        for index, d in enumerate(data)
    }
    return jsonify(result), 200


#endpoint for analytics
@app.route('/analytics', methods=['GET'])
def get_analytics():
    complaint_counts = db.session.query(
        Complaint.category, func.count(Complaint.complaint_id).label('count')
    ).group_by(Complaint.category).all()

    if not complaint_counts:
        return jsonify({"message": "No complaints found"}), 200

    max_complaints_category = max(complaint_counts, key=lambda x: x[1])
    min_complaints_category = min(complaint_counts, key=lambda x: x[1])

    fixed_categories = ["Adult Social Care", "Business", "Children's Services"]
    complaints_per_category = {category: 0 for category in fixed_categories}

    for category, count in complaint_counts:
        if category in complaints_per_category:
            complaints_per_category[category] = count

    complaints_array = [complaints_per_category[category] for category in fixed_categories]

    total_complaints = db.session.query(func.count(Complaint.complaint_id)).scalar()

    result = {
        "total_complaints": total_complaints,
        "cat_most": max_complaints_category[0],
        "cat_least": min_complaints_category[0],
        "catPCdata": complaints_array
    }

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
