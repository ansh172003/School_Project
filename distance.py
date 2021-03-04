from math import radians, cos, sin, asin, sqrt
import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "tiger",
    database = "project"
    )

if conn.is_connected() == True:
    cur = conn.cursor()
    
def get_data(start):
    query = "SELECT * FROM station where Station_Name = '{}'". format(start)
    cur.execute(query)
    rs = cur.fetchone()
    start_neighbour = rs[5].split(",")
    
    
def get_lat_lan(station):
    query = "SELECT * FROM station where Station_Name = '{}'". format(station)
    cur.execute(query)
    rs = cur.fetchone()
    data = [rs[3], rs[4]]
    return data

def Distance(a,b):

    lat1, lon1 = a[0], a[1]
    lat2, lon2 = b[0], b[1] 
     
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
     
    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
     
    return round(c*r,2)


def AstarAlgo(start,end):
    path = []
    
    

    
    
    
    
    
#Distance([28.64286, 77.2191],[28.36704, 79.43045])
