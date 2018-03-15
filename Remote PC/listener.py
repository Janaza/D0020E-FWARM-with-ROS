#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that listens to std_msgs/Strings published
## to the 'chatter' topic

import rospy
import psycopg2
#note that we have to import the Psycopg2 extras library!
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
