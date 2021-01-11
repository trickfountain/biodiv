# -*- coding: utf-8 -*-
from biodiv.filter import imgResizer, medBlurrer, otsuThresholder, pyramidMeanShiftFilter
import cv2 as cv
from biodiv.utils import rectangle_area
import numpy as np


class roiDrawer:
    '''Draws Regions Of Interest
    '''
    #TODO: make properties overwrite-able with kwargs
    ROI_MIN_SIZE = 2.0
    ROI_MARGIN = 3.75
    BORDER_PADDING = round(ROI_MARGIN/5)
    ROI_BOX_RGB_COLOR = (0, 255, 0)

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(**kwargs)

    def apply(self, img):
        self._load_img(img)
        self.detect_ROI()
        img_with_ROI_drawn = self.draw_ROI()

        return img_with_ROI_drawn

    def _load_img(self, img):
        #TODO: should the image property be in a class that is responsible
        # of drawing.
        self.img_org = img
        self.img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        #TODO: height, area, region_of_interest should be properties
        # of biodiv.img, not of the drawer itself.
        self.region_of_interest = []
        self.height, self.width = self.img.shape[0], self.img.shape[1]
        self.img_area = self.height * self.width
        self.margin_px = int(round(self.width * self.ROI_MARGIN / 100))
        self.min_ROI_area = self.img_area * self.ROI_MIN_SIZE / 100
        
    def draw_ROI(self):
        '''Draws regions of interest on img

        expects the output of a detector function: a list of top_left,
        bottom_right, tuple to draw.
        '''
        if self.region_of_interest is not None:
            img_with_roi_drawing = self.img_org.copy()
            
            for region in self.region_of_interest:
                tl, br = tuple(region[0]), tuple(region[1])
                cv.rectangle(img_with_roi_drawing, tl, br, self.ROI_BOX_RGB_COLOR, 5)
            
            return img_with_roi_drawing

        else:
            print('Did not find region of interest to draw')
            return self.img_org

    def detect_ROI(self):
        ''' '''
        ext_contours = self._find_ext_contours()
        self.region_of_interest = self._qualify_ROI(ext_contours)

    def _qualify_ROI(self, ext_contours):
        roi_list = []
        for contour in ext_contours:
            contour_area = self._calculate_ROI_zone(contour)

            if contour_area > self.min_ROI_area:
                top_left = self._top_left_from_contour(contour)
                bottom_right = self._bottom_right_from_contour(contour)    

                roi_list.append((top_left, bottom_right))

        return roi_list

    def _find_ext_contours(self):
        contours, hierarchy = cv.findContours(
            self.img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        ext_contours = [contours[i]
                        for i in range(len(contours)) if hierarchy[0][i][3] == -1]
        return ext_contours

    def _calculate_ROI_zone(self, contour):
        '''Calculate ROI bounded rectangle from contour including formating.
        '''

        top_left = self._top_left_from_contour(contour)
        bottom_right = self._bottom_right_from_contour(contour)
        ROI_area = rectangle_area(top_left, bottom_right)

        return ROI_area

    def _top_left_from_contour(self, contour):
        '''Takes contour and finds x, y coord of top left, taking
        into account formating options.
        '''
        x, y, _, _ = cv.boundingRect(contour)
        top_left = (x - self.ROI_MARGIN, y + self.ROI_MARGIN)
        top_left = self._frame_coord(top_left)

        return top_left

    def _bottom_right_from_contour(self, contour):
        x, y, width, height = cv.boundingRect(contour)
        bottom_right_x = (x + width + self.ROI_MARGIN)
        bottom_right_y = (y + height + self.ROI_MARGIN)
        bottom_right = (bottom_right_x, bottom_right_y)
        bottom_right = self._frame_coord(bottom_right)

        return bottom_right

    def _frame_coord(self, ROI_corner_coord):
        '''Apply _frame_height and _frame_width to corner coord'''

        ROI_corner_coord = self._frame_width(ROI_corner_coord)
        ROI_corner_coord = self._frame_height(ROI_corner_coord)

        return ROI_corner_coord

    def _frame_width(self, ROI_corner_coord):
        '''For a point on the X axis, make sure it's within
        the frame
        '''
        x, y = ROI_corner_coord
        if x < 0:
            x = self.BORDER_PADDING
        elif x > self.width:
            x = self.width - self.BORDER_PADDING

        #TODO: Not clean code
        # Some openCV functions do not support floats for coordinates
        x = int(x)
        y = int(y)
        return x, y

    def _frame_height(self, ROI_corner_coord):
        '''For a point on the Y axis, make sure it's within
        the frame
        '''
        x, y = ROI_corner_coord

        if y < 0:
            y = self.BORDER_PADDING
        elif y > self.height:
            y = self.height - self.BORDER_PADDING

        x = int(x)
        y = int(y)
        return x, y
  
    #TODO: should probably be a static method but I'm not sure how these work
    def _calculate_contour_area(self, contour):
        _, _, w, h = cv.boundingRect(contour)
        contour_area = (w + self.margin_px) * (h + self.margin_px)
        return contour_area

    def __repr__(self) -> str:
        return ('ROI detection using cv.findContours with parameters :\n'
                f'ROI_MIN_SIZE: {self.ROI_MIN_SIZE}, ROI_MARGIN: {self.ROI_MARGIN}px '
                f'ROI_BOX_RGB_COLOR: {self.ROI_BOX_RGB_COLOR}')


class imgDetector:
    '''Wraps up ROI detection and drawing steps'''
    
    def apply(self, img):
        # self._load_img(img, img)
        self.img = self.identifyROI(img)
        # ROI = self.detect_ROI()
        # self.draw_ROI(ROI)
        return self.img


        
# def detect_ROI(img, min_size=2, margin=3.75):
#     """Finds Regions Of Interest (ROI) on image
#     Returns a mask of all ROIs of minimum size min_size.

#     Expects a grayscale image.
#     img: 2 dimensionnal numpy array representing a gray scale image
#     min_size: Size of ROIs relative to img area. Includes margins.
#     margins: Padding added to ROIs, expressed as a pt of img width
#     """

#     # Some parameters are based on the width or area of the image.
#     height, width = img.shape[0], img.shape[1]
#     img_area = width * height

#     contours, hierarchy = cv.findContours(
#         img,
#         cv.RETR_EXTERNAL,
#         cv.CHAIN_APPROX_SIMPLE
#     )
#     ext_contours = [contours[i]
#                     for i in range(len(contours)) if hierarchy[0][i][3] == -1]
#     margin_px = int(round(width * margin/100))

#     ROIs = []
#     for i, cnt in enumerate(ext_contours):

#         x, y, w, h = cv.boundingRect(cnt)
#         area = (w+margin_px)*(h+margin_px)
#         top_left, bottom_right = bounded_rectangle(x, y, w, h,
#                                                    margin_px, width, height)

#         if area > img_area * min_size/100:
#             ROIs.append((top_left, bottom_right))

#     return ROIs


# def V1_detector(img_src: str):
#     # TODO: rewrite docstring, scope of V1 changed.
#     '''First version for detection
#     Pipeline that starts with img path and ends with img (resized)
#         and Regions of Interests

#     ROI: 
#     '''
#     img = cv.imread(img_src, 0)
#     res_img = resize_img(img, 600)
#     pre_processed = pp_img(res_img)
#     ROI = detect_ROI(pre_processed)

#     return res_img, ROI


# def draw_ROI(img, ROI):
#     '''Draws Regions of Interest on img

#     expects the output of a detector function (img & ROIs)
#     img and ROIs have to be the same shape.

#     ROI: (top_left, bottom_right) of a region rectangle.
#       meant to be used with cv.rectangle
#     '''
#     img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
#     for region in ROI:
#         tl, br = tuple(region[0]), tuple(region[1])
#         cv.rectangle(img, tl, br, (0, 200, 0), 5)

#     return img


# if __name__ == "__main__":
#     pic = "pictures/samples/cats1.jp2"
#     res_img, ROIs = V1_detector(pic)
#     out = draw_ROI(res_img.copy(), ROIs)

#     display(res_img, out)
