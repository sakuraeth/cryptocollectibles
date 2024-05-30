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

def write_nft_metadata_to_file(metadata):
    with open(METADATA_FILE_PATH, 'w') as file:
        json.dump(metadata, file, indent=4)

@app.route('/metadata', methods=['GET'])
def retrieve_all_metadata():
    metadata = read_nft_metadata_from_file()
    return jsonify(metadata)

@app.route('/metadata/<string:nft_id>', methods=['GET'])
def retrieve_metadata_by_id(nft_id):
    metadata = read_nft_metadata_from_file()
    return jsonify(metadata.get(nft_id, {}))

@app.route('/metadata', methods=['POST'])
def add_or_update_metadata():
    incoming_metadata = request.json
    if not incoming_metadata.get('id'):
        return jsonify({'error': 'Missing NFT ID'}), 400

    all_metadata = read_nft_metadata_from_file()
    all_metadata[incoming_metadata['id']] = incoming_metadata
    write_nft_metadata_to_file(all_metadata)

    return jsonify({'message': 'NFT metadata added/updated successfully'}), 200

@app.route('/metadata/<string:nft_id>', methods=['DELETE'])
def delete_metadata(nft_id):
    all_metadata = read_nft_metadata_from_file()
    if nft_id in all_metadata:
        del all_metadata[nft_id]
        write_nft_metadata_to_file(all_metadata)
        return jsonify({'message': f'NFT metadata for ID {nft_id} deleted successfully'}), 200
    else:
        return jsonify({'error': 'NFT ID not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)