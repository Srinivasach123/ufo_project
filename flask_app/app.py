from flask import Flask, jsonify, request
import sqlite3
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
DATABASE = '../ufo_sightings.db'


# Get all UFO sightings from the database
def get_all_sightings():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM sightings")
    data = c.fetchall()
    conn.close()
    return data

# Get UFO sightings by location
def get_sightings_by_location(location):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM sightings WHERE City=? or State=?", (location,location,))
    data = c.fetchall()
    conn.close()
    return data

# Get UFO sightings by date of occurrence
def get_sightings_by_date(date_of_occurrence):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM sightings WHERE Reported_Date=?", (date_of_occurrence,))
    data = c.fetchall()
    conn.close()
    return data

# Endpoint to get all UFO sightings
@app.route('/api/sightings', methods=['GET'])
def get_all_sightings_api():
    sightings = get_all_sightings()
    return jsonify(sightings)

# Endpoint to get UFO sightings by location
@app.route('/api/sightings/location/<string:location>', methods=['GET'])
def get_sightings_by_location_api(location):
    sightings = get_sightings_by_location(location)
    return jsonify(sightings)

# Endpoint to get UFO sightings by date of occurrence
@app.route('/api/sightings/date/<string:day>/<string:month>/<string:year>', methods=['GET'])
def get_sightings_by_date_api(day,month,year):
    date_of_occurrence = f"{day}/{month}/{year}"
    sightings = get_sightings_by_date(date_of_occurrence)
    return jsonify(sightings)

if __name__ == '__main__':
    
    app.run(debug=True)
