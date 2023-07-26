from dao.dao import Dao

class Controller:
    """
    Controller class for App
    """
    def __init__(self):
        self.dao = Dao()
    
    # Get all UFO sightings from the database
    def get_all_sightings(self):
        data = self.dao.execute("SELECT * FROM sightings")
        return data

    # Get UFO sightings by location
    def get_sightings_by_location(self, location):
        data = self.dao.execute("SELECT * FROM sightings WHERE City=? or State=?", (location,location,))
        return data

    # Get UFO sightings by date of occurrence
    def get_sightings_by_date(self, date_of_occurrence):
        data = self.dao.execute("SELECT * FROM sightings WHERE Reported_Date=?", (date_of_occurrence,))
        return data

