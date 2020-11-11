# NOTE: temporary file to call labelling from terminal
#      should be replaced by main.py

from argparse import ArgumentParser
from pathlib import Path
import re

from biodiv.label import label


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


if __name__ == "__main__":
    main()
