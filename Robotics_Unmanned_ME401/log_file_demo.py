#!/usr/bin/env python

# Author:       Shawn Herrington
# Data:         1/30/2019
# Purpose:      mwe for logging data to a file
# Depends:      You will need to create a directory called "logfiles" somewhere and
#		and make sure that the code points to the directory you created, see
#		line 39
# Details:	filename is todays data and the current time
#

# ------------------
# ATTENTION STUDENTS
# ------------------

# this file contains an example of how to write information to a file, you are expected to borrow
# parts from this file to open/close a log file and write information into it, there are many ways
# to log information in ROS (rosbag) and python (google it), the method used here was chosen
# arbitrarily, feel free to try other methods if you want to

# ----------------
# END INSTRUCTIONS
# ----------------

import rospy, time, csv, os, datetime

if __name__ == "__main__":

	try:

		# create a node
		rospy.init_node('LogFileNode', anonymous=True)

		# create a rate object for timing, the argument is in Hz
		r = rospy.Rate(100) #HZ

		# this will constitute the header for the columns in the csv file, this is simply because
		# it is the first line which will be written
		myData = ["var1,var2"]

		# the following code creates a base filename containing the data and time
		fileNameBase = "./scripts/log_files/" + datetime.datetime.now().strftime("%b_%d_%H_%M")

		# the end of the file will always be ".csv"
		fileNameSuffix = ".csv"

		# this number will only be used if the filename already exists
		num = 1

		# compose the complete filename from the component parts, don't use num yet
		fileName = fileNameBase + fileNameSuffix

		# while loop will execute until we have a unique filename
		while os.path.isfile(fileName):
			# if the filename is not unique, add a number to the end of it
			fileName = fileNameBase + "_" + str(num) + fileNameSuffix
			# increments the number in case the filename is still not unique
			num = num + 1

		# now that we have a good filename open it, the "a" option is "append", the default
		# behavior is to overwrite the file each time the file is opened, in this case we
		# want to keep the existing file but add a new line each time we open so we use
		# the append option
		myFile = open(fileName, 'a')
		# using the newly create file object
		with myFile:
			# create a csv writer object which is attached to the file object
			writer = csv.writer(myFile)
			# write a single row, there are other write functions which can be used,
			# since this one only writes a single row it automatically adds a newline
			# to the end of the data
			writer.writerow(myData)

		while not rospy.is_shutdown():

			# this represents the "real" data which we want to write to the file
			myData = [1,2]

			# print status message
			print "write to file"

			# same as the code block above
			myFile = open(fileName, 'a')
			with myFile:
				writer = csv.writer(myFile)
				writer.writerow(myData)

			# print status message
			print "write complete, waiting"

			r.sleep()

	except rospy.ROSInterruptException:

		pass
