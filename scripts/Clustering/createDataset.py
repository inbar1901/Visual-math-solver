"""
This file is used by clustering.py
it receive a folder and the figure name -
resize to 11x11, and creates 2 arrays, one of images class(type) names and one of the images themself.
"""
import os
import cv2
import numpy as np
import scipy
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

# creating array of numbers images and there labels
def create_dataset(img_folder, class_name):
    img_data_array = []
    class_names = []
    IMG_HEIGHT = 11
    IMG_WIDTH = 11

    for file in os.listdir(img_folder):
        image_path = os.path.join(img_folder, file)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # fitting the new number to model characteristics
        ret, thresh1 = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((3, 3), np.uint8)
        img_erosion = cv2.dilate(thresh1, kernel, iterations=1)
        gaus_eros = scipy.ndimage.gaussian_filter(img_erosion, 1)
        image = cv2.resize(gaus_eros, (IMG_HEIGHT, IMG_WIDTH), interpolation=cv2.INTER_AREA)
        plt.imshow(image)
        image = np.array(image)
        image = image.astype('float32')
        image = image.reshape((-1))

        img_data_array.append(image)
        class_names.append(class_name)
    return img_data_array, class_names

#
# # extract the image array and class name
# img_data, class_name = create_dataset( r'/home/inbarnoa/PycharmProjects/MathSolver/DataSet/DataSetNumbers/extracted_images', '9')