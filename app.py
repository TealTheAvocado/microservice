# microservice.py
from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import random
import requests
import certifi
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = 'mongodb+srv://database_owner:DatabasePassword@cluster0.ep9zacz.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client.flashcards
collection = db.flashcards

@app.route('/')
def index():
    return render_template('index.html')
# Function to connect to MongoDB and retrieve data
def get_data_from_mongodb():
    data = list(collection.find({}))
    return data

@app.route('/test_microservice')
def test_microservice():
    microservice_url = 'http://127.0.0.1:5002/get_data'  # Adjust the URL to match your microservice's URL
    response = requests.get(microservice_url)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return "Failed to fetch data from the microservice."

# Route to get random data from MongoDB
@app.route('/get_data', methods=['GET'])
def get_data():
    data = get_data_from_mongodb()
    # Choose 4 random items from the data
    selected_flashcards = random.sample(data, 6)
    # Format data for the flashcards
    flashcards = []
    for item in selected_flashcards:
        flashcard = {
            'shanghainese': item.get('shanghainese', ''),
            'phonetics': item.get('phonetics', ''),
            'english': item.get('english', ''),
            'category': item.get('category', '')
        }
        flashcards.append(flashcard)
    return jsonify(flashcards)

@app.route('/database')
def show_database():
    try:
        database_records = collection.find({})
        return render_template('database.html', database_records=database_records)
    except Exception as e:
        return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=5002) 
