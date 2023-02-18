#! /usr/bin/python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


def fb_callback(feedback):
    rospy.loginfo(feedback)


def move_base_client():
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rate = rospy.Rate(5)

    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = -1.857940765424243
    goal.target_pose.pose.position.y = -0.5539458581619578
    goal.target_pose.pose.position.z = 0.0

    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = -1.0
    goal.target_pose.pose.orientation.w = 0.03619453412488009

    rospy.loginfo(f"Sending Goal: {goal}")

    client.send_goal(goal, feedback_cb=fb_callback)

    while (state_result := client.get_state()) < 2:
        rate.sleep()

    if state_result == 3:
        rospy.logwarn(f"Action Done. State Result : {client.get_result()}")
    else:
        rospy.logerr(f"Something went wrong, State Result : {state_result}")


if __name__ == '__main__':
    try:
        rospy.init_node("move_base_client")
        move_base_client()
    except rospy.ROSInterruptException:
        print("Program interrupted before completion")