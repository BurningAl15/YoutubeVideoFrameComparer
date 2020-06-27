import cv2
import os
import numpy as np

from pytube import YouTube
# misc
import os
import shutil
import math
import datetime
# plots
import matplotlib.pyplot as plt

class FrameExtractor():
    '''
    Class used for extracting frames from a video file.
    '''
    def __init__(self, video_path):
        self.video_path = video_path
        self.vid_cap = cv2.VideoCapture(video_path)
        self.n_frames = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.vid_cap.get(cv2.CAP_PROP_FPS))
        
    def get_video_duration(self):
        duration = self.n_frames/self.fps
        print(f'Duration: {datetime.timedelta(seconds=duration)}')
        
    def get_n_images(self, every_x_frame):
        n_images = math.floor(self.n_frames / every_x_frame) + 1
        print(f'Extracting every {every_x_frame} (nd/rd/th) frame would result in {n_images} images.')
        
    def extract_frames(self, every_x_frame, img_name, dest_path=None, img_ext = '.jpg'):
        if not self.vid_cap.isOpened():
            self.vid_cap = cv2.VideoCapture(self.video_path)
        
        if dest_path is None:
            dest_path = os.getcwd()
        else:
            if not os.path.isdir(dest_path):
                os.mkdir(dest_path)
                print(f'Created the following directory: {dest_path}')
        
        frame_cnt = 0
        img_cnt = 0

        while self.vid_cap.isOpened():
            
            success,image = self.vid_cap.read() 
            
            if not success:
                break
            
            if frame_cnt % every_x_frame == 0:
                img_path = os.path.join(dest_path, ''.join([img_name, '_', str(img_cnt), img_ext]))
                cv2.imwrite(img_path, image)  
                img_cnt += 1
                
            frame_cnt += 1
        
        self.vid_cap.release()
        cv2.destroyAllWindows()


_url='https://www.youtube.com/watch?v=QPXQlU7k6bQ'
_codec=18
_fileName='Gladys.mp4'
_checkImages='MyFrames/frame__0.jpg'

"""
Info: https://pypi.org/project/pytube3/
"""

"""
DOWNLOAD VIDEO
"""

#Check if video file exists
if os.path.exists(_fileName)==False:
    #if not exists, then download
    video = YouTube(_url)

    video.streams.all()
    video.streams.filter(file_extension = "mp4").all()
    out_File=video.streams.get_by_itag(_codec).download()

    #Change the name of the file
    os.rename(out_File,'Gladys.mp4')

"""
EXTRACT FRAMES
"""
if os.path.exists(_checkImages)==False:
    #Check the name of the file and extract the frames
    fe=FrameExtractor(_fileName);

    #Set every how much frames we get an image
    fe.get_n_images(every_x_frame=10)
    fe.extract_frames(every_x_frame=10, 
                    img_name='frame_', 
                    dest_path='MyFrames')

"""
COMPARE IMAGES
"""

#Compare images
arr=np.array([])

#Count all the elements from MyFrames folder
DIR = 'MyFrames'
count=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

imgInitialName="MyFrames/frame__"

for i in range(count-1):
    i2=i+1
    img1=cv2.imread(imgInitialName+ str(i)+".jpg")
    img2=cv2.imread(imgInitialName+ str(i2)+".jpg")

    resizedImg1=cv2.resize(img1,(360,360),interpolation=cv2.INTER_AREA)

    resizedImg2=cv2.resize(img2,(360,360),interpolation=cv2.INTER_AREA)

    difference=cv2.subtract(resizedImg1,resizedImg2)
    #zeros are the different pixels

    result=not np.any(difference)

    if result is True:
        print("Images are the same")
    else:
        print("Images are different")
        
    print(np.count_nonzero(difference==0))
    arr=np.append(arr,np.count_nonzero(difference==0))


"""
PRINT THE PLOT
"""
plt.plot(arr)
plt.show()