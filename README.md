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
![concat_gridshape_rect_ex](https://user-images.githubusercontent.com/23406491/142562393-5d2de030-d9dc-4882-a90a-54cf5c21ab64.png)


## concat_img_indir(path, num_imgs, is_vertical, resize)
### Example
| Parameter | Description |
|---|---|
| path | **str** a directory containing images to concatenate |
| num_imgs | **int** if specified, concat first "num_imgs" images only |
| is_vertical | **bool** if True, concatenate along height |
| resize | **int** if not None, all the images will be resized to "(resize, resize)" |

```
import cv2
from glob import glob
import os
import numpy as np

from utils import concat_img_indir


# create a directory to save the results
res_dir = './results'
os.makedirs(res_dir, exist_ok=True)

# concatenate first 10 images in "./imgs/bridge"
concatenated = concat_img_indir('./imgs/bridge', 10)
cv2.imwrite(os.path.join(res_dir, 'concat_img_indir_10_ex.png'), concatenated)

# concatenate vertically first 10 images in "./imgs/bridge"
concatenated = concat_img_indir('./imgs/bridge', 10, True)
cv2.imwrite(os.path.join(res_dir, 'concat_img_indir_10_vertical_ex.png'), concatenated)

# concatenate vertically first 10 images in "./imgs/bridge and resize them into (128, 128)"
concatenated = concat_img_indir('./imgs/bridge', 10, True, 128)
cv2.imwrite(os.path.join(res_dir, 'concat_img_indir_10_vertical_128_ex.png'), concatenated)
```

### Result

* Images are from [DiffAug](https://github.com/mit-han-lab/data-efficient-gans).

Because I copied the images to conduct a 5-scale grid-shaped concatenation, the image below contains an image multiple times.

![concat_img_indir_10_ex](https://user-images.githubusercontent.com/23406491/142562463-74a3ea67-6748-42f0-937a-3dbbb8f84459.png)

