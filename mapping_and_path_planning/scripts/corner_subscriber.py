#!/usr/bin/env python

import rospy
from skyrad_msgs.msg import GeotaggedImage
import tf.transformations
from cv_bridge import CvBridge
import time
import math


''' This function runs a ros node that listens for the gps locations of the 4
corners of the image and saves them to a text file for testing purposes'''
def image_publisher():
    rospy.init_node('corners_read', anonymous=False)
    rate = rospy.Rate(21) # 10hz
    seq_num = 0


    while not rospy.is_shutdown():

        ''' Subscribe to trigger topic here'''
        rospy.Subscriber("image_publisher", GeotaggedImage, save_corners)

        rate.sleep()

''' Saves corner data to a .txt file'''
def save_corners(image_data):
    image_data.tl_lat
    if image_data.header.seq == 1:
        with open('image_corners.txt', 'w') as f:
            f.write('#Image_Num TL_Lat TL_Long TR_Lat TR_Long BL_Lat BL_Long BR_Lat BR_Long\n')

            f.write('Img_'+str(image_data.header.seq))
            f.write(' '+str(image_data.tl_lat))
            f.write(' '+str(image_data.tl_long))
            f.write(' '+str(image_data.tr_lat))
            f.write(' '+str(image_data.tr_long))
            f.write(' '+str(image_data.bl_lat))
            f.write(' '+str(image_data.bl_long))
            f.write(' '+str(image_data.br_lat))
            f.write(' '+str(image_data.br_long) + '\n')

    else
        with open('image_corners.txt', 'a') as f:
            f.write('Img_'+str(image_data.header.seq))
            f.write(' '+str(image_data.tl_lat))
            f.write(' '+str(image_data.tl_long))
            f.write(' '+str(image_data.tr_lat))
            f.write(' '+str(image_data.tr_long))
            f.write(' '+str(image_data.bl_lat))
            f.write(' '+str(image_data.bl_long))
            f.write(' '+str(image_data.br_lat))
            f.write(' '+str(image_data.br_long) + '\n')



if __name__ == '__main__':
    try:
        corner_subscriber()
    except rospy.ROSInterruptException:
        pass
