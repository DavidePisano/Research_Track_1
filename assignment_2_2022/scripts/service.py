#! /usr/bin/env python

"""
.. module::service
   :platform: Unix
   :synopsis:This module contains the code for the service node B. 
    This creates a service that returns the number of goals cancelled and reached. 
    It also subscribes to the topic */reaching_goal/result* to get the status of the result 
    and increment the number of goals cancelled and reached.


.. moduleauthor:: Davide Pisano S4363394@studenti.unige.it

Subscriber:
  /reaching_goal/result

Service: 
  /service

""" 

import rospy
from assignment_2_2022.srv import goal_service, goal_response
import actionlib
import actionlib.msg
import assignment_2_2022.msg

# Initialize variables for count how much goal was cancelled (canc_goal) or reached (reached_goal)
canc_goal = 0;
reached_goal = 0;

# callback for result subscriber
def result(msg):
	
    """
    This function is called when a message is received by the subscriber. 
    It increments the number of goals cancelled and reached depending on the status of the result.
    Args:
        msg (PlanningActionResult): The message received by the subscriber. It contains the status of the result.
    """

    global canc_goal, reached_goal
	
    # get the status from the message
    status = msg.status.status
	
    # if status is 2, goal_service was preempted
    if status == 2:
        canc_goal += 1
    # if status is 3, goal_service was reached_goal
    elif status == 3:
        reached_goal += 1
		
# the service function, use for implement the service 
def data(req):

    """
    This function is called when the service is called. It returns the number of goals cancelled and reached.
    """

    global canc_goal, reached_goal
	
    # return the response of the service 
    return goal_response(reached_goal, canc_goal)

def main():

    """
    This function initializes the ROS node and and the subscriber and creates the service.
    */reaching_goal/result* is the topic where the action server publishes the status of the result.
    */service* is the service that returns the number of goals cancelled and reached.
    
    """
    # Initialize the node
    rospy.init_node('service')
	
    # create the service
    srv = rospy.Service('service', goal_service, data)
	
    # initialize the subscriber for the result of the goal_service
    sub_result = rospy.Subscriber('/reaching_goal/result', assignment_2_2022.msg.PlanningActionResult, result)
	
    # wait
    rospy.spin()
	
if __name__ == "__main__":
    main()

