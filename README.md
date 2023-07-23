## Prerequistics
Install all dependent libraries using below command 

pip install -r requirements.txt

## Data Ingestion Process

we have data_ingestion.py file, that will be responsible for creating the database file "ufos.db"
It will create table "sightings" with following structure

CREATE TABLE IF NOT EXISTS sightings (
            Date TEXT,
            City TEXT,
            State TEXT,
            Country TEXT,
            Description TEXT,
            Duration TEXT,
            Additional_Info TEXT,
            Reported_Date TEXT,
            Observed TEXT,
            PRIMARY KEY (Date, City)
        )

This file is responsible to ingest data for last 6 months using api => http://www.nuforc.org/webreports/ndxe{month}.html where month will be replace with month for which data is ingested. 

If data is already present then it will ingest only new records for the current month.

Command: python data_ingestion.py

Result: A file named "ufo_sightings.db" will be created

We can setup this file to be executed daily using cron setup. 
0 1 * * * /usr/bin/python3 data_ingestion.py # this will execute this file at 1 am every day

Note: data_ingestion.py should be given correct absolute path.

## Flask Application


goto directory flask_app
Command: python app.py

Test the API:
You can test the API using tools like Postman or cURL. Here are some examples:

Get all sightings:
GET http://127.0.0.1:5000/api/sightings

response:
[
  [
    "1/31/23 19:49",
    "Gothenburg",
    "NE",
    "USA",
    "Fireball",
    "3 seconds",
    "Saw trailblazer that moves very rapid and moved with sparkling tail behind and then when it disappears, sparkling tail disappears",
    "3/6/23",
    ""
  ],
  [
    "1/31/23 19:15",
    "Sulphur Springs",
    "IN",
    "USA",
    "Circle",
    "10 seconds",
    "Fast spherical orange light",
    "3/6/23",
    "Yes"
  ],
  ...
]


Get sightings by location (e.g., "Tacoma"):
GET http://127.0.0.1:5000/api/sightings/location/Tacoma

response:
[
  [
    "2/28/23 21:12",
    "Tacoma",
    "WA",
    "USA",
    "Sphere",
    "30 seconds",
    "2 videos and 1 photo",
    "5/19/23",
    ""
  ],
  [
    "2/14/23 23:08",
    "Tacoma",
    "WA",
    "USA",
    "Orb",
    "I followed it for 10 min.",
    "A light that was coming and going the light would go away then re appear in a further location.",
    "3/6/23",
    ""
  ],
  ...
]


Get sightings by date of occurrence (e.g., "7/10/23")
GET http://127.0.0.1:5000/api/sightings/date/7/10/23

response:
[
  [
    "1/23/23 23:55",
    "Los Altos",
    "CA",
    "USA",
    "",
    "",
    "MADAR site 52 had spike on magnetometer but no compass MSV",
    "7/10/23",
    ""
  ],
  [
    "1/15/23 01:00",
    "Goshen",
    "CT",
    "USA",
    "Fireball",
    "10 seconds",
    "Static noises. What looked like a shooting star with blue and red tail came straight down and disappeared into farmland.",
    "7/10/23",
    ""
  ],
  ...
]

