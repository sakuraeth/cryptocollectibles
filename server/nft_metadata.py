import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

METADATA_FILE_PATH = os.getenv('METADATA_FILE', 'metadata.json')

def read_nft_metadata_from_file():
    try:
        with open(METADATA_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        # Handles the case where the file content is not valid JSON
        return {'error': 'Failed to decode JSON data.'}

def write_nft_metadata_to_file(metadata):
    try:
        with open(METADATA_FILE_PATH, 'w') as file:
            json.dump(metadata, file, indent=4)
    except IOError:
        return False
    return True

@app.route('/metadata', methods=['GET'])
def retrieve_all_metadata():
    metadata = read_nft_metadata_from_file()
    
    if isinstance(metadata, dict):
        return jsonify(metadata)
    else:
        return jsonify({'error': 'Unable to retrieve NFT metadata.'}), 500

@app.route('/metadata/<string:nft_id>', methods=['GET'])
def retrieve_metadata_by_id(nft_id):
    metadata = read_nft_metadata_from_file()

    if isinstance(metadata, dict):
        return jsonify(metadata.get(nft_id, {}))
    else:
        return jsonify({'error': 'Unable to retrieve NFT metadata.'}), 500

@app.route('/metadata', methods=['POST'])
def add_or_update_metadata():
    try:
        incoming_metadata = request.json
    except:
        return jsonify({'error': 'Invalid JSON data.'}), 400

    if not incoming_metadata.get('id'):
        return jsonify({'error': 'Missing NFT ID'}), 400

    all_metadata = read_nft_metadata_from_file()
    
    if isinstance(all_metadata, dict):
        all_metadata[incoming_metadata['id']] = incoming_metadata
        success = write_nft_metadata_to_file(all_metadata)
        
        if success:
            return jsonify({'message': 'NFT metadata added/updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to write NFT metadata to file.'}), 500
    else:
        return jsonify({'error': 'Unable to process NFT metadata.'}), 500

@app.route('/metadata/<string:nft_id>', methods=['DELETE'])
def delete_metadata(nft_id):
    all_metadata = read_nft_metadata_from_file()
    
    if isinstance(all_metadata, dict):
        if nft_id in all_metadata:
            del all_metadata[nft_id]
            success = write_nft_metadata_to_file(all_metadata)
            
            if success:
                return jsonify({'message': f'NFT metadata for ID {nft_id} deleted successfully'}), 200
            else:
                return jsonify({'error': 'Failed to write changes to NFT metadata file.'}), 500
        else:
            return jsonify({'error': 'NFT ID not found'}), 404
    else:
        return jsonify({'error': 'Unable to process NFT metadata.'}), 500

if __name__ == '__main__':
    app.run(debug=True)