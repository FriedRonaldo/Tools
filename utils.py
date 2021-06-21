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


def transpose_image(img, img_size, num_rows, num_cols):
    # assume that the padding is zero (no padding)
    img_sep = []
    for r in range(num_rows):
        for c in range(num_cols):
            tmp = img[r * img_size: (r + 1) * img_size, c * img_size: (c + 1) * img_size, :]
            img_sep.append(tmp)
    res = None
    for c in range(num_cols):
        row_img = None
        for r in range(num_rows):
            idx = c + r * num_cols
            row_img = img_sep[idx].copy() if row_img is None else np.concatenate((row_img, img_sep[idx]), 1)
        res = row_img.copy() if res is None else np.concatenate((res, row_img), 0)
    return res


def select_images(img_tot, idx_to_pick, img_size):
    res = []

    num_imgs = img_tot.shape[1] // img_size
    print(num_imgs)
    for i in range(num_imgs):
        if i in idx_to_pick:
            res.append(img_tot[:, i * img_size: (i + 1) * img_size, :])

    return res


def concat_gridshape(img_list, num_scales=3):
    tot_num_imgs = 2**((num_scales-1) * 2)

    assert tot_num_imgs < len(img_list)

    res = None
    img_cnt = 0
    for i in range(num_scales):
        num_img_at_scale = 2**(i*2)
        img_to_use = img_list[img_cnt:img_cnt + num_img_at_scale]

        scale = (1/2)**i
        nrows = 2 ** i

        scale_img = None
        img_idx = 0
        for r in range(nrows):
            row_img = None
            for c in range(nrows):
                img_to_cat = cv2.resize(img_to_use[img_idx], None, fx=scale, fy=scale)
                row_img = img_to_cat.copy() if row_img is None else np.concatenate((row_img, img_to_cat), 1)
                img_idx += 1
            scale_img = row_img.copy() if scale_img is None else np.concatenate((scale_img, row_img), 0)

        res = scale_img.copy() if res is None else np.concatenate((res, scale_img), 1)

        img_cnt += num_img_at_scale

    return res


