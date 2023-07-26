from flask import Flask, jsonify, request
import os
import requests
from bs4 import BeautifulSoup
from flask_swagger_ui import get_swaggerui_blueprint
import json 

from controllers.controller import Controller

app = Flask(__name__)
app_controller = Controller()


# Endpoint to get all UFO sightings
@app.route('/api/sightings', methods=['GET'])
def get_all_sightings_api():
    sightings = app_controller.get_all_sightings()
    return jsonify(sightings)

# Endpoint to get UFO sightings by location
@app.route('/api/sightings/location/<string:location>', methods=['GET'])
def get_sightings_by_location_api(location):
    sightings = app_controller.get_sightings_by_location(location)
    return jsonify(sightings)

# Endpoint to get UFO sightings by date of occurrence
@app.route('/api/   ', methods=['GET'])
def get_sightings_by_date_api(day,month,year):
    date_of_occurrence = f"{day}/{month}/{year}"
    sightings = app_controller.get_sightings_by_date(date_of_occurrence)
    return jsonify(sightings)

# Configure Swagger UI
SWAGGER_URL = '/swagger'
API_URL = 'http://127.0.0.1:5000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "SightingAPI"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))


if __name__ == '__main__':
    
    app.run(debug=True)
