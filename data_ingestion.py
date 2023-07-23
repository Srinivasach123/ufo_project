import os
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

DB_PATH  = 'ufo_sightings.db'


def check_file_exists(file_path):
    if os.path.exists(file_path):
        print(f"The file '{file_path}' exists.")
    else:
        print(f"The file '{file_path}' does not exist.")

def get_last_six_months():
    current_date = datetime.today()
    last_six_months = [current_date.strftime("%Y%m")]
    for i in range(6):
        last_month_date = current_date.replace(day=1) - timedelta(days=1)
        last_six_months.append(last_month_date.strftime("%Y%m"))
        current_date = last_month_date
    return last_six_months[::-1]

def parse_html_content(html_content):
    # Parse the HTML content using BeautifulSoup
    #print(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the rows in the table
    rows = soup.find_all('tr')

    # Create a list to store the extracted data
    sightings_list = []
    for row in rows[1:]:  # Skip the header row (index 0)
        cells = row.find_all('td')
        #print(cells, len(cells))
        if len(cells)%9 == 0:  # Ensure all cells are present
            sighting = {
                'Date': cells[0].text,
                'City': cells[1].text,
                'State': cells[2].text,
                'Country': cells[3].text,
                'Description': cells[4].text,
                'Duration': cells[5].text,
                'Additional_Info': cells[6].text,
                'Reported_Date': cells[7].text,
                'Observed': cells[8].text
            }
            sightings_list.append(sighting)

    return sightings_list

# Function to fetch UFO sightings data from the National UFO Reporting Center website
def fetch_ufo_sightings(month):
    print(f"Inserting data for month {month}")
    url = f"http://www.nuforc.org/webreports/ndxe{month}.html"  # URL for the data feed of the last 6 months
    print(url)
    response = requests.get(url)
    data = response.text
    ufo_sightings_list = parse_html_content(data)
    print(ufo_sightings_list)
    return ufo_sightings_list

def create_or_connect_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
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
    ''')
    conn.commit()
    return conn

# Function to insert UFO sightings into the database
def insert_or_update_sightings(conn, sightings_data):
    cursor = conn.cursor()
    for sighting in sightings_data:
        date = sighting['Date']
        city = sighting['City']
        cursor.execute('SELECT * FROM sightings WHERE Date=? AND City=?', (date, city))
        existing_sighting = cursor.fetchone()
        if existing_sighting:
            cursor.execute('''
                UPDATE sightings SET
                State=?, Country=?, Description=?, Duration=?, Additional_Info=?, Reported_Date=?, Observed=?
                WHERE Date=? AND City=?
            ''', (
                sighting['State'], sighting['Country'], sighting['Description'], sighting['Duration'],
                sighting['Additional_Info'], sighting['Reported_Date'], sighting['Observed'],
                sighting['Date'], sighting['City']
            ))
        else:
            cursor.execute('''
                INSERT INTO sightings (Date, City, State, Country, Description, Duration, Additional_Info, Reported_Date, Observed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sighting['Date'], sighting['City'], sighting['State'], sighting['Country'], sighting['Description'],
                sighting['Duration'], sighting['Additional_Info'], sighting['Reported_Date'], sighting['Observed']
            ))
    conn.commit()

if __name__ == '__main__':
    # Fetch UFO sightings data from the National UFO Reporting Center
    months = []
    if check_file_exists:
        months = get_last_six_months()
        print("Inserting last six months of data")
    else:
        
        curr = datetime.now()
        months = [curr.strftime("%Y%m")]
        print(f"Inserting Today's {curr.date()} data")
    sightings_data = []
    for month in months:
            sightings_data+=fetch_ufo_sightings(month)

    
    # Connect to the database (or create one if it doesn't exist)
    conn = create_or_connect_database()
    
    # Insert UFO sightings into the database
    insert_or_update_sightings(conn, sightings_data)
    # Close the database connection
    conn.close()
