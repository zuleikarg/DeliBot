#!/usr/bin/env python3

import rospy
from my_code.msg import data_employee, data_recognition, collect

import logging
import argparse
import os
import time
import cv2

start = 0
name = ''
depart = ''
video = []
collected = False

from demo_inference import DemoInference
from utils.vis_generator import VisGenerator
from utils.vis_writer import VisWriter
from video_iterator import build_video_iterator

parser = argparse.ArgumentParser(" SiamMOT Inference Demo")
# parser.add_argument('--demo-video', metavar="FILE", type=str,
                    # required=True)
parser.add_argument('--track-class', type=str, choices=('person', 'person_vehicle'),
                    default='person',
                    help='Tracking person or person/vehicle jointly')
parser.add_argument("--dump-video", type=bool, default=False,
                    help="Dump the videos as results")
parser.add_argument("--vis-resolution", type=int, default=1080)
parser.add_argument("--output-path", type=str, default=None,
                    help='The path of dumped videos')

def callback(data):
    global start, name, depart, video

    video= cv2.VideoCapture(0)
    start = 1
    name = data.name
    depart = data.department

def collecting(data):
    global collected

    collected = data.collected

if __name__ == '__main__':
    rospy.init_node('program', anonymous=True)
    rospy.Subscriber('program_started', data_employee, callback)
    rospy.Subscriber('collected', collect, collecting)
    recog_pub = rospy.Publisher('/recognition', data_recognition, queue_size=10)
    message = data_recognition()
    message.recog = False

    args = parser.parse_args()
    # video= cv2.VideoCapture(0)
    # ret, frame = video.read()

    while(not rospy.is_shutdown() and collected == False):
        
        if(start == 1):

            # out = cv2.VideoWriter("Real-Time.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30.0,(int(width), int(height)))

            starttime = time.time()
            ret, frame = video.read()
            height, width, _ = frame.shape
            
            if(ret):
                logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                                    datefmt='%Y-%m-%d:%H:%M:%S',
                                    level=logging.INFO)

                # Build visulization generator and writer
                vis_generator = VisGenerator(vis_height=args.vis_resolution)

                vis_writer = VisWriter(dump_video=args.dump_video,
                                    out_path=args.output_path,
                                    file_name=os.path.basename("Real-Time.mp4"))
                # Build demo inference
                tracker = DemoInference(track_class=args.track_class,
                                        vis_generator=vis_generator,
                                        vis_writer=vis_writer)
                # Build video iterator for inference
                video_reader = build_video_iterator(frame)

                results = list(tracker.process_frame_sequence(video_reader(),width,height, name))

                print(results[0][3][0])
                if(results[0][3][0] != "N"):
                    message.recog = bool(results[0][3][0])
                    recog_pub.publish(message)
                    
                # if args.dump_video:
                #     vis_writer.close_video_writer()

                #video_reader.vr.release()
                # out.write(results[0][2])
                
            else:
                exit

            endtime = time.time()
            print(f'Time of ejecution is: {endtime - starttime}')
            starttime = endtime
    
    if(start == True):
        video.release()

