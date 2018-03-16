#!/usr/bin/python
#This is the HMI, 
from Tkinter import *
import Tkinter as tk
import math
import random
import rospy
from std_msgs.msg import String
import psycopg2
import psycopg2.extras
import sys
import time
from datetime import datetime
from datetime import timedelta

master = tk.Tk()
height = 900
width = 900
master.resizable(False,False)
w = Canvas(master, width=width, height=height)
w.pack()
newarr = []
gridSize = 10

dotSize = 4

replayVar = True
closeDistance = 51.000
closeDistance_initValue = 51.000
closeAngleInt = 0

conn_string = "host='localhost' dbname='testdb' user='willow' password='willow'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
lastTime = datetime(2018, 3, 8, 17, 55, 8, 1)
print(chr(27) + "[2J") #clear terminal
interval = timedelta(seconds = 1000)#1000
timeConv = '%Y-%m-%d %H:%M:%S.%f'

if (int(input("input 1 for database playback, 0 for livefeed:  "))==1):
	replayVar=True
else:
	replayVar=False

def dbstuff():
	conn_string = "host='localhost' dbname='testdb' user='willow' password='willow'"
	print "Connecting to database\n	->%s" % (conn_string)
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	work_mem = 2048
	cursor.execute('SET work_mem TO %s', (work_mem,))
	cursor.execute('SHOW work_mem')
	memory = cursor.fetchone()
	print "Value: ", memory[0]
	print "Row:	", memory


def callback(msg):
    global newarr
    newarr = eval('['+msg.data[33:-2]+']')


#Grid
def drawGrid():
    for i in range(0, gridSize):
        w.create_line(0, height / gridSize * i, width, height / gridSize * i)
        w.create_line(width / gridSize * i, 0, width / gridSize * i, height)

    w.create_oval(width / 2 - 10, height / 2 - 10, height / 2 + 10, height / 2 + 10, fill="blue")
distText = str(0.0)
def onObjectClick(distance):
    #Printa avstand till objekt
    print "Distance: " + str(distance) + " meters"







def draw(msg):
    dist = 100
    i=0

    for degree in range(135, (135+len(msg)), 1): #405
         rad = math.radians(degree)
         dist =  float(msg[-i]) * height * 10 / 50 / 2
         i += 1
         if(dist > 5):
            obj1Id = w.create_oval(width / 2 - dotSize + math.cos(rad) * dist, height / 2 - dotSize + math.sin(rad) * dist, height / 2 + dotSize + math.cos(rad) * dist, height / 2 + dotSize + math.sin(rad) * dist, fill="red", tags="obj1tag")
            w.tag_bind(obj1Id, '<ButtonPress-1>',
            lambda event, distance=msg[-i]:
            onObjectClick(distance))




def HMIListener():
    rospy.init_node('HMIListener', anonymous=True)
    #ig = InfoGetter()
    dist = 100
    i = 33

    rospy.Subscriber('laser', String, callback)#or replay ig
    while not rospy.is_shutdown():
        w.delete('all')
        drawGrid()
        global newarr
        msg = newarr
        draw(msg)
        master.update()


def replay():
    while True:
        global lastTime
        global closeDistance
        global closeAngleInt


        #Select interval seconds of lidar data
        sql = "SELECT timestamp FROM hej WHERE timestamp >= '"+str(lastTime)+"' AND timestamp < '"+str(lastTime + interval)+"'";
        cursor.execute(sql)
        timeArr = (cursor.fetchall())

        sql = "SELECT lidar FROM hej WHERE timestamp >= '"+str(lastTime)+"' AND timestamp < '"+str(lastTime + interval)+"'";
        cursor.execute(sql)
        lidarData = cursor.fetchall()


        i = 0
        while i < len(timeArr):
            #
            #print timeArr[i][0]
            #
            newTime = datetime.strptime(str(timeArr[i][0]), timeConv)

            # Calculate wait time until next timestamp
            if(len(str((newTime.microsecond))) == 5): # Handles microsecond rounding error
                newS = str(time.mktime(newTime.timetuple()))[:-1]+"0"+str((newTime.microsecond))
            else:
                newS = str(time.mktime(newTime.timetuple()))[:-1]+str((newTime.microsecond))

            if(len(str((lastTime.microsecond))) == 5):
                lastS = str(time.mktime(lastTime.timetuple()))[:-1]+"0"+str((lastTime.microsecond))
            else:
                lastS = str(time.mktime(lastTime.timetuple()))[:-1]+str((lastTime.microsecond))
            waitTime = float(newS) - float(lastS)


            if(waitTime > 0):
                time.sleep(waitTime)

                messageStr = str(lidarData[i][0][0])

                for j in range(1, len(lidarData[i][0])):
                    messageStr += "," + str(lidarData[i][0][j])



                data = eval('['+messageStr+']')
                for findCloseDist in range (0, 271):
                    if (data[findCloseDist] < closeDistance) and (data[findCloseDist] > 0.5):
                        closeDistance = data[findCloseDist]
                        closeDistance_initValue = str(lidarData[0][-1][findCloseDist])
                        closeAngleInt = findCloseDist
                        print "Nearest object at: " + str(closeDistance)

                w.delete('all')
                drawGrid()
                draw(data)

                master.update()
            elif(waitTime == 0):
                print("\nStream ended")
                print("Database traversed from: 2018-03-08 17:55:08.396775" + "\nto:                      " + str(newTime))
                print ("\nFound nearest object at: "+ str(closeDistance))
                print ("Object moved from: " + str(lidarData[0][0][closeAngleInt]) + " meters to: "+ str(closeDistance)+" meters")
                print("\n\nRunning live feed")
                HMIListener()
                sys.exit(0)





            lastTime = newTime
            i += 1


if __name__ == '__main__':
    master.update()
    print replayVar
    if  replayVar:
	year = int(raw_input("\nInsert year (yyyy)"))
	month = int(raw_input("\nInsert month (MM)"))
	day = int(raw_input("\nInsert day (DD)"))
	hour = int(raw_input("\nInsert time of day in hours (hh)"))
	minu = int(raw_input("\nInsert minuets (mm)"))
	sec = raw_input("\nInsert seconds (SS) (or leave empty)")
	if (sec == ""):
		sec = 0
	else:
		sec = int(sec)	
	lastTime = datetime(year, month, day, hour, minu, sec, 0)
        print "Running playback from:  "+str(lastTime)
        replay()

    try:
        HMIListener()
    except rospy.ROSInterruptException:
        pass
