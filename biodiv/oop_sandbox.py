# Scratchpad specifically used because you want to do some big boy
# OOP proper coding with classes dans such.
import cv2 as cv
from biodiv.detection import biodivImg, V1, roiDrawer
from biodiv.filter import imgResizer, medBlurrer, otsuThresholder, pyramidMeanShiftFilter

pic = biodivImg(img_pth='pictures/samples/but1.jp2')

# print(pic.img.shape, 
# pic.img.min(),
# pic.img.max(),
# pic.img.dtype)

# import cv2 as cv
# pmsf_test = cv.pyrMeanShiftFiltering(pic.img, 21, 21)
# img_filter = pyramidMeanShiftFilter()
# pic.apply(img_filter)

detector = V1()
detector.LOADING_RESIZING_STEPS = [imgResizer(width=1000)]
drawer = roiDrawer()
drawer.ROI_BOX_RGB_COLOR = (255, 0, 0)
detector.ROI_DETECTION_STEPS = [drawer]

print(detector)
pic.apply(detector)
pic.display_img()

# loaded_pic = imgLoader(img_src='pictures/samples/but1.jp2')

# loaded_pic.test_super()

   