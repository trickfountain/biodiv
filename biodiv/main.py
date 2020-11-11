# Entry point when "using" biodiv
#   this will become sort of a CLI to test functions offline.

from argparse import ArgumentParser
from pathlib import Path
from biodiv.label import label
import cv2 as cv

#NOTE : DOES NOT FUNCTION. PLAN IS TO FOLD LABELLER.PY AND DETECTOR.PY INTO MAIN.PY
#       BUT NOT A PRIORITY FOR NOW

#TODO: transform this into a CLI type parser.
# No need to include detect.
# check if some parts of detect need to be salvaged.

def main():

    parser = ArgumentParser()
    #TODO: remove and replace with --all or --new
    parser.add_argument(
        'action', choices=['detect', 'label'], 
        help='indicate which action to perform: detect or label'
    )
    parser.add_argument(
        'path', help='path to perform action on: file or directory'
    )
 
    args = parser.parse_args()

    # validate path provided
    p = Path(args.path)
    if p.exists() is False:
        raise ValueError('Path provided is not valid')
    elif p.is_dir() is True:
        print('>> Directory detected')
    elif p.is_file() is True:
        print('>> Fil detected')
    else:
        raise ValueError('Path seems to be valid but target is '
                         'not a file or a directory')

    if p.is_dir() is True:
        # TODO: unfinished, want to be able to only labeled new/unlabeled imgs
        labeled = [p.name.replace("_lab", "") for p in p.glob("*_lab.*")]
        excl_pat = ['_res.'] # exclude resized img.
        incl_pat = ['*.jp2', '*.png', '*.jpeg']
        incl_pat.extend([pat.upper() for pat in incl_pat])

        if args.new is True:
            excl_pat.extend(labeled)

        files = []
        for pat in incl_pat:
            matches = p.glob(pat)
            for match in matches:
                fn = match.name.lower()
                if any(pat in fn for pat in excl_pat):
                    pass
                else:
                    files.append(str(match))

        print(f'Detected the following files:\n {files}\n')

    else:
        files = [p]

    if args.action == 'detect':
        # TODO not sure detect is ready for this context
        # follow similar pattern to label, with option to display after each.
        # action = detect
        pass
    elif args.action == 'label':
        action = label

    for img_src in files:
        print(f'------ processing: {img_src} ---------')
        action(img_src)

    print('---- All done ! ----')

    # while True:

    #     # input pars with input
    #     pic_choice = input('Enter the name of the picture found in '
    #                     f'{pic_dir} or q to quit\n')
    #     if pic_choice == 'q':
    #         break

    #     # TODO: validate input
    #     img_src = pic_dir+'/'+pic_choice

    #     try:
    #         img_res, ROIs = V1(img_src)
    #     except ValueError:
    #         print(f"***ERROR*** Could not find {img_src}, try again ?\n")
    #         continue

    #     # TODO: wrap in a function to create nice green rectangles
    #     for roi in ROIs:
    #         tl, br = tuple(roi[0]), tuple(roi[1])
    #         rectangle(img_res, tl, br, 0, 5)

    #     display(img_res)


if __name__ == "__main__":
    main()