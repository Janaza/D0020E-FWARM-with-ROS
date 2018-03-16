#!/usr/bin/env python

import datetime
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

dataarr = []

def callback(data):
	global dataarr
	#Pick ranges from LaserScan
	dataarr = data.ranges

def talker():
    hz = 22
    n = 0
    global dataarr
    pub = rospy.Publisher('laser', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(hz)
    rospy.loginfo("Node started")
    while not rospy.is_shutdown():
	msg = rospy.Subscriber('scan',LaserScan,callback)
	i = 0
	temp = []
	#removes every half degree from the scan
	while(i < len(dataarr)):
		temp.append(dataarr[i])
		i+=2
	sensor_data_str ="'" + str(datetime.datetime.utcnow()) + "' , '{" +str(temp)[1:-1]+ "}'"
	n+= 1
        pub.publish(sensor_data_str)
        rate.sleep()


if __name__ == '__main__':
    try:
	print "Attempting to start talker..."
        talker()

    except rospy.ROSInterruptException:
        pass
