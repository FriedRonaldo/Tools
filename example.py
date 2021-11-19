import cv2
from glob import glob
import os
import numpy as np

from utils import concat_img_indir, concat_gridshape, transpose_image, select_images


# create a directory to save the results
res_dir = './results'
os.makedirs(res_dir, exist_ok=True)

#########################
# (EX) concat_img_indir #
#########################

# concatenate all the images in "./imgs/bridge"
concatenated = concat_img_indir('./imgs/bridge')
cv2.imwrite(os.path.join(res_dir, 'concat_img_indir_ex.png'), concatenated)

# concatenate first 10 images in "./imgs/bridge"
concatenated = concat_img_indir('./imgs/bridge', 10)
cv2.imwrite(os.path.join(res_dir, 'concat_img_indir_10_ex.png'), concatenated)

# concatenate vertically first 10 images in "./imgs/bridge"
concatenated = concat_img_indir('./imgs/bridge', 10, True)
cv2.imwrite(os.path.join(res_dir, 'concat_img_indir_10_vertical_ex.png'), concatenated)

# concatenate vertically first 10 images in "./imgs/bridge and resize them into (128, 128)"
concatenated = concat_img_indir('./imgs/bridge', 10, True, 128)
cv2.imwrite(os.path.join(res_dir, 'concat_img_indir_10_vertical_128_ex.png'), concatenated)

#########################
# (EX) concat_gridshape #
#########################

img_dir_list = sorted(glob('./imgs/bridge/*.jpg'))

img_list = [cv2.imread(f) for f in img_dir_list]

img_grid = concat_gridshape(img_list)
cv2.imwrite(os.path.join(res_dir, 'concat_gridshape_ex.png'), img_grid)

# scale down once again
img_grid = concat_gridshape(img_list, 4)
cv2.imwrite(os.path.join(res_dir, 'concat_gridshape_4_ex.png'), img_grid)

# scale down twice again
img_grid = concat_gridshape(img_list, 5)
cv2.imwrite(os.path.join(res_dir, 'concat_gridshape_5_ex.png'), img_grid)

# process with rectangle shaped images
img_list = [np.ones((256, 512, 3)) * (255 // (i + 1)) for i in range(50)]
img_grid = concat_gridshape(img_list)
cv2.imwrite(os.path.join(res_dir, 'concat_gridshape_rect_ex.png'), img_grid)

########################
# (EX) transpose_image #
########################

img = cv2.imread('./results/concat_img_indir_10_ex.png')

img = np.concatenate((img, img), 0)

img_tr = transpose_image(img, img.shape[0])

cv2.imwrite(os.path.join(res_dir, 'transpose_image_ex_org.png'), img)
cv2.imwrite(os.path.join(res_dir, 'transpose_image_ex.png'), img_tr)

######################
# (EX) select_images #
######################

img = cv2.imread('./results/concat_img_indir_10_ex.png')

selected = select_images(img, [0, 7, 9], 256)

img_sel = np.concatenate(selected, 1)

cv2.imwrite(os.path.join(res_dir, 'select_images_ex.png'), img_sel)
