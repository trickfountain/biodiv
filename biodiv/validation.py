import cv2 as cv
import numpy as np
from biodiv.detection import detect_ROI, V1, resize_img
from biodiv.utils import find_extContours, display


def cnts_benchmark(img_src, detector=detect_ROI):
    '''Calculate detection recall and precision for a given detector

    Uses pure red (0, 0, 255) dots for labelling. Input expected
      is a color, 3 channels image but where only the dots are colored.

    A detector is the step that takes a pre-processed image and finds
    Regions Of Interests.

    Finds the center of each circle using Moment and checks if
    center is within the bounded rectangle of an ROI.
    '''
    
    img = cv.imread(img_src, 1)
    _, thresh1 = cv.threshold(img, 50, 255, cv.THRESH_BINARY)
    b, _, r = cv.split(thresh1)
    targets = r-b

    t_cnts = find_extContours(targets)
    targets = []
    for i, cnt in enumerate(t_cnts):
        M = cv.moments(cnt)
        cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        targets.append((i, (cx, cy)))

    detected = detector(b)

    det_cnts = []
    for i, (tl, br) in enumerate(detected):
        canvas = np.zeros(img.shape[0:2], np.uint8)
        cv.rectangle(canvas, tuple(tl), tuple(br), 255, 3)
        cnts = find_extContours(canvas)
        det_cnts.append((i, cnts[0]))

    matches = []
    for det_id, roi_cnt in det_cnts:
        for target_id, center in targets:
            result = cv.pointPolygonTest(roi_cnt, center, False)
            if result == 1:
                matches.append((det_id, target_id))

    tot_matches = len(matches)
    un_matches = len(set([tup[1] for tup in matches]))
    tot_targets = len(targets)
    tot_cnts = len(det_cnts)
    recall = un_matches/len(targets)*100 if tot_matches else 0
    precision = un_matches/len(det_cnts)*100 if det_cnts else 0

    results = {
        'recall': recall,
        'precision': precision,
        'tot_matches': tot_matches,
        'un_matches': un_matches,
        'tot_targets': tot_targets,
        'tot_cnts': tot_cnts
    }

    return results

# TODO: det_benchmark and cnts_benchmark should probably be the
# the same function, just confused about which function should return what.


def det_benchmark(img_src, img_lab, detector=V1):
    # TODO: docstring prob needs fixing
    '''Calculate detection recall and precision for a given detector

    Uses pure red (0, 0, 255) dots for labelling. Input expected
      is a color, 3 channels image but where only the dots are colored.

    A detector is the step that takes a pre-processed image and finds
    Regions Of Interests.

    Finds the center of each circle using Moment and checks if
    center is within the bounded rectangle of an ROI.
    '''

    img_res, ROIs = detector(img_src)
    img_res_width = img_res.shape[1]
    img_lab = cv.imread(img_lab, 1)
    img_lab = resize_img(img_lab, img_res_width)
    img_lab = cv.cvtColor(img_lab, cv.COLOR_RGB2BGR)
    _, thresh1 = cv.threshold(img_lab, 50, 255, cv.THRESH_BINARY_INV)
    b, _, r = cv.split(thresh1)
    dots = r-b
    t_cnts = find_extContours(dots)

    targets = []
    for i, cnt in enumerate(t_cnts):
        M = cv.moments(cnt)
        cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        targets.append((i, (cx, cy)))

    det_cnts = []
    for i, (tl, br) in enumerate(ROIs):
        canvas = np.zeros(img_res.shape[0:2], np.uint8)
        cv.rectangle(canvas, tuple(tl), tuple(br), 255, -1)
        contours = find_extContours(canvas)
        det_cnts.append((i, contours[0]))

    matches = []
    for det_id, roi_cnt in det_cnts:
        for target_id, center in targets:
            result = cv.pointPolygonTest(roi_cnt, center, False)
            if result == 1:
                matches.append((det_id, target_id))

    tot_matches = len(matches)
    un_matches = len(set([tup[1] for tup in matches]))
    tot_targets = len(targets)
    tot_cnts = len(det_cnts)
    recall = un_matches/len(targets)*100 if tot_matches else 0
    precision = un_matches/len(det_cnts)*100 if det_cnts else 0

    results = {
        'recall': recall,
        'precision': precision,
        'tot_matches': tot_matches,
        'un_matches': un_matches,
        'tot_targets': tot_targets,
        'tot_cnts': tot_cnts
    }

    return results


if __name__ == "__main__":
    # img_src = 'biodiv/tests/test_images/cats1.jp2'
    # img_lab = 'biodiv/tests/test_images/cats1_bw_lab.jp2'

    img_src = 'biodiv/tests/test_images/but1.jp2'
    img_lab = 'biodiv/tests/test_images/but1_lab.jp2'
    print(det_benchmark(img_src, img_lab))


