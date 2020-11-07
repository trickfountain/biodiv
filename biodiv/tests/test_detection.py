import numpy as np
from biodiv.detection import resize_img, pp_img
import pytest


class TestResize_img():
    def test_img_happy(self):
        '''Test if (800,800) image is resized appropriately
        '''
        img = np.zeros( (800, 800), dtype=np.uint8)
        res = resize_img(img, resize_width=400)

        assert res.shape[1] == 400

    def test_input(self):
        '''Check that proper error is thrown if provided with
        wrong input type.
        '''
        img = 'path/to/pic'
        with pytest.raises(ValueError) as e:
            resize_img(img)

        assert 'img should be of format' in str(e.value)


class Testpp_Img():

    def test_input_e(self):
        # input strictly has to be of dtype np.uint8
        img = np.array((800, 800), dtype=np.uint32)
        with pytest.raises(ValueError) as e:
            pp_img(img)

        assert 'Expecting np.array' in str(e.value)

    def test_grayScale_happy(self):
        '''Check that grayscale image is processed and 
        grayscale on output
        '''
        img = np.array((800, 800), dtype=np.uint8)
        pp = pp_img(img)

        assert pp.ndim == 2
    def test_3Chan_happy(self):
        '''Check that 3 color channel image is transformed in grayscale
        during pre-processing
        '''
        img = np.array((800, 800, 3), dtype=np.uint8)
        pp = pp_img(img)

        assert pp.ndim == 2

class TestV1():
    
    def test_V1_shapes(self):
        pic = "biodiv/tests/test_images/five_shapes.png"
        
        pass