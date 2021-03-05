import datetime
from datetimerange import DateTimeRange
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

def haversine(start, end):
    query = "SELECT Latitude, Longitude FROM STATION WHERE station_id = '{}'". format(start)
    cur.execute(query)
    a = cur.fetchone()
    query = "SELECT Latitude, Longitude FROM STATION WHERE station_id = '{}'". format(end)
    cur.execute(query)
    b = cur.fetchone()

    lat1, lon1 = a[0], a[1]
    lat2, lon2 = b[0], b[1] 
     
    lon1, lon2 = radians(lon1), radians(lon2)
    lat1, lat2 = radians(lat1), radians(lat2)
      
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 

    return round(c*r,2)
    
    
def get_time(a, path, s_time, speed):

    count = 0
    t_distance = 0
    station_time = datetime.timedelta(minutes = 10)
    path = path.split("#")

    for i in range(0,len(path)-1):
        distance = haversine("S_ID_"+path[i], "S_ID_"+path[i+1])
        t_distance = t_distance + distance
        count += 1

        if path[i+1] == a:
            break
        
    s_time = s_time.split("-")
    init_time= datetime.datetime(int(s_time[0]), int(s_time[1]), int(s_time[2]), int(s_time[3]), int(s_time[4]))
    time_delta = datetime.timedelta(minutes = t_distance/speed*60)  + (station_time*count)
    time = init_time + time_delta
    
    return time

def point_path_intersection(points, data):
    p = points[0]
    a = get_time(p, data[0][2], data[0][3], data[0][6])
    b = get_time(p, data[1][2], data[1][3], data[1][6])

    if a-b < datetime.timedelta(minutes = 5):
        print("cant schedule ")
    else:
        print("schedule")
                

def long_path_intersection(points, data):
 
    intersecting = "#".join(points)

    joining_points = [points[0], points[-1]]
    t11 = get_time(joining_points[0], data[0][2], data[0][3], data[0][6])
    t12 = get_time(joining_points[-1], data[0][2], data[0][3], data[0][6])
    t21 = get_time(joining_points[0], data[1][2], data[1][3], data[1][6])
    t22 = get_time(joining_points[-1], data[1][2], data[1][3], data[1][6])
    
    if intersecting in data[0][2] and intersecting in data[1][2]:                                                           #unidirectional       
        a = DateTimeRange(start_datetime=t11, end_datetime=t12, start_time_format='%Y-%m-%d %H:%M:%S%z', end_time_format='%Y-%m-%d %H:%M:%S%z')
        b = DateTimeRange(start_datetime=t21, end_datetime=t22, start_time_format='%Y-%m-%d %H:%M:%S%z', end_time_format='%Y-%m-%d %H:%M:%S%z')
        print(a,b)
        if a.is_intersection(b):
            if t11-t21 < datetime.timedelta(minutes = 12) or t12-t22 < datetime.timedelta(minutes = 12):
                print("you can't")
            else:
                print("you can")
        else:
            print("you can")
    else:

        a = DateTimeRange(start_datetime=t11, end_datetime=t12, start_time_format='%Y-%m-%d %H:%M:%S%z', end_time_format='%Y-%m-%d %H:%M:%S%z')
        b = DateTimeRange(start_datetime=t22, end_datetime=t21, start_time_format='%Y-%m-%d %H:%M:%S%z', end_time_format='%Y-%m-%d %H:%M:%S%z')
        print(a,b)
        if a.is_intersection(b):
            print("Never ever possible")
        else:
            print("Possible")
    
    
def intersection_no(data):
    points = []
    for i in data[0][2].split("#"):
        for j in data[1][2].split("#"):
            if  i == j:
                points.append(i)
    if len(points) == 1:
        a = point_path_intersection(points, data)
    else:
        a = long_path_intersection(points, data)
    
    return a


def receiver(Start, End, Path, Start_t, End_t, D, S):
    user_data = [Start, End, Path, Start_t, End_t, D, S]
    query = "Select  * from Schedule"
    cur.execute(query)
    rs = cur.fetchall()
    flag = 0
    for i in rs:
        data = [list(i), user_data]
        a = intersection_no(data)
        if a == False:
            flag = 1
            break
    if flag == 1:
        print("Found an interupption")


