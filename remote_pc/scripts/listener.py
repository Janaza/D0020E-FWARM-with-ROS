#!/usr/bin/env python
#This script will listen on the data coming from Embeded PC and insert the data into a database
import rospy
import psycopg2
import psycopg2.extras
import sys
from std_msgs.msg import String

conn_string = "host='localhost' dbname='example_db' user='example_user' password='example_user'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def callback(data):
    SQL = "INSERT INTO lidar_data (timestamp, lidar) VALUES ("+data.data+");"
    cursor.execute(SQL)
    conn.commit()

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

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    print "lidar_data1"
    rospy.init_node('listener', anonymous=True)
    msg = rospy.Subscriber('laser', String, callback) #laserScanData
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    dbstuff()
    listener()
