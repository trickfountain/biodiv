# taken from https://automaticaddison.com/how-to-annotate-images-using-opencv/
from argparse import ArgumentParser
from pathlib import Path
import re

import cv2 as cv


def main():

    parser = ArgumentParser()
    parser.add_argument(
        'label_type', choices=['all', 'new'],
        help='Choose between relabelling all images or just new ones'
    )
    parser.add_argument(
        'path', help='path to perform action on: accepts file & directory'
    )
    args = parser.parse_args()

    # validate path provided
    pth = Path(args.path)
    if pth.exists() is False:
        raise ValueError('Path provided is not valid')

    elif pth.is_dir() is True:
        files = [str(pth) for pth in pth.iterdir()]

        # All files with valid extension that do not have _lab
        src_p = re.compile(r'.*(?<!_lab)\.(png|jp2|jpeg)', re.IGNORECASE)
        # All files with valid extension AND _lab
        lab_p = re.compile(r'(.*)(_lab)\.(png|jp2|jpeg)', re.IGNORECASE)

        src_match = [src_p.match(f)for f in files if src_p.match(f)]
        src_files = [m.string for m in src_match]

        flag = args.label_type
        if flag == 'all':
            files = src_files

        elif flag == 'new':
            matches = [lab_p.match(f)for f in files if lab_p.match(f)]
            lab_files = [m.string.replace("_lab", "") for m in matches]
            new_files = list(set(src_files).difference(set(lab_files)))
            files = new_files

    elif pth.is_file() is True:
        files = [pth]

    else:
        raise ValueError('Path is valid but does not seem to be a file or directory')

    for img_src in files:
        print(f'------ processing: {img_src} ---------')
        label(img_src)

    print('---- Labelling completed ----')


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


if __name__ == "__main__":
    main()
