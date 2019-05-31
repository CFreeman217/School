#!/usr/bin/env python

# Author:	Shawn Herrington
# Data:		1/30/2019
# Purpose:	MWE for logging 6 DOF position information for turtlebot3
#		gazebo simulation
# Depends:	1) ROS node which publishes topic "/eul" needs to be running
#		   in order for the orientation information to be valid
#		2) custom message "Position" which depends on custom messages
#		   "Linear" and "Angular" is used
# Details:	use of global variables is avoided
#

# ------------------
# ATTENTION STUDENTS
# ------------------

# Please read all of the following instructions carefully

# use this file as an example of how to pull in position data for the turtlebot
# simulation, this script is meant as a minimum working example which exposes
# the position information to the calling program, in this case the calling
# program is defined within '__main__' and it's primary function is to read
# in the position data and print that data to the screen

# in order to use this program you will need to ensure the dependencies are met
# 1) the quat_2_eul script has been provided, you should follow ROS
# tutorials on the creation of a package and then copy and paste this script
# into your newly created package (I named my package quat_2_eul), you will
# need to run this script using rosrun in order to get valid orientation
# information
# 2) you should also follow the ROS tutorial on creating a custom
# msg which can be found here:
# http://wiki.ros.org/ROS/Tutorials/CreatingMsgAndSrv
# using the custom message definitions shown below:

# create a file called "Position.msg"
# Linear linear
# Angular angular

# create a file called "Linear.msg"
# float32 x
# float32 y
# float32 z

# create a file called "Angular.msg"
# float32 roll
# float32 pitch
# float32 yaw

# ----------------
# END INSTRUCTIONS
# ----------------


import rospy, time, os, datetime
from beginner_tutorials.msg import Position
from nav_msgs.msg import Odometry


# declare a new object of type Position(), by declaring here outside of
# any function, the variable belongs to the global namespace and thus
# can be accessed by any of the functions within this file
# Position() is a custom message format consisting of 3 linear
# and 3 angular position states (x,y,z,roll,pitch,yaw)
position = Position()

# callback function for 3DOF linear position
def callback_pos(data):

	# the following line allows this function to access the variable
	# called position which exists in the global namespace, without
	# this statement using the global keyword, we will get an error
	# that the local variable "position" has been used prior to
	# being declared
	global position

	position.linear.x = data.pose.pose.position.x
	position.linear.y = data.pose.pose.position.y
	position.linear.z = data.pose.pose.position.z

# callback function for 3DOF rotation position
def callback_ori(data):

	global position

	position.angular.roll  = data.angular.roll
	position.angular.pitch = data.angular.pitch
	position.angular.yaw   = data.angular.yaw

if __name__ == '__main__':

	# to understand this type of programmatic flow control refer to help
	# pagges like the one here:
	# https://www.w3schools.com/python/python_try_except.asp
	# for our purposes, think of try/except blocks as fancy if statements,
	# the code inside of the the try block will exxecute as long as
	# exceptions (errors or special signals) occur at the system level,
	# the "signal" which most of you are probably familiar with is the =
	# signal sent by ctrl+c when you want to kill a program that is
	# running in the termainl, the reason try/except is used here is to
	# make ctrl+c kill the program is a predictable and nice manner
	try:

		time.sleep(1)

		# create subscriber to the euler angle node, inside this node
		# the quaternion to euler conversion and yaw wrapping is being
		# handled, the angular positions are also converted to degrees
		# from radians prior to being published
		rospy.Subscriber('/eul', Position, callback_ori)

		# create a subscriber to the odometry node, this node is created
		# automatically in the turtlebot3 simulation, it contains the
		# position in 3 dimensions in the global frame, the angular
		# position is stored as quaternion and has to be converted to
		# euler angles to be "readable"
		rospy.Subscriber('/odom', Odometry, callback_pos)

		# create a node, the name is arbitrary
		rospy.init_node('PositionNode', anonymous=True)

		# rospy.rate(100) sets the update rate at 100Hz when using the
		# sleep() function which will be called to control timing in
		# the main while loop, this is hard to read at 100Hz, try
		# reducing the value of the refresh rate to make it easier
		# to read the message printed to the console
		rate = rospy.Rate(100) # 100Hz update rate

		# it seems like waiting for a second makes things run smoothly
		time.sleep(1) # pause for 1 second

		# putting code inside of this while statement seems to make
		# ctrl+c killing of programs work more smoothly, if you don't
		# include this, scripts will hang and you will have to
		# restart gazebo (gross)
		while not rospy.is_shutdown():

			# NOTE "\t" in a string inserts a tab character to make the output look nicer
			print "Position"
			print "x: %.2f" % position.linear.x + "\ty:\t%.2f" % position.linear.y + "\tz:\t%.2f" % position.linear.z
			print "Orientation"
			print "roll: %.2f" % position.angular.roll + "\tpitch: %.2f" % position.angular.pitch + "\tyaw: %.2f" % position.angular.yaw

		rate.sleep()

	except rospy.ROSInterruptException:

		pass
