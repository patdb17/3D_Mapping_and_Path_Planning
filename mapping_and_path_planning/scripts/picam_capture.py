import sys
import cv2

#From the output, these are the supported camera modes from the driver :
#GST_ARGUS: 3264 x 2464 FR = 21.000000 fps Duration = 47619048 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 3264 x 1848 FR = 28.000001 fps Duration = 35714284 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 1920 x 1080 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 1640 x 1232 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 1280 x 720 FR = 59.999999 fps Duration = 16666667 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 1280 x 720 FR = 120.000005 fps Duration = 8333333 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;

def read_cam():
    cap = cv2.VideoCapture("nvarguscamerasrc sensor_id=0 ! video/x-raw(memory:NVMM), width=(int)3264, auto-exposure=1, exposure-time=0.0005, wbmode=5, height=(int)2464,format=(string)NV12, framerate=(fraction)21/1 ! nvvidconv ! video/x-raw,width=960, height=616, format=(string)BGRx ! videoconvert !  appsink")

    if cap.isOpened():
        read_cam.counter += 1
        ret_val, img = cap.read()
        filename = 'output_pi_img_' + str(read_cam.counter) + '.png'

        if img is None:
            result = "Image is empty, skipping save!!"
        else:
            cv2.imwrite(filename, img)
            return img

    else:
     print "camera open failed"

"Main code function"
# if __name__ == '__main__':
#      read_cam()
