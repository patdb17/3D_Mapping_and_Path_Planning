#!/usr/bin/env python
import rospy
#import geopy
#from geopy.distance import geodesic
# Because of transformations
import tf.transformations
import tf2_ros
import geometry_msgs.msg
from std_msgs.msg import Float64
from sensor_msgs.msg import NavSatFix
from nav_msgs.msg import Odometry
import tf2_msgs.msg

counter = 0

def callback_gps(data):
    ''' Broadcasts this UAS's translation and rotation, and publishes it as a
    transform from frame "map" to frame "velodyne". '''

    global counter
    global t
    global previous_pos

    t = geometry_msgs.msg.TransformStamped() # Creating the message object instance

    t.header.seq = counter
    counter += 1
    t.header.stamp = rospy.Time.now() # Gives transform being published a timestamp
    t.header.frame_id = "map" # Sets the name of parent frame of the link we're creating to map
    t.child_frame_id = "velodyne" # Sets the name of the child node of the link we're creating to velodyne

    # Copying the information from the gps lat/long into the 3D transform
    position = data.pose.pose.position
    orientation = data.pose.pose.orientation

    t.transform.translation.x = position.x
    t.transform.translation.y = position.y
    t.transform.translation.z = position.z

    q = [orientation.x, orientation.y, orientation.z, orientation.w]
    e = tf.transformations.euler_from_quaternion(q)
    print(e)
    new_e = list(e)
    # in  z-y-x rotation convention (Tait-Bryan angles), the rotation from pixhawk to velodyne is (0, -90, 90)
    new_e[0] = new_e[0]+1.5707 # Rotation about x
    new_e[2] = new_e[2]+1.5707 # Rotation about z


    q = tf.transformations.quaternion_from_euler(new_e[0], new_e[1], new_e[2])
    t.transform.rotation.x = q[0]
    t.transform.rotation.y = q[1]
    t.transform.rotation.z = q[2]
    t.transform.rotation.w = q[3]

    talker()




def callback_alt(data):
    pass



def callback_heading(data):
    pass


def talker():
    br = tf2_ros.TransformBroadcaster() # Creating TransformBroadcaster object instance
    global t

    # Sending a transform with a TransformBroadcaster requires passing in just the transform itself
    br.sendTransform(t)


def listener():
    rospy.init_node('tf2_velodyne_map_broadcaster')

    # Node subsribes to topic "/mavros/global_position/global", and runs the function
    # callback_gps on every incoming message
    #rospy.Subscriber("mavros/global_position/global", NavSatFix, callback_gps)
    rospy.Subscriber("mavros/global_position/local", Odometry, callback_gps)
    rospy.Subscriber("mavros/global_position/rel_alt", Float64, callback_alt)
    rospy.Subscriber("mavros/global_position/compass_hdg", Float64, callback_heading)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
