from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import firestore 
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)
try:
    db = firestore.Client()
    COLLECTION_NAME = os.environ.get('COLLECTION_NAME', 'names')
    names_collection = db.collection(COLLECTION_NAME)
    logging.info(f"Successfully connected to Firestore and using collection '{COLLECTION_NAME}'")
except Exception as e:
    logging.error(f"Failed to connect to Firestore: {e}")
    names_collection = None

@app.route('/api/hello', methods=['GET'])
def get_hello_message():
    your_name = request.args.get('name', 'Guest')
    return jsonify({"message": f"Hello, {your_name}"})

@app.route('/api/names', methods=['POST'])
def add_name():
    if names_collection is None:
        return jsonify({"error": "Database not connected"}), 500

    data = request.get_json()
    if not data or 'name' not in data or not data['name'].strip():
        return jsonify({"error": "Name is required"}), 400

    name_to_add = data['name']
    try:
        update_time, doc_ref = names_collection.add({'name': name_to_add})
        logging.info(f"Name '{name_to_add}' added to Firestore with ID: {doc_ref.id}")
        return jsonify({"message": "Name added successfully", "id": doc_ref.id}), 201
    except Exception as e:
        logging.error(f"Error adding name to Firestore: {e}")
        return jsonify({"error": "Failed to add name"}), 500

@app.route('/api/names', methods=['GET'])
def get_all_names():
    if names_collection is None:
        return jsonify({"error": "Database not connected"}), 500

    try:
        all_names = []
        for doc in names_collection.stream():
            all_names.append(doc.to_dict().get('name'))
        
        all_names = [name for name in all_names if name is not None]

        logging.info(f"Successfully retrieved {len(all_names)} names from Firestore.")
        return jsonify({"names": all_names}), 200
    except Exception as e:
        logging.error(f"Error retrieving names from Firestore: {e}")
        return jsonify({"error": "Failed to retrieve names"}), 500

port = int(os.environ.get("PORT", 8080))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)