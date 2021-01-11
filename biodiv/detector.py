from biodiv.detection import roiDrawer
from biodiv.filter import (imgResizer, medBlurrer, otsuThresholder,
                           pyramidMeanShiftFilter)
from biodiv.img import imgLoader

import cv2 as cv


class detectorV1:
    '''First version of detection pipeline
    '''

    LOADING_RESIZING_STEPS = [
        imgResizer(width=600)
    ]
    IMG_FILTER_STEPS = [
        medBlurrer(),
        otsuThresholder(),
        pyramidMeanShiftFilter(),
    ]
    ROI_DETECTION_STEPS = [ 
        roiDrawer()
    ]

    STAGES = {
        'Loading and resizing': LOADING_RESIZING_STEPS,
        'Image filters': IMG_FILTER_STEPS,
        'Detection': ROI_DETECTION_STEPS
    }

    def __init__(self, img_pth) -> None:
        loader = imgLoader(img_pth)
        self.img = loader.load_image()

    def apply(self):
        
        for step in self.LOADING_RESIZING_STEPS:
            self.img = step.apply(self.img)
            self.resized_img = self.img.copy()

            # cv.imshow('resized', self.resized_img)
            # cv.waitKey(0)

        for step in self.IMG_FILTER_STEPS:
            self.img = step.apply(self.img)
            # cv.imshow(f'{step}', self.img)
            # cv.waitKey(0)

        for step in self.ROI_DETECTION_STEPS:
            self.img = step.apply(self.img)
            # cv.imshow(f'{step}', self.img)
            # cv.waitKey(0)

        return self.resized_img, self.img

    def __repr__(self) -> str:
        repr = ''
        for stage, step_list in self.STAGES.items():
            repr += f'------- {stage} ------\n'
            for step in step_list:
                repr += str(step) + '     \n'
        return repr
