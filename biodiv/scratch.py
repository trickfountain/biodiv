
from pathlib import Path
import numpy as np
import cv2 as cv

from biodiv.detector import detectorV1
# from biodiv.detection import roiDrawer

img_src = '/Users/ericfontaine/code/biodiv/biodiv/tests/test_images/five_shapes.png'
det = detectorV1(img_src)
org, d = det.apply()

cv.imshow('original', org)
cv.waitKey(0)
cv.imshow('detected', d)
cv.waitKey(0)
cv.destroyAllWindows()