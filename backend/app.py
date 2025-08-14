from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
import logging 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app) 
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('DB_NAME', 'hello_app_db')
COLLECTION_NAME = os.environ.get('COLLECTION_NAME', 'names')

client = None
db = None
names_collection = None

def connect_to_mongodb():
    global client, db, names_collection
    try:
        logging.info(f"Attempting to connect to MongoDB at {MONGO_URI}")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ismaster')
        db = client[DB_NAME]
        names_collection = db[COLLECTION_NAME]
        logging.info(f"Successfully connected to MongoDB and selected collection '{COLLECTION_NAME}'")
    except ServerSelectionTimeoutError as err:
        logging.error(f"MongoDB Server Selection Timeout: {err}")
        client = None
        db = None
        names_collection = None
    except ConnectionFailure as err:
        logging.error(f"MongoDB Connection Failure: {err}")
        client = None
        db = None
        names_collection = None
    except Exception as err:
        logging.error(f"An unexpected error occurred during MongoDB connection: {err}", exc_info=True)
        client = None
        db = None
        names_collection = None

connect_to_mongodb()

@app.route('/api/hello', methods=['GET'])
def get_hello_message():
    your_name = request.args.get('name', 'Guest')
    return jsonify({"message": f"Hello, {your_name}"})

@app.route('/api/names', methods=['POST'])
def add_name():
    if names_collection is None:
        logging.error("Attempted to add name, but MongoDB collection is not initialized.")
        return jsonify({"error": "Database not connected or collection not found"}), 500

    data = request.get_json()
    if not data or 'name' not in data:
        logging.warning("Attempted to add name with missing 'name' field in request data.")
        return jsonify({"error": "Name is required"}), 400

    name_to_add = data['name']
    try:
        result = names_collection.insert_one({"name": name_to_add})
        logging.info(f"Name '{name_to_add}' added successfully with ID: {result.inserted_id}")
        return jsonify({"message": "Name added successfully", "id": str(result.inserted_id)}), 201
    except Exception as e:
        logging.error(f"Error adding name '{name_to_add}' to DB: {e}", exc_info=True) # Log full traceback
        return jsonify({"error": "Failed to add name", "details": str(e)}), 500

@app.route('/api/names', methods=['GET'])
def get_all_names():
    if names_collection is None:
        logging.error("Attempted to retrieve names, but MongoDB collection is not initialized.")
        return jsonify({"error": "Database not connected or collection not found"}), 500

    try:
        names = []
        for doc in names_collection.find({}, {"_id": 0, "name": 1}):
            names.append(doc['name'])
        logging.info(f"Successfully retrieved {len(names)} names from DB.")
        return jsonify({"names": names}), 200
    except Exception as e:
        logging.error(f"Error retrieving names from DB: {e}", exc_info=True) 
        return jsonify({"error": "Failed to retrieve names", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
