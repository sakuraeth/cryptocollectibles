import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()   # Load environment variables

# Flask app initialization
app = Flask(__name__)

# Assuming metadata is stored in a JSON file for simplicity
METADATA_FILE = os.getenv('METADATA_FILE', 'metadata.json')

def load_metadata():
    """Load NFT metadata from the file."""
    try:
        with open(METADATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_metadata(metadata):
    """Save NFT metadata to the file."""
    with open(METADATA_FILE, 'w') as file:
        json.dump(metadata, file, indent=4)

@app.route('/metadata', methods=['GET'])
def get_metadata():
    """Retrieve all NFT metadata."""
    metadata = load_metadata()
    return jsonify(metadata)

@app.route('/metadata/<string:nft_id>', methods=['GET'])
def get_single_metadata(nft_id):
    """Retrieve metadata for a single NFT based on its ID."""
    metadata = load_metadata()
    return jsonify(metadata.get(nft_id, {}))

@app.route('/metadata', methods=['POST'])
def add_metadata():
    """Add or update metadata for an NFT."""
    new_metadata = request.json
    if not new_metadata.get('id'):
        return jsonify({'error': 'Missing NFT ID'}), 400
    
    metadata = load_metadata()
    metadata[new_metadata['id']] = new_metadata
    save_metadata(metadata)
    
    return jsonify({'message': 'Metadata added/updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)