"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the Jackson family object with 3 members
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET all members
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# GET single member
@app.route('/members/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

# POST new member
@app.route('/members', methods=['POST'])
def create_member():
    member = request.json
    if member:
        new_member = jackson_family.add_member(member)
        return jsonify(new_member), 200
    return jsonify({"error": "Invalid member data"}), 400

# DELETE member
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_single_member(id):
    deleted_member = jackson_family.delete_member(id)
    if deleted_member:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Member not found"}), 404

# Run server
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
