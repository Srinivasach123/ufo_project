import sqlite3

class Dao:
    """
    Dao Layer for Database sql queries
    """
    
    def __init__(self):
        self.DATABASE = '../data/ufo_sightings.db'
    
    def execute(self, sql):
        conn = sqlite3.connect(self.DATABASE)
        c = conn.cursor()
        c.execute(sql)
        data = c.fetchall()
        conn.close()
        return data
    