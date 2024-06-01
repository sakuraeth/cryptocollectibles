import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

app = Flask(__name__)

NFT_METADATA_DIR = os.getenv("NFT_METADATA_DIR", "nft_metadata")

os.makedirs(NFT_METADATA_DIR, exist_ok=True)

@lru_cache(maxsize=128)
def get_metadata_path(token_id):
    return os.path.join(NFT_METADATA_DIR, f"{token_id}.json")

@app.route('/metadata/<token_id>', methods=['GET'])
def get_metadata(token_id):
    metadata_path = get_metadata_path(token_id)
    try:
        with open(metadata_path, 'r') as file:
            metadata = json.load(file)
        return jsonify(metadata), 200
    except FileNotFoundError:
        return jsonify({"error": "Metadata not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to decode metadata JSON"}), 500

@app.route('/metadata/<token_id>', methods=['POST'])
def add_or_update_metadata(token_id):
    metadata_path = get_metadata_path(token_id)
    new_metadata = request.json

    if new_metadata is None:
        return jsonify({"error": "Invalid or missing JSON in request"}), 400

    try:
        with open(metadata_path, 'w') as file:
            json.dump(new_metadata, file)
        get_metadata_path.cache_clear() 
        return jsonify({"message": "Metadata saved successfully"}), 200
    except TypeError as e:
        return jsonify({"error": f"Invalid data format: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)