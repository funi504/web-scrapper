import requests
from PIL import Image
from io import BytesIO
import imagehash
import cv2
import numpy as np
from skimage.transform import resize



image_url = 'https://m.media-amazon.com/images/I/71T2YWfY+xL._AC_UL320_.jpg'
image_url3 = 'https://m.media-amazon.com/images/I/81QHa5P3fZL._AC_UL320_.jpg'
image_url2 ='https://shop.medindia.com/content/images/thumbs/0001450_morpheme-memocare-plus-for-mental-alertness-500mg-extract-60-veg-capsules-2-bottles_300.jpeg'

# with skimage (you can also use PIL or cv2)


shape = image_url.shape
image_url3_resized = resize(image_url3, shape)


