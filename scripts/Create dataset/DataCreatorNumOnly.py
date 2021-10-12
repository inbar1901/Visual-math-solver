"""
This module create dataset from separate digits and signs
it create equation contain only numbers and math operation and finished with '='
it create the equation wide (using erosion and gaussian filter)
output also a caption to the equation in order to create round truth
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

path = '/home/inbarnoa/PycharmProjects/MathSolver/DataSet/DataSetNumbers/extracted_images'
caption = open('/home/inbarnoa/PycharmProjects/MathSolver/equation_numbers_caption_1.txt', 'a')

folder_amaunt = 27
equ_length = 15

numbers_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0','1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
equal_signs_list = ['=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=']
signs_list = ['+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot']


fig_size = 45
close_flag = 0  # means that if a close is taken we will take the other close as well
# increase numbers probability
# decrease close probability
for im in range(10):
    amountRand = random.randrange(2, equ_length)
    pic_width = random.randrange((amountRand * 45) + 10, (amountRand * 50) + 10)
    pic_height = random.randrange(60, 70)
    pic = np.array(Image.new(mode='1', size=(pic_width, pic_height)))
    image_caption = ''

    # creating the new picture
    for figure in range(amountRand):
        if figure == 0 or figure == amountRand-2:
            figure_type = random.choice(numbers_list)
        elif figure == amountRand-1:
            figure_type = '='
        else:
            if figure_type in signs_list:
                figure_type = random.choice(numbers_list)
            else:
                figure_type = random.choice(numbers_list + numbers_list + signs_list )


        figure_file_name = random.choice(os.listdir(path + '/' + figure_type))
        fig_pic_w = imread(path + '/' + figure_type + '/' + figure_file_name)

        fig_pic = fig_pic_w < 200

        fig_width = random.randrange(-3, 3)
        fig_height = random.randrange(-5, 5)
        pic[5 + fig_height:fig_size + 5 + fig_height,(figure * fig_size) + 5 + fig_width:((figure + 1) * fig_size) + 5 + fig_width] = fig_pic



        final = (Image.fromarray(pic))
        image_caption = image_caption + ' ' + figure_type

    final.save('./equationNumbers/B' + str(im) + '_0' + '.bmp')
    img_cvt = cv2.imread('./equationNumbers/B' + str(im) + '_0' + '.bmp', cv2.IMREAD_GRAYSCALE)
    kernel = np.ones((3, 3), np.uint8)
    img_erosion = cv2.dilate(img_cvt, kernel, iterations=1)
    gaus_eros = scipy.ndimage.gaussian_filter(img_erosion, 1)
    cv2.imwrite('./equationNumbers/D' + str(im) + '_0' + '.bmp', gaus_eros)
    caption.write('D' + str(im) + '	' + image_caption + '\n')
    os.remove('./equationNumbers/B' + str(im) + '_0' + '.bmp')
    close_flag = 1

print('success =)')
