# -*- coding: utf-8 -*-

# Load image
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def display(img, img2=None, title=None, cmap="gray"):
    if type(img2) == np.ndarray:
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(121)
        ax.imshow(img, cmap=cmap)
        ax = fig.add_subplot(122)
        ax.imshow(img2, cmap=cmap)

    else:
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.imshow(img, cmap=cmap)

    if title:
        fig.suptitle(title, fontsize=16)

    plt.show()


def rect_area(pt1, pt2):
    max_x, min_y = pt1
    min_x, max_y = pt2
    width = max_x - min_x
    height = max_y - min_y
    area = width * height

    return area


def otsu(img):
    _, OTSU = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    return OTSU


def bounded_rectangle(x, y, w, h, margin, width, height, output_type="tlbr"):
    '''Return coordinates of ROI rectangle taking into account margins and
    img boundaries.

    Returns either (top_left, bottom_right) or 4 corner coordinates depending
    on output_type.

    x,y,w,h : top left coord + width and height returned by cv.boundingRect
    margin: margin (in px) chosen for ROI
    width, height: of the image (img.shape)
    output_type: tlbl or corners
        tlbl: Top Left Bottom Right, format for cv.rectangle
        corners: (x,y) coord of each corner, format for contours
    '''

    # TODO : check if x,y width and height are ok. I think openCV uses (y, x) or something.
    tl = np.array((x - margin, y - margin))
    bl = np.array((tl[0], y + h + margin))
    br = np.array((x + w + margin, bl[1]))
    tr = np.array((br[0], y - margin))

    if output_type == 'tlbr':
        coords = np.array([tl, br])

    elif output_type == 'corners':
        coords = np.array([tl, bl, br, tr], dtype=np.int32)

    else:
        raise ValueError('Expecting one of "tlbr" or "corners" for argument'
                         ' output_type')

    pad = round(margin/5)
    for i, coord in enumerate(coords):
        x, y = coord
        if x < 0:
            coords[i][0] = pad
        elif x > width:
            coords[i][0] = width - pad

        if y < 0:
            coords[i][1] = pad
        elif y > height:
            coords[i][1] = height - pad

    return coords


def redCircle_mask(pic):
    '''Takes an image and creates a mask from red circle.

    Used to test accuracy of detection by providing labeled test image.
    '''
    img = cv.imread(pic)

    pass


def find_extContours(img, thresh=1000):
    contours, _ = cv.findContours(
        img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #TODO: Not sure if needed, RETR_EXTERNAL should already return external contours
    #TODO: check to add area filter, really low: just to remove "specks"
    ext_contours = [cnt for cnt in contours if cv.contourArea(cnt) > thresh]

    return ext_contours


# TODO: Create load_image
def load_image(img_src, colors=1):
    '''Loads image with cv2 and raise error if source not found
    '''
    ## Test for file on img_src.


    ## Check that img is not None on exit.