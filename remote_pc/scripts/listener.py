#!/usr/bin/env python
#This script will listen on the data coming from Embeded PC and insert the data into a database
import rospy
import psycopg2
import psycopg2.extras
import sys
from std_msgs.msg import String

conn_string = "host='localhost' dbname='testdb' user='willow' password='willow'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

    SQL = "INSERT INTO hej (timestamp, lidar) VALUES ("+data.data+");"
    #data = (data.data, )
    #cursor.execute(SQL, data)
    cursor.execute(SQL)
    conn.commit()

    #cursor.execute("SELECT lidar FROM hej")
    #print cursor.fetchall()


def dbstuff():
	conn_string = "host='localhost' dbname='testdb' user='willow' password='willow'"
	#print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this query to perform queries
	# note that in this example we pass a cursor_factory argument that will
	# dictionary cursor so COLUMNS will be returned as a dictionary so we
	# can access columns by their name instead of index.
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	# tell postgres to use more work memory
	work_mem = 2048

	# by passing a tuple as the 2nd argument to the execution function our
	# %s string variable will get replaced with the order of variables in
	# the list. In this case there is only 1 variable.
	# Note that in python you specify a tuple with one item in it by placing
	# a comma after the first variable and surrounding it in parentheses.
	cursor.execute('SET work_mem TO %s', (work_mem,))

	# Then we get the work memory we just set -> we know we only want the
	# first ROW so we call fetchone.
	# then we use bracket access to get the FIRST value.
	# Note that even though we've returned the columns by name we can still
	# access columns by numeric index as well - which is really nice.
	cursor.execute('SHOW work_mem')

	# Call fetchone - which will fetch the first row returned from the
	# database.
	memory = cursor.fetchone()

	# access the column by numeric index:
	# even though we enabled columns by name I'm showing you this to
	# show that you can still access columns by index and iterate over them.
	print "Value: ", memory[0]

	# print the entire row
	print "Row:	", memory


def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    print "hej1"

    rospy.init_node('listener', anonymous=True)

    msg = rospy.Subscriber('laser', String, callback) #laserScanData


    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    print "Running3"
    dbstuff()
    listener()
