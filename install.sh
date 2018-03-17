#!/bin/bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
sudo apt-get update
sudo apt-get install ros-kinetic-desktop-full
source /opt/ros/kinetic/setup.bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
git clone https://github.com/Janaza/D0020E-FWARM-with-ROS .
sudo chmod +x ~/catkin_ws/src/remote_pc/scripts/HMIOO.py
sudo chmod +x ~/catkin_ws/src/remote_pc/scripts/listener.py 
sudo chmod +x ~/catkin_ws/src/remote_pc/scripts/getFromDB.py
sudo chmod +x ~/catkin_ws/src/embeded_pc/scripts/talker.py 
cd ~/catkin_ws/ 
catkin_make
source ~/catkin_ws/devel/setup.bash
sudo apt-get install ros-kinetic-lms1xx
sudo apt-get install rosbash
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc 
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc

printf "\n\n"
printf "ROS and packages have been installed. Don't forget to set proper network settings on both embeded pc and remote pc. \nIP/subnet/gateway should all be set as they are on the LMS151 LiDAR."
printf "You should also export the variables ROS_MASTER_URI='http://EMBEDED_PC_IP:11311' and ROS_IP=EMBEDED_PC_IP"
printf " on the remote pc!\n"

