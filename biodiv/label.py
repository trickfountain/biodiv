# taken from https://automaticaddison.com/how-to-annotate-images-using-opencv/
import cv2 as cv


def label(img_src):
    """Use mouse callback to add red dot on img

    Saves a copy of the image with _lab added to the name
      in the same directory than original.
    """

    output_fn = img_src.split('.')[0] + "_lab." + img_src.split('.')[1]
    img = cv.imread(img_src, 1)

    param = {'img': img}
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.setMouseCallback('image', draw_circle, param)

    print('q: quit. s: save & quit')
    while True:
        key = cv.waitKey(1) & 0xFF
        cv.imshow('image', img)
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv.imwrite(output_fn, img)
            break
    cv.destroyAllWindows()


def draw_circle(event, x, y, _, param):
    """
    Draws dots on clicking on left mouse button
    """
    img = param['img']
    pic_area = img.size
    c_area = pic_area / 300
    radius = round((c_area / 3.14159)**0.5)

    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img, (x, y), radius, (0, 0, 255), -1)

