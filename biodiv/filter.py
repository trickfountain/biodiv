import cv2 as cv


class imgFilter:
    ARGS = None
    
    def __init__(self, **kwargs):
        self.ARGS.update(kwargs)
        self.__dict__.update(self.ARGS)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}\n'\
               f'    arguments:  {self.ARGS}'


class imgResizer(imgFilter):
    ARGS = {
        'resize_factor': 0.5,
        'width': None
    }

    def apply(self, img):
        '''resize self.img proportionnaly, in place

        Defaults to resize_factor = 0.5, will use width as final width
        if supplied.'''

        if self.width is not None:
            self.resize_factor = self.width/img.shape[1]

        width = int(img.shape[1] * self.resize_factor)
        height = int(img.shape[0] * self.resize_factor)
        dim = (width, height)
        img = cv.resize(img, dim, interpolation=cv.INTER_CUBIC)
        return img


class medBlurrer(imgFilter):
    ARGS = {
        'ksize': 5
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_ksize()

    def _validate_ksize(self):
        if self.ksize % 2 == 0:
            raise ValueError('Invalid value for ksize: cv.medianBlur only accepts'\
                             ' odd values for ksize ')

    def apply(self, img):
        return cv.medianBlur(img, self.ksize)


class otsuThresholder(imgFilter):
    ARGS = {
        'thresh': 0,
        'maxval': 255,
        'thresh_type': cv.THRESH_BINARY + cv.THRESH_OTSU
    }

    def apply(self, img):
        ## TODO: this is broken, need to add function that checks if
        # input is grayscale and also cvt if not.
        # output of filters should always be the same ie. RGB.
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        _, img = cv.threshold(img, self.thresh, self.maxval, self.thresh_type)
        img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
        return img


class pyramidMeanShiftFilter(imgFilter):
    ARGS = {
        'pmsf_par': (21, 21)
    }

    def apply(self, img):
        # TODO: check if pmsf can be done on gray image, the two conversions are prob
        # useless.
        # TODO: conversions to gray and color should be inherited anyways
        #color_img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
        img = cv.pyrMeanShiftFiltering(img, self.pmsf_par[0],
                                            self.pmsf_par[1])
        #gray_img = cv.cvtColor(pmsf_img, cv.COLOR_RGB2GRAY)
        return img