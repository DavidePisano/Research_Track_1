#!/usr/bin/env python

"""
.. module::input_user
   :platform: Unix
   :synopsis: This module contains the code for the client node A. 


.. moduleauthor:: Davide Pisano S4363394@studenti.unige.it

Subscriber:
  /odom

Publisher: 
  /Position_velocity

Action Client:
  /reaching_goal

""" 

import rospy
import actionlib
import actionlib.msg
import assignment_2_2022.msg
from std_srvs.srv import *
import sys
import select
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Twist
from assignment_2_2022.msg import Position_vel

# It creates a publisher to publish the custom message to the topic /Position_velocity and a subscriber to subscribe to the topic /odom and call the callback function when a message is received. 
# It also calls the action client. 

def publishVal(msg):
	
    """
    This function is called when a message is received by the subscriber.
    It creates the custom message and publishes it to the topic /Position_velocity.
    
    Args:
    msg (Odometry): The message received by the subscriber. It contains the position and the linear velocity of the robot.

    Return:
    none
    
    """

    # recall the global publisher as pub
    global pub
    
    # initialize the postion and the velocity from the message
    pos = msg.pose.pose.position
    velocity = msg.twist.twist.linear
	
    # Initialize a custom message
    pos_velox = Position_vel()
	
    # assign the parameters of the custom message (pos_velox)
    pos_velox.x = pos.x
    pos_velox.y = pos.y
    pos_velox.velX = velocity.x
    pos_velox.velY = velocity.y
	
    # Publish the custom message
    pub.publish(pos_velox)

def client():

    """
    This function creates the action client and sends the goal to the action server. 
    It also waits for the action server to be up and running.
    
    Args:
        None
    """
    
    # initialize the action client and wait that the server started
    client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)
    client.wait_for_server()
    
    while not rospy.is_shutdown():
        
        # Get in input the coordinates from the utent 
        position_X = input("Input target x: ")
        position_Y = input("Input target y: ")
        
        position_X = float(position_X)
        position_Y = float(position_Y)
    	
        # Create the goal_service position in coordinates x,y 
        goal_service = assignment_2_2022.msg.PlanningGoal()
        goal_service.target_pose.pose.position.x = position_X
        goal_service.target_pose.pose.position.y = position_Y
    
        # Send the goal_service position to the server
        client.send_goal(goal_service)
        
        # literal character for the stop instruction for the robot 
        stop_btn = input("If you want to stop the robot press 's': ")
           
	# check if the stop input is correct 
        if (stop_btn == "s"):
	    # delete the goal_service
            print("The goal_service position has been deleted!")
            client.cancel_goal()

def main():

    """
    This function initializes the ROS node, creates the publisher and the subscriber and calls the action client.
    
    */odom* is the topic where the robot publishes its position and linear velocity.
    */Position_velocity* is the topic where the client node publishes the custom message.
    
    The position and the linear velocity are passed as a nav_msgs/Odometry message.
    """

    # initialize the node 
    rospy.init_node('input_user')
    
    # create a global publisher, call as pub
    global pub
    
    # initialize the publisher to send a msg 
    pub = rospy.Publisher("/Position_velocity", Position_vel, queue_size = 1)
    
    # initialize the subscriber to get velocity and position
    sub_from_Odom=rospy.Subscriber("/odom", Odometry, publishVal)
    
    # Call the client function
    client()
      
if __name__ == '__main__':
    main()

