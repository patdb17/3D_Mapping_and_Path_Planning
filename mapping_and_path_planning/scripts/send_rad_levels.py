#!/usr/bin/env python
import rospy
import geopy
from geopy.distance import geodesic
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float64
from std_msgs.msg import String
from mavros_msgs.msg import StatusText

# Establish source location (Lat,Long) and source height [meters]
pos_source = ((37.213030, -80.4388310), 0)  #change for current source location <-- Caleb's house 

sim_counts = 100000, 5     # Source, Background

def callback_gps(data):
	global aircraft_gps
	lat = data.latitude
	lon = data.longitude
	aircraft_gps = lat, lon

def callback_alt(data):
	global aircraft_alt
	aircraft_alt = data.data
	counts()

def counts():
	pos_craft = (aircraft_gps, aircraft_alt) # Craft Position

	# Calculate Distance Between Source and Craft
	dist_hor = geopy.distance.distance(pos_source[0], pos_craft[0]).meters
	dist_vert = pos_source[1] - pos_craft[1]
	dist = (dist_vert**2 + dist_hor**2)**0.5

	prop_factor = 1/(dist**2) # Inverse Square Law
	counts_predict = (sim_counts[0] - sim_counts[1]) * prop_factor # Predicted Count Value

	talker(counts_predict)

def talker(counts_predict):
	pub = rospy.Publisher('mavros/statustext/send', StatusText, queue_size=10)
	rospy.init_node('send_rad_levels', anonymous=True)
	rate = rospy.Rate(2) # 2hz
	status_text = StatusText()
	counts = str(round(counts_predict))
	status_text.text = counts
	print(counts)
	status_text.severity = 11
	pub.publish(status_text)
	rate.sleep()

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('send_rad_levels', anonymous=True)

    rospy.Subscriber("mavros/global_position/global", NavSatFix, callback_gps)
    rospy.Subscriber("mavros/global_position/rel_alt", Float64, callback_alt)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
	listener()




