import mysql.connector
import mainalgo

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "tiger",
    database = "Project"
    )

if conn.is_connected() == True:
    cur = conn.cursor()

def new_train_schedule():
    Start_Sta = input("Enter the starting station :")
    End_Sta = input("Enter the ending station :")
    Path_ID = input("Enter the path ID :")
    Start_Time = input("Enter the departure time :")
    End_Time = input("Entet the arrival time :")
    Distance = int(input("Enter the total distance of journey :"))
    Speed = int(input("Enter the speed :"))
    mainalgo.receiver(Start_Sta, End_Sta, Path_ID, Start_Time, End_Time, Distance, Speed)
    
    
    
new_train_schedule()