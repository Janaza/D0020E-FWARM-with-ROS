# D0020E - FWARM with ROS
###### Installation
The file 'install.sh' can be used for installing ROS-kinetic, setting up a workspace (catkin_ws), installing the LMS1xx driver and our ROS packages. Make this file executable with chmod +x and run it in a terminal. The install.sh file assumes that bash is the default shell and that the computer is using apt-get package manager (as it is in a mint Ubuntu). Run this file on both the embeded and remote PC. 

If you don't want to run this file follow these instructions:  

1. Install ROS
1. Follow the ROS tutorials for setting up a ROS workspace http://wiki.ros.org/ROS/Tutorials
2. Download our packages to the corresponding PC (the packages could also be ran on the same PC)
3. Download the package containing the lms1xx driver http://wiki.ros.org/LMS1xx
4. Build the packages (http://wiki.ros.org/ROS/Tutorials/BuildingPackages)
--------
  
  
###### Network settings
Set networking settings on the PC running the driver to be able to communicate with the LiDAR.   
 For example in our case we used:
  
  IP: 169.254.152.1  
  Subnet: \16  
  Gateway: 10.163.68.254

These settings have to be configured on the remote PC aswell.
  
The network settings can also be edited on the LMS151 by using the SOPAS tool: https://www.sick.com/se/sv/sopas-engineering-tool-2018/p/p367244

--------

###### Running the talker node (embeded pc)
To start the talker node on the embeded pc first run the driver by running in terminal: 
 
 roslaunch lms1xx LMS1xx.launch host:=IP.OF.LIDAR.X  
 rosrun lms1xx LMS1xx_node  
 We can now run the talker:  
 rosrun embeded_pc talker.py
 
 In our case we set the argument host to 169.254.152.4  
 
--------

###### Running the listener, database and the HMI (remote pc)
Run the roscore (roscore in terminal)  
The HMI with livefeed and playback can now be run with:  
rosrun remote_pc HMIOO.py

To update the database with incoming LiDAR data run:  
rosrun remote_pc listener.py

--------
On the remote PC you must set the enviorment variables $ROS_MASTER_URI and $ROS_IP to point to the embeded pc.
 
 In our case we configured these variables to: 
 
 $ROS_MASTER_URI='http://169.254.152.1:11311'  
 $ROS_IP=169.254.152.1
 
For more info about these variables see the ROS documentation: http://wiki.ros.org/ROS/Tutorials/MultipleMachines



