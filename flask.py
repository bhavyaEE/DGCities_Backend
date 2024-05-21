from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# Configuration for your MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://youruser:yourpassword@192.168.1.100/yourdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define your data model
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    sentiment = db.Column(db.String(50))

# Endpoint to submit data
@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    # Call NLP server for sentiment analysis
    sentiment = call_nlp_server(data['text'])
    # Create a new data entry
    data_entry = Data(text=data['text'], sentiment=sentiment)
    # Add the entry to the database
    db.session.add(data_entry)
    db.session.commit()
    return jsonify({"message": "Data submitted successfully"}), 200

# Endpoint to retrieve data
@app.route('/data', methods=['GET'])
def get_data():
    filters = request.args
    # Query the database based on filters
    data = Data.query.all()
    return jsonify([{"text": d.text, "sentiment": d.sentiment} for d in data]), 200

# Function to call NLP server
def call_nlp_server(text):
    # Replace 'nlp_server_address' with the actual address of your NLP server
    response = requests.post('http://nlp_server_address:5000/analyze', json={'text': text})
    if response.status_code == 200:
        return response.json().get('sentiment')
    else:
        raise Exception("Error calling NLP server")

if __name__ == '__main__':
    app.run(debug=True)
