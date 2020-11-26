#TO DO: ADD ARGPARSE

import cv2 as cv
from biodiv.detection import V1, draw_ROI, display
from argparse import ArgumentParser
from pathlib import Path


def main():
    parser = ArgumentParser()
    parser.add_argument(
        'action', choices=['save', 'show'],
        help='Choose between relabelling all images or just new ones'
    )
    parser.add_argument(
        'path', help='picture to apply detection on'
    )
    parser.add_argument(
        '-o', '--output', default=None,
        help='directory where to save pic_det.png'
    )

    args = parser.parse_args()

    img_pth = Path(args.path)

    if args.action == 'show':
        res_img, ROIs = V1(str(img_pth))
        out = draw_ROI(res_img.copy(), ROIs)

        display(res_img, out)

    elif args.action == 'save':
        res_img, ROIs = V1(str(img_pth))
        out = draw_ROI(res_img.copy(), ROIs)

        if args.output is None:
            out_pth = str(img_pth).split('.')[0] + '_det.png'
            cv.imwrite(out_pth, out)
        else:
            file_name = img_pth.name.split('.')[0] + '_det.png'
            out_pth = Path(args.output) / file_name
            cv.imwrite(str(out_pth), out)


if __name__ == "__main__":
    main()
