"""
This script perform the preprocessing to te image -
from thin handwrite it become more real and natural -
erosion and the gaussian filter 3x3
"""

import random
import os
import pickle as pkl
import numpy as np
from scipy.misc.pilutil import imread, imresize, imsave, imshow
from PIL import Image, ImageOps
import scipy
from scipy.ndimage import gaussian_filter
import cv2

image_path = "/home/inbarnoa/Pictures/try1.jpg"
input_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
kernel = np.ones((3, 3), np.uint8)
img_erosion = cv2.dilate(input_image, kernel, iterations=1)
gaus_eros = scipy.ndimage.gaussian_filter(img_erosion, 1)
cv2.imwrite('/home/inbarnoa/PycharmProjects/MathSolver/exampelsForPresentation/tmp1.bmp', gaus_eros)

close_flag = 1

print('success =)')
