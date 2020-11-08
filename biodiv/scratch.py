from biodiv.detection import V1
from biodiv.utils import display
import os
os.environ['OPENCV_IO_ENABLE_JASPER'] = 'True'
import cv2 as cv

detector = V1
#img_src = 'biodiv/tests/test_images/but1.jp2'
#img_res, ROIs = detector(img_src)

t = cv.imread('biodiv/tests/test_images/but1.jp2', 1)
display(t)
