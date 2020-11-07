import cv2 as cv
from matplotlib.pyplot import contour
import numpy as np
from numpy.lib.polynomial import polyint
from biodiv.utils import display
from biodiv.utils import bounded_rectangle


x, y, w, h, margin = 10, 30, 40, 60, 10
coords = bounded_rectangle(x, y, w, h, margin, width=100, height=100, output_type='corners')

contours = [coords]

drawing = np.zeros([400, 400], np.uint8)

for cnt in contours:
    cv.drawContours(drawing, [cnt], 0, (255, 255, 255), 2)

a = np.array([40,40])
b = np.array([300,300])

# cnt = contours[0]
# for target in [a,b]:
#     print(target)
#     result = cv.pointPolygonTest(tuple(cnt), target, False)
#     print(result)

