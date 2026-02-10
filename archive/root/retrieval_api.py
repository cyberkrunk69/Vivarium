from flask import Flask, request, jsonify
import requests
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

# Secured the API endpoint
@app.route('/retrieve', methods=['GET'])
@auth.login_required
def retrieve():
    return jsonify({'data': 'Retrieved data'})