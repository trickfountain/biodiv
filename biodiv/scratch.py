from biodiv.detection import V1

detector = V1
img_src = 'biodiv/tests/test_images/but1.jp2'
img_res, ROIs = detector(img_src)


print(img_res)