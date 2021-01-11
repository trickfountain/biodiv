from matplotlib import pyplot as plt
from pathlib import Path
import cv2 as cv


class pthValidator:

    def __init__(self, img_pth) -> None:
        self.img_pth = img_pth
        self.img_pth = self.load_pth()
        self.validate_pth_points_to_file()

    def load_pth(self):
        pth = Path(self.img_pth)
        return pth

    def validate_pth_points_to_file(self):
        file_exist_flag = self.img_pth.exists()
        if file_exist_flag is False:
            raise ValueError('path provided is not pointing to a file')


class imgValidator:
    VALID_IMG_DTYPE = 'uint8'
    VALID_IMG_CHANNELS = 3

    def __init__(self, img) -> None:
        self.img = img
        self.validate_img()

    def validate_img_dtype(self):
        img_type = self.img.dtype
        if img_type != self.VALID_IMG_DTYPE:
            raise TypeError('Image data does not have valid dtype '
                                 f'expecting: {self.VALID_IMG_DTYPE}')

    def validate_img_channels(self):
        invalid_channels_Error = AssertionError(
            'Image loaded is not in a valid format: expecting RGB image '
            f'with {self.VALID_IMG_CHANNELS} channels')

        try:
            channels = self.img.shape[2]
        except IndexError:
            raise invalid_channels_Error

        if channels != self.VALID_IMG_CHANNELS:
            raise invalid_channels_Error

    def validate_img(self):
        self.validate_img_dtype()
        self.validate_img_channels()


class imgLoader(pthValidator, imgValidator):
    '''This is a helper class to load attributes when instanciating a biodiv img
    '''

    def __init__(self, img_pth) -> None:
        super().__init__(img_pth)
        self.img_name = self.img_pth.name
        self.img = self.load_image()
        imgValidator(self.img)
        self.img_org = self.img.copy()

    def load_image(self):
        '''load image. accepts str or pathlib oject.'''
        img = cv.imread(str(self.img_pth), 1)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        return img


class biodivImg(imgLoader):
    '''
    '''

    def display_img(self, show_original=True):
        '''Display img using cv.imshow.
        Big images will be very big'''

        window = plt.figure(self.img_name, figsize=(8, 6))
        if show_original is False:
            ax = window.add_subplot(111)
            ax.imshow(self.img_org)
            window.suptitle(self.img_name, fontsize=16)

        elif show_original is True:
            ax = window.add_subplot(121)
            ax.imshow(self.img_org)
            ax = window.add_subplot(122)
            ax.imshow(self.img)
            window.suptitle(self.img_name, fontsize=16)

        else:
            raise ValueError('Invalid input for show_original: expecting '
                             'boolean')
        
        plt.show()

    def apply(self, transformerClass):
        '''Applies 'apply' method of given transformerClass

        transformerClass can be individual filters, pipelines, detectors
        etc. They all return a modified version of self.img'''
        self.img = transformerClass.apply(self.img)
