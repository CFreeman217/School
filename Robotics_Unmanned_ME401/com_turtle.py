#!/usr/bin/env python

import rospy, time, csv, os, datetime
from beginner_tutorials.msg import Position
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import sys, select
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

WAFFLE_MAX_LIN_VEL = 0.26
WAFFLE_MAX_ANG_VEL = 1.82

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1

msg = """
Command and control. 

Turtlebot commands given: 

Forward @ 1.5 m/s for 5 seconds
Right turn @ 0.15 rad/s for 2 seconds
Forward @ 1.5 m/s for 5 seconds

space key, s : force stop

CTRL-C to quit
"""

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

def getKey():
    if os.name == 'nt':
      return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop )
    elif input < output:
        output = max( input, output - slop )
    else:
        output = input

    return output

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
    if turtlebot3_model == "burger":
      vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
    elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)
    else:
      vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)

    return vel

def checkAngularLimitVelocity(vel):
    if turtlebot3_model == "burger":
      vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
    elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)
    else:
      vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)

    return vel

if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)


    rospy.init_node('turtlebot3_teleop')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    turtlebot3_model = rospy.get_param("model", "burger")

    status = 0
    target_linear_vel   = 0.0
    target_angular_vel  = 0.0
    control_linear_vel  = 0.0
    control_angular_vel = 0.0
    start = time.time()
    try:
        print msg

        # this will constitute the header for the columns in the csv file, this is simply because
        # it is the first line which will be written
        myData = ["pos_x, pos_y, pos_z, roll, pitch, yaw, tgt_lin, ctrl_lin, tgt_ang, ctrl_ang"]

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
        time.sleep(1)
        rospy.Subscriber('/eul', Position, callback_ori)
        # create a subscriber to the odometry node, this node is created
        # automatically in the turtlebot3 simulation, it contains the
        # position in 3 dimensions in the global frame, the angular
        # position is stored as quaternion and has to be converted to
        # euler angles to be "readable"
        rospy.Subscriber('/odom', Odometry, callback_pos)
        # create a node, the name is arbitrary
        # rospy.init_node('PositionNode', anonymous=True)
        # rospy.rate(100) sets the update rate at 100Hz when using the
        # sleep() function which will be called to control timing in
        # the main while loop, this is hard to read at 100Hz, try
        # reducing the value of the refresh rate to make it easier
        # to read the message printed to the console
        rate = rospy.Rate(100) # 100Hz update rate
        # it seems like waiting for a second makes things run smoothly
        time.sleep(1) # pause for 1 second
        # # putting code inside of this while statement seems to make
        # # ctrl+c killing of programs work more smoothly, if you don't
        # # include this, scripts will hang and you will have to
        # # restart gazebo (gross)


        while(1):
            key = getKey()
            now = time.time()
            elapsed = now - start
            if elapsed < 5.0:
                target_linear_vel = 1.5
                target_angular_vel = 0.0
            elif elapsed < 7.0:
                target_linear_vel = 0.0
                target_angular_vel = -.15
            elif elapsed < 12.0:
                target_linear_vel = 1.5
                target_angular_vel = 0.0
            else:
                target_linear_vel = 0.0
                target_angular_vel = 0.0
                break

            if key == ' ' or key == 's' :
                target_linear_vel   = 0.0
                control_linear_vel  = 0.0
                target_angular_vel  = 0.0
                control_angular_vel = 0.0
                # print 'STOPPPED'
                # print vels(target_linear_vel, target_angular_vel)
            else:
                if (key == '\x03'):
                    break


            # this represents the "real" data which we want to write to the file
            myData = [position.linear.x,position.linear.y,position.linear.z,position.angular.roll,position.angular.pitch,position.angular.yaw,target_linear_vel, control_linear_vel, target_angular_vel, control_angular_vel]
            # print status message
            # print "write to file"
            # same as the code block above
            # myFile = open(fileName, 'a')
            myFile = open(fileName, 'a')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerow(myData)

            # print status message
            print "write complete, waiting"
            rate.sleep()
            twist = Twist()

            control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
            twist.linear.x = control_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0

            control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel

            pub.publish(twist)

    except:
        print "ERROR"

    finally:
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)