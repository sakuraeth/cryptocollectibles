import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from functools import lru_cache,cached_property
from werkzeug.exceptions import HTTPException

load_dotenv()

app = Flask(__name__)

NFT_METADATA_DIR = os.getenv("NFT_METADATA_DIR", "nft_metadata")

os.makedirs(NFT_METADATA_DIR, exist_ok=True)

class MetadataCache:
    def __init__(self):
        self._cache = {}
        self.max_cache_size = 128
    
    def get(self, token_id):
        return self._cache.get(token_id)

    def set(self, token_id, metadata):
        if len(self._cache) >= self.max_cache_size:
            # Simple eviction policy, remove first added item
            next(iter(self._cache))
        self._cache[token_id] = metadata

metadata_cache = MetadataCache()

def get_metadata_path(token_id):
    return os.path.join(NFT_METADATA_DIR, f"{token_id}.json")

@app.route('/metadata/<token_id>', methods=['GET'])
def get_metadata(token_id):
    # First, attempt to retrieve from cache
    cached_metadata = metadata_cache.get(token_id)
    if cached_entry is not None:
        return jsonify(cached_metadata), 200
    
    metadata_path = get_metadata_path(token_id)
    try:
        with open(metadata_path, 'r') as file:
            metadata = json.load(file)
        metadata_cache.set(token_id, metadata)  # Cache the metadata after loading
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
        metadata_cache.set(token_id, new_metadata)  # Update cache upon saving
        return jsonify({"message": "Metadata saved successfully"}), 200
    except TypeError as e:
        return jsonify({"error": f"Invalid data format: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == '__main__':
    app.run(debug=True)