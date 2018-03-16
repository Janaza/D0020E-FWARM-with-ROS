# D0020E - FWARM with ROS 
Follow the ROS tutorials for setting up a ROS workspace http://wiki.ros.org/ROS/Tutorials

Download our packages to the corresponding PC (the packages could also be ran on the same PC)
Download the package containing the lms1xx driver http://wiki.ros.org/LMS1xx
Build the packages (http://wiki.ros.org/ROS/Tutorials/BuildingPackages)

Set networking settings on the PC running the driver to be able to communicate with the LiDAR. For example in our case we used:

IP: 169.254.152.1

Subnet: \16

Gateway: 10.163.68.254

To start the talker node on the embeded pc first run the driver by running: roslaunch lms1xx LMS1xx.launch and rosrun lms1xx LMS1xx_node
then run our package: rosrun embeded_pc talker.py

On the remote PC set the enviorment variables $ROS_MASTER_URI and $ROS_IP to point to the embeded pc (more info http://wiki.ros.org/ROS/Tutorials/MultipleMachines) 
In our case we configured these variables to: 

$ROS_MASTER_URI='http://169.254.152.1:11311'

$ROS_IP=169.254.152.1

Don't forget to set the OS network settings to the same as on the embeded pc.

The HMI with livefeed and playback can now be run with: rosrun remote_pc HMIOO.py
To update the database with incoming LiDAR data run: rosrun remote_pc listener.py


