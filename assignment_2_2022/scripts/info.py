#! /usr/bin/env python

"""
.. module::info
   :platform: Unix
   :synopsis: This module contains the code for the node C. 
    This subscribes to the topic /Position_velocity and prints the distance 
    between the desired position and the current position and the average speed. 


.. moduleauthor:: Davide Pisano S4363394@studenti.unige.it

Subscriber:
  /odom

""" 

import rospy
import math
import time
from assignment_2_2022.msg import Position_vel

# initialize the frequency 
freq = 1.0

# initialize the last position printed 
last = 0

# call the  function for the position velocity info subscriber
def position_vel(msg):

    """
    This function is called when a message is received by the subscriber.
    It prints the distance between the desired position and the current position and the average speed.
    """

    global freq, last
	
    # compute the period in milliseconds
    period = (1.0/freq) * 1000
	
    # compute the current time in milliseconds 
    curr_time = time.time() * 1000
	
	
    if curr_time - last > period:
        	
        # initialize the desired position x,y given by the user
        des_x = rospy.get_param("des_pos_x")
        des_y = rospy.get_param("des_pos_y")
		
        # initialize the attual current position x,y 
        real_x = msg.x
        real_y = msg.y
		
        # compute the distance between the desidered position and the attual current position
        dist = math.dist([des_x, des_y], [real_x, real_y])
		
        # compute the average speed 
        average_speed = math.sqrt(msg.velX**2 + msg.velY**2)
		
        # print information (distance and average speed)
        print( "Difference between the desired position and the attual current position is: ", float(round(dist, 5)))
        print( "The average speed is: ", float(round(average_speed, 5)))
        print()
		
        # update last position
        last = curr_time
	

def main():

    """
    This function initializes the ROS node and creates the subscriber.
    */Position_velocity* is the topic where the client node publishes the custom message.
    The position and the linear velocity are passed as a nav_msgs/Odometry message.    
    """

    global frequency
	
    # initialize the node
    rospy.init_node('info')
	
    # get the publishing frequency 
    freq = rospy.get_param("frequency")

    # initialize the subscriber to give the position_velocity
    sub_pos = rospy.Subscriber("/Position_velocity", Position_vel, position_vel)
	
    # wait
    rospy.spin()
	
if __name__ == "__main__":
    main()	

