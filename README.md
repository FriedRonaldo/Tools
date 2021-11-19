# Image processing tools

| Function | Description |
|---|---|
| [concat_gridshape](#concat_gridshapeimg_list-num_scales) | **list** containing numpy array images read by cv2.imread|
| [concat_img_indir](#concat_img_indirpath-num_imgs-is_vertical-resize) | **np.array** numpy array image|


## concat_gridshape(img_list, num_scales)
### Example
| Parameter | Description |
|---|---|
| img_list | **list** list of numpy array images read by cv2.imread |
| num_scales | **int** total number of different scales to downscale |

```
import cv2
from glob import glob
import os
import numpy as np

from utils import concat_gridshape


res_dir = './results'
os.makedirs(res_dir, exist_ok=True)

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
```
### Result

* Images are from [DiffAug](https://github.com/mit-han-lab/data-efficient-gans)

![concat_gridshape_ex](https://user-images.githubusercontent.com/23406491/142562001-23337034-0a82-4867-ba5f-3bb9f87e2214.png)
![concat_gridshape_4_ex](https://user-images.githubusercontent.com/23406491/142562009-aa3ad864-25eb-4bed-88b5-8ca8d9cefa41.png)
![concat_gridshape_5_ex](https://user-images.githubusercontent.com/23406491/142562014-2424e7b5-af6d-4bb4-adc4-429ecad88c7c.png)



## concat_img_indir(path, num_imgs, is_vertical, resize)
hi
