#!/usr/bin/env python

import rospy
from skyrad_msgs.msg import GeotaggedImage
from mavros_msgs.msg import RCOut
from std_msgs.msg import Float64
from sensor_msgs.msg import NavSatFix
from nav_msgs.msg import Odometry
import tf.transformations
from cv_bridge import CvBridge
from img_corners import *
import picam_capture
import time
import math

cam_trigger = False
odom = [0,0,0,0,0,0,0]
cv2_img = 0

''' This function runs a ros node that listens for a camera trigger, reads in gps data
    and publishes the image taken as well as the gps locations of the 4 corners of the image'''
def image_publisher():
    global cam_trigger
    global cv2_img
    picam_capture.read_cam.counter = 0
    pub = rospy.Publisher('image_publisher', GeotaggedImage, queue_size=10)
    rospy.init_node('image_data', anonymous=False)
    rate = rospy.Rate(10) # 10hz
    seq_num = 0


    while not rospy.is_shutdown():

        ''' Subscribe to trigger topic here'''
        rospy.Subscriber("mavros/rc/out", RCOut, trigger_func)

        if cam_trigger == True:

            # Node subsribes to topics when camera is triggered to pull gps data
            rospy.Subscriber("mavros/global_position/global", NavSatFix, callback_gps)
            rospy.Subscriber("mavros/global_position/local", Odometry, callback_odom)
            rospy.Subscriber("mavros/global_position/rel_alt", Float64, callback_alt)
            rospy.Subscriber("mavros/global_position/compass_hdg", Float64, callback_heading)

            cv2_img = picam_capture.read_cam()
            corners = uncorrected_corners(cv2_img, odom)
            geo_image = GeotaggedImage()
            geo_image.header.stamp = rospy.Time.now()

            bridge = CvBridge()

            geo_image.image = bridge.cv2_to_imgmsg(cv2_img, "bgr8")

            geo_image.header.frame_id = "image_sensor"
            seq_num = seq_num+1
            geo_image.header.seq = seq_num

            geo_image.tl_lat = corners[0][1]
            geo_image.tl_lon = corners[0][0]

            geo_image.tr_lat = corners[1][1]
            geo_image.tr_lon = corners[1][0]

            geo_image.bl_lat = corners[2][1]
            geo_image.bl_lon = corners[2][0]

            geo_image.br_lat = corners[3][1]
            geo_image.br_lon = corners[3][0]

            rospy.loginfo("Image Seq Num: %d, tl_lat: %f" % (geo_image.header.seq, geo_image.tl_lat))
            pub.publish(geo_image)
	    time.sleep(0.25)
            cam_trigger = False

        rate.sleep()

''' Saves gps data'''
def callback_gps(gps_data):
    global cam_trigger
    global odom

    if cam_trigger == True:
        odom[1] = gps_data.latitude
        odom[2] = gps_data.longitude

''' Saves yaw pitch roll '''
def callback_odom(odom_data):
    global cam_trigger
    global odom
    if cam_trigger == True:
        q_x, q_y, q_z, q_w = [odom_data.pose.pose.orientation.x,
                              odom_data.pose.pose.orientation.y,
                              odom_data.pose.pose.orientation.z,
                              odom_data.pose.pose.orientation.w]

        # Do math to convert quaternion into ypr
        yaw, pitch, roll = tf.transformations.euler_from_quaternion([q_x, q_y, q_z, q_w], 'szyx')
	yaw = math.degrees(yaw)
	pitch = math.degrees(pitch)
	roll = math.degrees(roll)
        odom[4] = yaw
        odom[5] = pitch
        odom[6] = roll

''' Saves relative altitude '''
def callback_alt(rel_alt_data):
    global cam_trigger
    global odom

    if cam_trigger == True:
        odom[3] = rel_alt_data.data

''' Saves yaw angle (might be unnecessary since we can find from odom)'''
def callback_heading(heading_data):
    global cam_trigger
    global odom

    if cam_trigger == True:
        odom[4] = heading_data.data

''' Listens for camera trigger '''
def trigger_func(trigger_data):
    global cam_trigger

    # Trigger is sent on channel 16 of mavros RCOut
    # 0 is no trigger, and 1 is the trigger
    if trigger_data.channels[15] == 1 and cam_trigger == False:
        cam_trigger = True
        print(trigger_data.channels[15])



if __name__ == '__main__':
    try:
        image_publisher()
    except rospy.ROSInterruptException:
        pass

 # BEWARE
# geo_image.image = self.bridge.cv2_to_imgmsg(cv_image, "bgr8")
