#!/usr/bin/env python3
import math
import rospy
from std_msgs.msg import String
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

k_linear = float(input("\nEnter the constant for the linear velocity: \n"))
k_angular = float(input("Enter the constant for the angular velocity: \n"))
rospy.set_param("/linear_constant", k_linear)
rospy.set_param("/angular_constant", k_angular)


class Turtle:

        def __init__(self):

                rospy.init_node('turtle_controller', anonymous=True)
                self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
                self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
                self.pose = Pose()
                self.rate = rospy.Rate(10)

        def update_pose(self, data):
                self.pose = data
                self.pose.x = round(self.pose.x , 4)
                self.pose.y = round(self.pose.y , 4)

        def distance(self, goal_pose):
                return abs(math.sqrt(((goal_pose.x-self.pose.x)**2) + ((goal_pose.x-self.pose.x)**2)))
        
        def linear_velocity(self, goal_pose, k_linear):
                linear_velocity = k_linear * self.distance(goal_pose)
                return linear_velocity

        def angle(self, goal_pose):
                desired_angle = (- self.pose.theta) + math.atan2(goal_pose.y-self.pose.y , goal_pose.x-self.pose.x)
                return desired_angle

        def angular_velocity(self, goal_pose, k_angular):
                angular_velocity = k_angular * self.angle(goal_pose)
                return angular_velocity


        def go_to_goal(self):
                goal_pose = Pose()
                vel_msg = Twist()

                #goal_pose.x = float(input("Enter x-cordinate of the goal: "))
                #goal_pose.y = float(input("Enter y-cordinate of the goal: "))
                goal_pose.x = rospy.get_param("/x_coordinate")
                goal_pose.y = rospy.get_param("/y_coordinate")



                while self.distance(goal_pose) >= 0.01:
                        
                        vel_msg.linear.x = self.linear_velocity(goal_pose, k_linear)
                        vel_msg.linear.y = 0
                        vel_msg.linear.y = 0

                        vel_msg.angular.x =0 
                        vel_msg.angular.y =0
                        vel_msg.angular.z = self.angular_velocity(goal_pose, k_angular)
                        
                        self.velocity_publisher.publish(vel_msg)
                        self.rate.sleep()

                vel_msg.linear.x = 0
                vel_msg.angular.z = 0
                self.velocity_publisher.publish(vel_msg)
                print("Succesfully Reached the goal (",  goal_pose.x, ",", goal_pose.y, ")")
                rospy.spin()

if __name__ == '__main__':
        try:
                x= Turtle()
                x.go_to_goal()
        except rospy.ROSInterruptException:
                pass
      