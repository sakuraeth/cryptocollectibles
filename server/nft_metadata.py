import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

NFT_METADATA_FILE_PATH = os.getenv('NFT_METADATA_FILE', 'metadata.json')

def load_nft_metadata():
    try:
        with open(NFT_METADATA_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        # Handles the case where the file content is not valid JSON
        return {'error': 'Failed to decode JSON data.'}

def save_nft_metadata(metadata):
    try:
        with open(NFT_METADATA_FILE_PATH, 'w') as file:
            json.dump(metadata, file, indent=4)
    except IOError:
        return False
    return True

@app.route('/metadata', methods=['GET'])
def get_all_nft_metadata():
    metadata = load_nft_metadata()
    
    if isinstance(metadata, dict):
        return jsonify(metadata)
    else:
        return jsonify({'error': 'Unable to retrieve NFT metadata.'}), 500

@app.route('/metadata/<string:nft_id>', methods=['GET'])
def get_nft_metadata(nft_id):
    metadata = load_nft_metadata()

    if isinstance(metadata, dict):
        return jsonify(metadata.get(nft_id, {}))
    else:
        return jsonify({'error': 'Unable to retrieve NFT metadata.'}), 500

@app.route('/metadata', methods=['POST'])
def add_or_update_nft_metadata():
    try:
        submitted_metadata = request.json
    except:
        return jsonify({'error': 'Invalid JSON data.'}), 400

    if not submitted_metadata.get('id'):
        return jsonify({'error': 'Missing NFT ID'}), 400

    existing_metadata = load_nft_metadata()
    
    if isinstance(existing_metadata, dict):
        existing_metadata[submitted_metadata['id']] = submitted_metadata
        success = save_nft_metadata(existing_metadata)
        
        if success:
            return jsonify({'message': 'NFT metadata added/updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to save NFT metadata to file.'}), 500
    else:
        return jsonify({'error': 'Unable to process NFT metadata.'}), 500

@app.route('/metadata/<string:nft_id>', methods=['DELETE'])
def remove_nft_metadata(nft_id):
    metadata_repository = load_nft_metadata()
    
    if isinstance(metadata_repository, dict):
        if nft_id in metadata_repository:
            del metadata_repository[nft_id]
            success = save_nft_metadata(metadata_repository)
            
            if success:
                return jsonify({'message': f'NFT metadata for ID {nft_id} removed successfully'}), 200
            else:
                return jsonify({'error': 'Failed to save changes to NFT metadata file.'}), 500
        else:
            return jsonify({'error': 'NFT ID not found'}), 404
    else:
        return jsonify({'error': 'Unable to process NFT metadata.'}), 500

if __name__ == '__main__':
    app.run(debug=True)