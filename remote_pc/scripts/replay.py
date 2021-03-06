#!/usr/bin/env python
#Publish data from database to a ROS publisher
import rospy
import psycopg2
import psycopg2.extras
import sys
import time
from std_msgs.msg import String
from datetime import datetime
from datetime import timedelta

conn_string = "host='localhost' dbname='example_db' user='example_user' password='example_user'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
lastTime = datetime(2018, 2, 16, 13, 25, 28, 688503)
interval = timedelta(seconds = 100)
timeConv = '%Y-%m-%d %H:%M:%S.%f'


def dbstuff():
	conn_string = "host='localhost' dbname='example_db' user='example_user' password='example_user'"
	print "Connecting to database\n	->%s" % (conn_string)
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	work_mem = 2048
	cursor.execute('SET work_mem TO %s', (work_mem,))
	cursor.execute('SHOW work_mem')
	memory = cursor.fetchone()
	print "Value: ", memory[0]
	print "Row:	", memory


def talker():
    pub = rospy.Publisher('replay', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(5) # 100hz

    sql = "SELECT timestamp FROM lidar_data WHERE timestamp >= '"+str(lastTime)+"' AND timestamp < '"+str(lastTime + interval)+"'";
    cursor.execute(sql)
    timeArr = cursor.fetchall()

    print(timeArr)
    print(sql)
    print(len(timeArr))

    sql = "SELECT lidar FROM lidar_data WHERE timestamp >= '"+str(lastTime)+"' AND timestamp < '"+str(lastTime + interval)+"'";
    cursor.execute(sql)
    lidarData = cursor.fetchall()[0][0]

    i = 0
    data = str(time.mktime(newTime.timetuple()))[:-1]+str((newTime.microsecond))
    while i < len(timeArr):
        newTime = datetime.strptime(str(timeArr[i][0]), timeConv)
        messageStr = "[" + str(lidarData[0])
        for j in range(1, len(lidarData)):
           messageStr += "," + str(lidarData[j])
        messageStr += "]"
        print(messageStr)
        pub.publish(messageStr)
		print("ok")
        rate.sleep()
	i += 1


if __name__ == '__main__':
    dbstuff()
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
