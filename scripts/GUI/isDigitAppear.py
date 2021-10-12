"""
This file is used in te GUI, only for digit only equation
input - equation (str), solution (str) and the image of equation
it use the find_figures_in_eq, if the figure appear it take a figure from the same group and if not it create a random figure -
but verify that all figures will be from the same group.
the output is the full image with solution tnd equation
"""
import os
import random
import numpy as np
from findFiguresInEq import find_figures_in_eq
from matchGroup import matchGroup
import cv2
import scipy
from PIL import Image
import matplotlib.pyplot as plt

def isDigitAppear (equation, sol:str, img):
    digits_bb, mean_spacing_x, mean_spacing_y, mean_height = find_figures_in_eq(equation, img)
    number_group = np.full(10,-1)
    run_number = 18
    model_path = r'/home/inbarnoa/PycharmProjects/MathSolver/clustering_model'

    current_width = img.shape[1]
    pic_height = img.shape[0]
    pic_width = (len(sol) * (mean_height+mean_spacing_x+5)) + current_width

    pic = np.zeros((pic_height,pic_width ), dtype=np.uint8)
    #pic = np.array(Image.new(mode='1', size=(pic_width, pic_height)))
    pic[:,0:current_width] = img
    plt.imshow(pic)

    # generating the solution image only for numbers
    for idx,char in enumerate(sol):
        if int(sol)<0 and idx==0: # if sol in negative first digit is minus
            random_img_path = r'/home/inbarnoa/PycharmProjects/MathSolver/DataSet/DataSetNumbers/extracted_images/-/-_1350.jpg'
            random_image = cv2.imread(random_img_path, cv2.IMREAD_GRAYSCALE)
            ret, thresh1 = cv2.threshold(random_image, 200, 255, cv2.THRESH_BINARY_INV)
            kernel = np.ones((3, 3), np.uint8)
            img_erosion = cv2.dilate(thresh1, kernel, iterations=1)
            random_img = scipy.ndimage.gaussian_filter(img_erosion, 1)
        else:
            char_Firstlocation = str(equation).find(char)
            if char_Firstlocation != -1 and number_group[int(char)] == -1: # the digit is in the equation and it is the first time the digit appear
                BB = digits_bb[char_Firstlocation][1]
                cropImg = img[:,BB[0]:BB[1]]
                random_img,group = matchGroup(char, cropImg, run_number)
                number_group[int(char)] = group

            else: # the digit appeared already or the digit is not in the equation
                if number_group[int(char)] == -1:
                    number_group[int(char)] = random.randrange(0,9,1)
                kmeans_data_path = model_path + '/imageKmeanData' + char + '_run' + str(run_number) + '.txt'
                imageKmeansData = open(kmeans_data_path)
                imageKmeansData = imageKmeansData.readlines()
                matched_lines = [line for line in imageKmeansData if
                                 "Kmeans Label: " + str(number_group[int(char)]) in line]
                random_image_in_group = random.choice(matched_lines)
                random_image_in_group = random_image_in_group.split()[2]
                random_image_in_group_path = r'/home/inbarnoa/PycharmProjects/MathSolver/DataSet/DataSetNumbers/extracted_images/' + char + '/' + random_image_in_group

                # importing the new number
                random_image = cv2.imread(random_image_in_group_path, cv2.IMREAD_GRAYSCALE)

                # fitting the new number to model characteristics - needed only on original photos
                ret, thresh1 = cv2.threshold(random_image, 200, 255, cv2.THRESH_BINARY_INV)
                kernel = np.ones((3, 3), np.uint8)
                img_erosion = cv2.dilate(thresh1, kernel, iterations=1)
                random_img = scipy.ndimage.gaussian_filter(img_erosion, 1)

        # creating the result image
        fig_spacing_x = random.randrange(-1 + mean_spacing_x, 1 + mean_spacing_x)
        fig_spacing_y = random.randrange(mean_spacing_y, 3 + mean_spacing_y)
        fig_height = random.randrange(-2 + mean_height, 2 + mean_height)
        random_img_resize= cv2.resize(random_img, (fig_height,fig_height), interpolation=cv2.INTER_AREA)
        fig_width = random_img_resize.shape[1]

        pic[fig_spacing_y: fig_spacing_y + fig_height, current_width + fig_spacing_x: current_width + fig_spacing_x + fig_width] = random_img_resize
        current_width += fig_width + fig_spacing_x
        plt.imshow(pic)
    plt.savefig("tmp.jpg")
    # print(":)")
    return pic

# #path = r'/home/inbarnoa/PycharmProjects/MathSolver/equationNumbers/A7_0.bmp'
# path = r'77.jpg'
# img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
# isDigitAppear("77*11=", "847", img)