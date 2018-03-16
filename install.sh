#!/bin/bash
sudo apt-get install ros-kinetic-desktop-full
source /opt/ros/kinetic/setup.bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
git clone https://github.com/Janaza/D0020E-FWARM-with-ROS .
cd ~/catkin_ws/ 
catkin_make
sudo apt-get install ros-kinetic-lms1xx
source ~/catkin_ws/devel/setup.bash


echo "source /opt/ros/kinetic/setup.bash" >> .bashrc 
echo "source ~/catkin_ws/devel/setup.bash" >> .bashrc
printf "\n\n"
printf "ROS and packages have been installed. Don't forget to set proper network settings on both embeded pc and remote pc. \nIP/subnet/gateway should all be set as they are on the LMS151 LiDAR."
printf "You should also export the variables ROS_MASTER_URI='http://EMBEDED_PC_IP:11311' and ROS_IP=EMBEDED_PC_IP"
printf " on the remote pc!\n"

