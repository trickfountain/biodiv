#TO DO: ADD ARGPARSE

import cv2 as cv
from biodiv.detection import V1, draw_ROI, display
from argparse import ArgumentParser


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
        '-o', '--output', default=None
    )

    # TODO: add -o --output to define output path.
    args = parser.parse_args()

    if args.action == 'show':
        pic = args.path
        res_img, ROIs = V1(pic)
        out = draw_ROI(res_img.copy(), ROIs)

        display(res_img, out)

    elif args.action == 'save':
        pic = args.path
        res_img, ROIs = V1(pic)
        out = draw_ROI(res_img.copy(), ROIs)

        if args.output is None:
            cv.imwrite(pic.split('.')[0] + '_det.'
                       + pic.split('.')[1], out)
        else:
            cv.imwrite(args.output, out)


if __name__ == "__main__":
    main()
