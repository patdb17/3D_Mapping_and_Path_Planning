import cv2 as cv
import math
import pyproj

FOVhoriz = 70 # Lens/sensor horizontal FOV in deg
FOVvert = 55.49 # Lens/sensor vertical FOV in deg
cam_angle_offset = 180 # Camera was angled 90deg relative to heading of UAS


"Calulating the lat/long of each corner"
def uncorrected_corners(img, odom):

    # Returns list of odom info
    # odom = get_odom(imgFilePath)
    # odom = [0, 37.1971445, -80.5779913, 122.57999420166, 319.58, 1.62, -9.7]

    # Assign odom info to variables
    lat_y = float(odom[1])
    long_x = float(odom[2])
    height_z = float(odom[3])
    yaw = float(odom[4])
    pitch = float(odom[5])
    roll = float(odom[6])

    # print(odom)
    # print(lat_y, long_x, height_z, yaw, pitch, roll)

    # Extracting height and width of image in pixels
    # img = cv.imread(imgFilePath)
    h, w = img.shape[:2]

    # Calculating distance from directly below aircraft to edges of image
    dist_left = height_z * math.tan(math.radians(roll + FOVhoriz/2))
    dist_right = height_z * math.tan(math.radians(FOVhoriz/2 - roll))
    dist_up = height_z * math.tan(math.radians(pitch + FOVvert/2))
    dist_down = height_z * math.tan(math.radians(FOVvert/2 - pitch))

    # Converts distances from aircraft xy-coordinates to global xy-coordinates
    corner_add = []
    corner_add.append(uas_to_global(-dist_left, dist_up, yaw + cam_angle_offset))
    corner_add.append(uas_to_global(dist_right, dist_up, yaw + cam_angle_offset))
    corner_add.append(uas_to_global(dist_right, -dist_down, yaw + cam_angle_offset))
    corner_add.append(uas_to_global(-dist_left, -dist_down, yaw + cam_angle_offset))

    # Changes aircraft lat-long to xy
    # print(long_x, lat_y)
    long_x, lat_y = lonlat_to_xy(long_x, lat_y)
    # print(long_x, lat_y)

    # Convention used is top-left, top-right, bottom-left, bottom-right
    corners = []
    corners.append([long_x+corner_add[0][0], lat_y+corner_add[0][1]])
    corners.append([long_x+corner_add[1][0], lat_y+corner_add[1][1]])
    corners.append([long_x+corner_add[3][0], lat_y+corner_add[3][1]])
    corners.append([long_x+corner_add[2][0], lat_y+corner_add[2][1]])

    # Converts image coordinates to long-lat
    for point in corners:
        point[1], point[0] = xy_to_lonlat(point[0], point[1])

    return corners

"Extracts the odometry data for a given image and returns list of data"
# def get_odom(imgFilePath):
#
#     # File path to text file with odom data
#     odomFilePath = 'Images/location.txt'
#
#     # Opens file
#     file = open(odomFilePath,'r')
#
#     # Pulls all text from file
#     all_info = file.readlines()
#
#     # Isolates image file name from path
#     imgFileName = imgFilePath[7:]
#
#     # Finds the correct line for image
#     for info in all_info:
#         if info.startswith(imgFileName):
#             img_info = info
#             break
#
#     # Converts string of info into list of info
#     img_info = img_info.split()
#
#     return img_info

"Function to convert xy coordinates to long-lat"
def xy_to_lonlat(x, y):
    proj_latlon = pyproj.Proj(proj='latlong',datum='WGS84')
    proj_xy = pyproj.Proj(proj="utm", zone=17, datum='WGS84') # For Blacksburg use zone 17, for Baltimore use zone 18
    lonlat = pyproj.transform(proj_xy, proj_latlon, x, y)
    return lonlat[0], lonlat[1]

"Function to convert long-lat to xy coordinates"
def lonlat_to_xy(lon, lat):
    proj_latlon = pyproj.Proj(proj='latlong',datum='WGS84')
    proj_xy = pyproj.Proj(proj="utm", zone=17, datum='WGS84') # For Blacksburg use zone 17, for Baltimore use zone 18
    xy = pyproj.transform(proj_latlon, proj_xy, lon, lat)
    return xy[0], xy[1]

"Function to convert xy coords in UAS frame to global frame"
def uas_to_global(x, y, yaw):
    new_x = x*math.cos(math.radians(yaw)) - y*math.sin(math.radians(yaw))
    new_y = y*math.cos(math.radians(yaw)) + x*math.sin(math.radians(yaw))
    return new_x, new_y



"Main code function"
# if __name__ == '__main__':
#     imgFilePath = 'Images/image39.jpg'
#
#     corners = uncorrected(imgFilePath)
#
#     print(corners)
