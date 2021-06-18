import os
from glob import glob
import cv2
import numpy as np


def concat_img_indir(path, is_vertical=False):
    """
    :param path: a directory containing images to concatenate
    :param is_vertical: if True, concatenate along height
    :return: a concatenated image
    Example:
    prefix = './photo2ukiyoe/'
    print(sorted(os.listdir(prefix)))
    taget_dirs = sorted(os.listdir(prefix))

    print(taget_dirs)

    for target in taget_dirs:
        cur = os.path.join(prefix, target)
        res = concat_img_indir(cur, False)
        if res is None:
            continue
        cv2.imwrite('{}.png'.format(target), res)
    """
    img_dir_list = sorted(glob(os.path.join(path, '*.png'))) + sorted(glob(os.path.join(path, '*.jpg')))

    img_dir_list = img_dir_list

    if len(img_dir_list) <= 0:
        return None

    concat_dim = 0 if is_vertical else 1

    result = None
    for img_dir in img_dir_list:
        img_ = cv2.imread(img_dir)

        img_ = cv2.resize(img_, (128, 128))

        if result is None:
            result = img_.copy()
        else:
            result = np.concatenate((result, img_), concat_dim)

    return result
