import numpy as np
from biodiv.detection import roiDrawer
import pytest
import cv2 as cv


# class TestResize_img():
#     def test_img_happy(self):
#         '''Test if (800,800) image is resized appropriately
#         '''
#         img = np.zeros( (800, 800), dtype=np.uint8)
#         res = resize_img(img, resize_width=400)

#         assert res.shape[1] == 400

#     def test_input(self):
#         '''Check that proper error is thrown if provided with
#         wrong input type.
#         '''
#         img = 'path/to/pic'
#         with pytest.raises(ValueError) as e:
#             resize_img(img)

#         assert 'img should be of format' in str(e.value)


# class Testpp_Img():

#     def test_input_e(self):
#         # input strictly has to be of dtype np.uint8
#         img = np.array((800, 800), dtype=np.uint32)
#         with pytest.raises(ValueError) as e:
#             pp_img(img)

#         assert 'Expecting np.array' in str(e.value)

#     def test_grayScale_happy(self):
#         '''Check that grayscale image is processed and 
#         grayscale on output
#         '''
#         img = np.array((800, 800), dtype=np.uint8)
#         pp = pp_img(img)

#         assert pp.ndim == 2

#     def test_3Chan_happy(self):
#         '''Check that 3 color channel image is transformed in grayscale
#         during pre-processing
#         '''
#         img = np.array((800, 800, 3), dtype=np.uint8)
#         pp = pp_img(img)

#         assert pp.ndim == 2


#TODO: Not surue if I need to use fixtures here.
# Also the code below should probably be less modular.
# Also confirm real quick that img_100_x_200 does give you
# x = 100, y = 200
# You have to make sure that cv.imRead, cv.imWrite and biodivImg display are
# all in sync for x, y coordinates.

@pytest.fixture()
def img_100_x_200():
    # Numpy uses axis 0 for column, 1 for rows: so array is height, width
    img = np.zeros((200, 100, 3), dtype='uint8')

    return img

@pytest.fixture()
def img_five_shapes():
    img_src = 'biodiv/tests/test_images/five_shapes.png'
    img = cv.imread(img_src, 1)

    return img

@pytest.fixture()
def drawer(img_100_x_200):
    args = {
        'ROI_MIN_SIZE': 2.0,
        'ROI_MARGIN': 5.0,
        'BORDER_PADDING': 1.0,
        'ROI_BOX_RGB_COLOR': (0, 255, 0),
    }
    drawer = roiDrawer(**args)
    drawer._load_img(img_100_x_200)

    return drawer

@pytest.fixture()
def contour(img_100_x_200):
    #TODO: mock contour.
    # Each individual contour is a Numpy array of (x,y) coordinates
    # of boundary points of the object.
    top_left, bottom_right = (20, 20), (60, 100)
    img = img_100_x_200
    cv.rectangle(img, top_left, bottom_right, (255, 255, 255), -1)
    contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contour = contours[0]

    return contour


class TestroiDrawer:

    def test_frame_width_no_effect(self, drawer):
        input_x, input_y = (80, 150)
        out_x, out_y = drawer._frame_width((input_x, input_y))

        assert input_x == out_x
        assert input_y == out_y

    def test_frame_width_overshoot(self, drawer):
        input_x, input_y = (105, 150)
        out_x, out_y = drawer._frame_width((input_x, input_y))

        padding = drawer.BORDER_PADDING
        test_img_width = drawer.width
        expected_out_x = test_img_width - padding

        assert out_x == expected_out_x
        assert out_y == input_y

    def test_frame_width_undershoot(self, drawer):
        input_x, input_y = (-40, 150)
        out_x, out_y = drawer._frame_width((input_x, input_y))
        padding = drawer.BORDER_PADDING
        expected_out_x = 0 + padding

        assert out_x == expected_out_x
        assert out_y == input_y

    def test_frame_height_no_effect(self, drawer):
        input_x, input_y = (40, 150)
        out_x, out_y = drawer._frame_height((input_x, input_y))

        assert input_x == out_x
        assert input_y == out_y

    def test_frame_height_overshoot(self, drawer):
        input_x, input_y = (40, 205)
        out_x, out_y = drawer._frame_height((input_x, input_y))

        padding = drawer.BORDER_PADDING
        test_image_height = drawer.height
        expected_y = test_image_height - padding

        assert out_x == input_x
        assert out_y == expected_y

    def test_frame_height_undershoot(self, drawer):
        input_x, input_y = (40, -20)
        out_x, out_y = drawer._frame_height((input_x, input_y))
        padding = drawer.BORDER_PADDING
        expected_out_y = 0 + padding

        assert out_x == input_x
        assert out_y == expected_out_y

    def test_frame_coord_no_effect(self, drawer):
        input_x, input_y = (40, 150)
        out_x, out_y = drawer._frame_coord((input_x, input_y))

        assert input_x == out_x
        assert input_y == out_y

    def test_frame_coord_overshoot(self, drawer):
        input_x, input_y = (150, 235)
        out_x, out_y = drawer._frame_coord((input_x, input_y))

        padding = drawer.BORDER_PADDING
        test_image_height = drawer.height
        test_image_widht = drawer.width
        expected_x = test_image_widht - padding
        expected_y = test_image_height - padding

        assert out_x == expected_x
        assert out_y == expected_y

    def test_frame_coord_undershoot(self, drawer):
        input_x, input_y = (-15, -50)
        out_x, out_y = drawer._frame_coord((input_x, input_y))

        padding = drawer.BORDER_PADDING
        expected_x = padding
        expected_y = padding

        assert out_x == expected_x
        assert out_y == expected_y

    def test_bottom_right_from_contour(self, drawer,  img_100_x_200):
        img = drawer.img
        top_left, bottom_right = (20, 20), (60, 100)
        cv.rectangle(img, top_left, bottom_right, 255, -1)

        contours, _ = cv.findContours(img, cv.RETR_EXTERNAL,
                                      cv.CHAIN_APPROX_SIMPLE)
        contour = contours[0]
        drawer_bottom_right = drawer._bottom_right_from_contour(contour)

        # Drawing the rectangle adds 1 pixel to the size of the contour
        expected_x = 1 + bottom_right[0] + drawer.margin_px
        expected_y = 1 + bottom_right[1] + drawer.margin_px
        expected_bottom_right = expected_x, expected_y

        assert drawer_bottom_right == expected_bottom_right

    def test_bottom_left_from_contour(self, drawer):
        img = drawer.img
        top_left, bottom_right = (20, 20), (60, 100)
        cv.rectangle(img, top_left, bottom_right, 255, -1)

        contours, _ = cv.findContours(img, cv.RETR_EXTERNAL,
                                      cv.CHAIN_APPROX_SIMPLE)
        contour = contours[0]
        drawer_top_left = drawer._top_left_from_contour(contour)

        expected_x = top_left[0] - drawer.margin_px
        expected_y = top_left[1] + drawer.margin_px
        expected_top_left = expected_x, expected_y

        assert drawer_top_left == expected_top_left

    def test_calculate_ROI_zone(self, drawer):
        img = drawer.img
        top_left, bottom_right = (20, 20), (60, 100)
        cv.rectangle(img, top_left, bottom_right, 255, -1)

        contours, _ = cv.findContours(img, cv.RETR_EXTERNAL,
                                      cv.CHAIN_APPROX_SIMPLE)
        contour = contours[0]

        # Drawing the rectangle adds 1 pixel to the size of the contour
        width = 50.0 + 1.0
        height = 80.0 + 1.0
        expected_area = width * height
        roi_area = drawer._calculate_ROI_zone(contour)

        assert roi_area == expected_area

    def test_qualify_ROI_OK(self, drawer):
        img = drawer.img
        top_left, bottom_right = (20, 20), (60, 100)
        cv.rectangle(img, top_left, bottom_right, 255, -1)

        contours, _ = cv.findContours(img, cv.RETR_EXTERNAL,
                                      cv.CHAIN_APPROX_SIMPLE)
        
        valid_contours = drawer._qualify_ROI(contours)

        assert len(valid_contours) == 1

    def test_qualify_ROI_too_small(self, drawer):
        img = drawer.img
        top_left, bottom_right = (20, 20), (25, 25)
        cv.rectangle(img, top_left, bottom_right, 255, -1)

        contours, _ = cv.findContours(img, cv.RETR_EXTERNAL,
                                      cv.CHAIN_APPROX_SIMPLE)
        
        valid_contours = drawer._qualify_ROI(contours)

        assert len(valid_contours) == 0

    #TODO: no test for detect_ROI
    def test_detect_ROI_happy_path(self, drawer, img_five_shapes):
        drawer._load_img(img_five_shapes)
        drawer.detect_ROI()
        out = drawer.region_of_interest
        assert len(out) == 5

    def test_draw_ROI_happy_path(self, drawer):
        regions = [((10, 10), (60, 100))]
        drawer.region_of_interest = regions
        img_with_drawing = drawer.draw_ROI()

        color = drawer.ROI_BOX_RGB_COLOR

        for roi in regions:
            tl, br = roi
            # x, y coordinate is array[y, x] in numpy
            rgb_at_top_left = img_with_drawing[tl[1], tl[0]]
            rgb_at_bottom_right = img_with_drawing[br[1], br[0]]
            
            check_color_top_left = rgb_at_top_left == color
            check_color_bottom_right = rgb_at_bottom_right == color

            assert check_color_top_left.all()
            assert check_color_bottom_right.all()

    #TODO: test when no region is detected. How should it act ?
    def test_draw_ROI_no_region(self, drawer):
        pass