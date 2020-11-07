# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
from biodiv.utils import bounded_rectangle, display


def resize_img(img: np.array, resize_width=False):
    '''Resize image.

    Keep original shape if resize_width=False
    '''
    if not isinstance(img, np.ndarray):
        raise ValueError('img should be of format np.array, check input provided')

    if resize_width:
        width = resize_width
        resize_factor = width/img.shape[1]
        img = cv.resize(img.copy(), None, fx=resize_factor, fy=resize_factor,
                        interpolation=cv.INTER_CUBIC
                        )

    return img


def pp_img(img: np.ndarray, ksize=5, pmsf_par=(21,21)):
    '''Wrapper for pre-processing steps needed for proper detection
    '''

    # TODO : Consider including cv.Canny. Looks fast and good but haven't figured out how to return
    # image that is nice and bright.
    # canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    # from : https://docs.opencv.org/3.4/da/d0c/tutorial_bounding_rects_circles.html

    try:
        # Test whether array is of type uint8. If not an array will fail.
        t = img.dtype == 'uint8'
        if not t:
            raise AttributeError
    except AttributeError:
        raise ValueError('Expecting np.array for img')

    # medium Blur. Supposed to keep edges better than gaussian blur
    ksize = ksize
    medBlur = cv.medianBlur(img, ksize)

    # Inv binary threshold with Otsu
    _, otsu = cv.threshold(medBlur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # pyramid mean shift filtering. Does a good job at neutralizing
    #   background but really expensive to compute
    grayToRbg = cv.cvtColor(otsu, cv.COLOR_GRAY2RGB)
    pmsf = cv.pyrMeanShiftFiltering(grayToRbg, pmsf_par[0], pmsf_par[1])
    pmsf_gray = cv.cvtColor(pmsf, cv.COLOR_RGB2GRAY)

    # TODO tests: check that returning array
    #             test error message with img = None or string

    return pmsf_gray


def detect_ROI(img, min_size=2, margin=3.75):
    """Finds Regions Of Interest (ROI) on image
    Returns a mask of all ROIs of minimum size min_size.

    Expects a grayscale image.
    img: 2 dimensionnal numpy array representing a gray scale image
    min_size: Size of ROIs relative to img area. Includes margins.
    margins: Padding added to ROIs, expressed as a pt of img width
    """

    # Some parameters are based on the width or area of the image.
    height, width = img.shape[0], img.shape[1]
    img_area = width * height

    contours, hierarchy = cv.findContours(
        img,
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
        )
    ext_contours = [contours[i] for i in range(len(contours)) if hierarchy[0][i][3] == -1]
    margin_px = int(round(width * margin/100))

    ROIs = []
    for i, cnt in enumerate(ext_contours):

        x, y, w, h = cv.boundingRect(cnt)
        area = (w+margin_px)*(h+margin_px)
        top_left, bottom_right = bounded_rectangle(x, y, w, h,
                                                   margin_px, width, height)

        if area > img_area * min_size/100:
            ROIs.append((top_left, bottom_right))

    return ROIs


def V1(img_src: str):
    ##TODO: rewrite docstring, scope of V1 changed.
    '''Detects principal Regions Of Interest (ROI) for an image

    expects a grayscale image loaded with OpenCv

    V1 is using pyramid shift filtering which is expensive to compute and 
    probably not necessary.

    show :: If true will display original and detected images side by side.
        Otherwise returns modified image with ROI inside rectangles
    '''
    img = cv.imread(img_src, 0)
    res_img = resize_img(img, 600)
    pre_processed = pp_img(res_img)
    ROIs = detect_ROI(pre_processed)

    return res_img, ROIs


if __name__ == "__main__":
    pic = "pictures/samples/cats1.jp2"
    res_img, ROIs = V1(pic)
    out = res_img.copy()
    for ROI in ROIs:
        tl, br = tuple(ROI[0]), tuple(ROI[1])
        cv.rectangle(out, tl, br, 127, 5)

    display(res_img, out)
