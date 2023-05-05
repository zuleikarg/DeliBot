import cv2
import os
import face_recognition
import numpy as np
from matplotlib import cm
from datetime import date

from maskrcnn_benchmark.structures.bounding_box import BoxList

id_photo=0

class VisGenerator:
    """
    Generate a video for visualization
    """
    def __init__(self, vis_height=None):
        """
        vis_height is the resolution of output frame
        """
        self.path = "demo_vis/"+ str(date.today())
        self._vis_height = vis_height
        # by default, 50 colors
        self.num_colors = 50
        self.colors = self.get_n_colors(self.num_colors)
        # use coco class name order
        self.class_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat']

    @staticmethod
    def get_n_colors(n, colormap="gist_ncar"):
        # Get n color samples from the colormap, derived from: https://stackoverflow.com/a/25730396/583620
        # gist_ncar is the default colormap as it appears to have the highest number of color transitions.
        # tab20 also seems like it would be a good option but it can only show a max of 20 distinct colors.
        # For more options see:
        # https://matplotlib.org/examples/color/colormaps_reference.html
        # and https://matplotlib.org/users/colormaps.html

        colors = cm.get_cmap(colormap)(np.linspace(0, 1, n))
        # Randomly shuffle the colors
        np.random.shuffle(colors)
        # Opencv expects bgr while cm returns rgb, so we swap to match the colormap (though it also works fine without)
        # Also multiply by 255 since cm returns values in the range [0, 1]
        colors = colors[:, (2, 1, 0)] * 255
        return colors

    def normalize_output(self, frame, results: BoxList):
        if self._vis_height is not None:
            boxlist_height = results.size[1]
            frame_height, frame_width = frame.shape[:2]
            assert (boxlist_height == frame_height)

            rescale_ratio = float(self._vis_height) / float(frame_height)
            new_height = int(round(frame_height * rescale_ratio))
            new_width = int(round(frame_width * rescale_ratio))

            frame = cv2.resize(frame, (new_width, new_height))
            results = results.resize((new_width, new_height))

        return frame, results

    def frame_vis_generator(self, frame, results: BoxList, width, height, name):
        global id_photo
        #Create the path with the date if it doesn't already exists
        if not os.path.exists(self.path):
            os.mkdir(self.path)  

        frame, results = self.normalize_output(frame, results)
        ids = results.get_field('ids')
        results = results[ids >= 0]
        results = results.convert('xyxy')
        bbox = results.bbox.detach().cpu().numpy()
        ids = results.get_field('ids').tolist()
        labels = results.get_field('labels').tolist()

        recognition = "N"
        for i, entity_id in enumerate(ids):

            color = self.colors[entity_id % self.num_colors]
            class_name = self.class_names[labels[i] - 1]
            text_width = len(class_name) * 20
            x1, y1, x2, y2 = (np.round(bbox[i, :])).astype(np.int)

            new_image = frame[y1:y2,x1:x2]
            small_frame = cv2.resize(new_image, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small_frame,model="cnn")
            unknown_face_encoding = face_recognition.face_encodings(rgb_small_frame,face_locations)
            # print(unknown_face_encoding)
            # new_image = cv2.resize(new_image, (width, height), interpolation = cv2.INTER_AREA)
            if(len(new_image)>1 and len(unknown_face_encoding)>0):
                # Implementar para cuando no haya datos en new_iamge, es decir, cuando no se detecte persona

                #print(f'No conocida{unknown_face_encoding}')
                known_person = face_recognition.load_image_file("conocidos/"+name+".jpg")
                # img = cv2.imread('demos/Zuleika.jpg',cv2.IMREAD_COLOR)
                # cv2.imshow('image',img)
                # cv2.waitKey(0)
                known_face_encoding = face_recognition.face_encodings(known_person)[0]
                #print(f'Conocida{known_person}')

                recognition = face_recognition.compare_faces([np.array(known_face_encoding)], np.array(unknown_face_encoding))
                # print(f'{recognition}')

            # if not os.path.exists('demos/demo_vis/'+str(date.today())):
            #     os.mkdir(str(date.today())) 

            # cv2.imwrite('demos/demo_vis/'+str(date.today())+"/"+str(id_photo)+".jpg",new_image)
            # id_photo = id_photo+1

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=3)
            cv2.putText(frame, str(entity_id), (x1 + 5, y1 + 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)
            # Draw black background rectangle for test
            cv2.rectangle(frame, (x1-5, y1-25), (x1+text_width, y1), color, -1)
            cv2.putText(frame, '{}'.format(class_name), (x1 + 5, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), thickness=2)

            cv2.imwrite(os.path.join(self.path,str(id_photo)+".jpg"), new_image)
            id_photo = id_photo+1
        return frame,recognition
