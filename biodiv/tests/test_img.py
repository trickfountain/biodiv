
from pathlib import Path
import pathlib
from biodiv.img import biodivImg, imgLoader, imgValidator, pthValidator
import pytest
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from unittest.mock import Mock

#TODO: Should have valid path and valid image as part of fixtures
# or overall configs.

@pytest.fixture(scope="module")
def valid_img_pth():
    return 'biodiv/tests/test_images/five_shapes.png'

@pytest.fixture(scope="module")
def valid_img(valid_img_pth):
    return cv.imread(valid_img_pth, 1)

@pytest.fixture(scope='module')
def pure_red_img_pth():
    return 'biodiv/tests/test_images/pure_red.png'


class TestPthValidator:
    # setup
    invalid_pth = 12345
    valid_pth_points_to_nothing = './test_images/seven_shapes.png'

    def test_happy_path_str(self, valid_img_pth):
        input_pth = valid_img_pth
        pth_validator = pthValidator(input_pth)
        assert isinstance(pth_validator.img_pth, Path)

    def test_happy_path_Path(self, valid_img_pth):
        input_pth = Path(valid_img_pth)
        pth_validator = pthValidator(input_pth)
        assert isinstance(pth_validator.img_pth, Path)

    def test_pth_points_to_nothing(self):
        with pytest.raises(ValueError) as e:
            pthValidator(self.valid_pth_points_to_nothing)

        assert "not pointing to a file" in str(e.value)

    def test_invalid_pth(self):
        with pytest.raises(TypeError) as e:
            pthValidator(self.invalid_pth)

        assert 'expected str' in str(e.value)


class TestimgValidator:

    def test_validate_img_happy_path(self, valid_img):
        validator = imgValidator(valid_img)
        validator.validate_img()

        assert True

    def test_validate_img_dtype(self):
        invalid_img_dtype = np.zeros((600, 800, 3), dtype='int8')

        with pytest.raises(TypeError) as e:
            imgValidator(invalid_img_dtype)

        assert "not have valid dtype" in str(e.value)

    def test_validate_img_channels_grayscale(self, valid_img_pth):
        invalid_img_grayscale = cv.imread(valid_img_pth, cv.IMREAD_GRAYSCALE)

        with pytest.raises(AssertionError) as e:
            imgValidator(invalid_img_grayscale)

        assert 'expecting RGB image with 3 channels' in str(e.value)

    def test_validate_img_channels_RGBA(self, valid_img):
        invalid_img_channels_RGBA = cv.cvtColor(valid_img, cv.COLOR_BGR2BGRA)
        
        with pytest.raises(AssertionError) as e:
            imgValidator(invalid_img_channels_RGBA)

        assert 'expecting RGB image with 3 channels' in str(e.value)


class TestimgLoader:
    
    def test_happy_path(self, valid_img_pth):
        loader = imgLoader(valid_img_pth)

        assert isinstance(loader.img_name, str)
        assert isinstance(loader.img, np.ndarray)
        assert isinstance(loader.img_pth, pathlib.Path)

    def test_load_RGB(self, pure_red_img_pth):
        loader = imgLoader(pure_red_img_pth)
        # cv assumes BGR, our program assumes RBG
        r, b, g = cv.split(loader.img)

        assert np.max(r) == 255
        assert np.max(b) == 0
        assert np.max(g) == 0


class TestbiodivImg:

    def test_happy_path(self, valid_img_pth):
        biodivImg(valid_img_pth)
        assert True        

    def test_diplay_img(self, valid_img_pth):
        #TODO: mock plt.show() instead
        img = biodivImg(valid_img_pth)
        plt.show = Mock()

        img.display_img()

        plt.show.assert_called_once()