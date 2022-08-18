from std_srvs.srv import Trigger
from sensor_msgs.msg import Image
import cv2 as cv
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
import os
from datetime import datetime as Datetime
from datetime import date as Date

class VideoRecord(Node):

    filename = ""
    data_dir = ""
    parameter = ""
    start_record = False
    finished = False
    out_video = cv.VideoWriter()
    # out_video_2 = cv.VideoWriter()
    home_dir = os.path.expanduser('~')
    directory = home_dir + '/lg/video/'


    def __init__(self):
        super().__init__('video_record')
        self.sub = self.create_subscription(Image, "/camera/color/image_raw", self.callback, qos_profile=10)
        self.start_record_srv = self.create_service(Trigger, 'start_record_video', self.handle_start_record)
        self.stop_record_srv = self.create_service(Trigger,'stop_record_video', self.handle_stop_record)

        # state initial
        today = Date.today()
        self.data_dir = self.directory +  today.strftime("%y_%m_%d") + "/"

        if(os.path.exists(self.data_dir)):
            pass
        else:
            os.makedirs(self.data_dir)
        pass

    def add_two_ints_callback(self, request, response):
        response.success = True
        return response
    
    
    def handle_start_record(self,request, response):
        now = Datetime.now()
        self.filename = now.strftime("%H_%M")
        self.get_logger().info('file name is: ' + self.filename +'.mp4')

        fourcc = cv.VideoWriter_fourcc(*"mp4v")
        # fourcc = cv.VideoWriter_fourcc('H','2','6','4')
        fps = 30
        size = (1280, 720)
        
        fileFullName = self.data_dir + self.filename + '.mp4'
        self.out_video = cv.VideoWriter(fileFullName, fourcc, fps, size)
        self.start_record = True
        response.success = True
        return response

    def handle_stop_record(self,request, response):
        self.get_logger().info('Video: ' + self.filename +'.mp4'+' Finished!')
        self.start_record = False
        self.finished = True
        response.success = True
        return response

    def callback(self,image):
        if self.start_record:
            # self.get_logger().info("Start record" )
            bridge = CvBridge()
            cv_image = bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')            
            self.out_video.write(cv_image)
            # self.out_video_2.write(cv_image)
        elif self.finished:
            self.finished = False
            self.out_video.release()
            # self.out_video_2.release()
        else:
            pass
        # cv.waitKey(0) 

def main():
    rclpy.init()

    video_record = VideoRecord()

    rclpy.spin(video_record)

    rclpy.shutdown()


if __name__ == '__main__':
    main()