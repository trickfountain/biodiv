# Entry point when "using" biodiv
#   this will become sort of a CLI to test functions offline.

from biodiv.detection import V1
from biodiv.utils import display
from cv2 import rectangle

pic_dir = 'pictures/samples'
print('hello Eric \n'
      f'Enter the name of the picture found in {pic_dir}')
# input pars with input

pic_choice = input()
# TODO: validate input
img_src = pic_dir+'/'+pic_choice

img_res, ROIs = V1(img_src)

# TODO: wrap in a function to create nice green rectangles
for roi in ROIs:
    tl, br = tuple(roi[0]), tuple(roi[1])
    rectangle(img_res, tl, br, 0, 5)

display(img_res)
