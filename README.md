# Image processing tools

| Function | Description |
|---|---|
| [concat_gridshape](#concat_gridshapeimg_list-num_scales) | **list** containing numpy array images read by cv2.imread|


## concat_gridshape(img_list, num_scales)
### Example
| Parameter | Description |
|---|---|
| img_list | **list** list of numpy array images read by cv2.imread |
| num_scales | **int** total number of different scales to downscale |

```
from utils import concat_gridshape
import cv2
from glob import glob
import os


res_dir = './result'
os.makedirs(res_dir, exist_ok=True)

data_list = ['obama',]

for data in data_list:
    img_dir_list = sorted(glob(os.path.join('./data', data, '100', '*.jpg')))
    img_list = []
    for img_dir in img_dir_list:
        img_list.append(cv2.imread(img_dir))

    grid = concat_gridshape(img_list)

    cv2.imwrite(os.path.join(res_dir, 'grid_{}.png'.format(data)), grid)
```
### Result

* Obama images are from [DiffAug](https://github.com/mit-han-lab/data-efficient-gans)

![grid_obama](https://user-images.githubusercontent.com/23406491/138026142-dba459d0-250d-4a69-9b4b-2989a77b05ce.png)
