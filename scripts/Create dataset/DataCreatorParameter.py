"""
This module create dataset from separate digits and signs
it create equation contain numbers, one parameter and math operation and one '=' in the middle
it create the equation wide (using erosion and gaussian filter)
output also a caption to the equation in order to create round truth
it create a legal equation with only one parameter that can be solved (even with higher power)
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
caption = open('/home/inbarnoa/PycharmProjects/MathSolver/equation_parameter_caption_1.txt', 'a')

folder_amaunt = 27
equ_length = 15

numbers_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0','1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
equal_signs_list = ['=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=']
signs_list = ['+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot']
letters_list = ['A', 'b','C','d','e','f','G','H','i','j','k','l','M','N','o','p','q','R','S','T','u','v','w','X','y','z']

fig_size = 45


# increase numbers probability
# decrease close probability
for im in range(100):
    param_exist = 0
    eqSign_exist = 0
    amountRand = random.randrange(3, equ_length)
    pic_width = random.randrange((amountRand * 45) + 10, (amountRand * 50) + 10)
    pic_height = random.randrange(60, 70)
    pic = np.array(Image.new(mode='1', size=(pic_width, pic_height)))
    image_caption = ''

    # creating the new picture
    for figure in range(amountRand):
        if figure == 0:
            figure_type = random.choice(numbers_list+letters_list+numbers_list)
            if figure_type in letters_list:
                param_exist=figure_type
        elif figure == amountRand-1:
            if param_exist == 0:
                figure_type = random.choice(letters_list)
                param_exist = figure_type
            else:
                figure_type = random.choice(numbers_list +  [param_exist,param_exist,param_exist,param_exist,param_exist] )
        elif figure == amountRand-2 and eqSign_exist == 0:
            figure_type='='
            eqSign_exist =1
        elif amountRand >3 and figure == amountRand-3 and eqSign_exist == 0:
            figure_type = random.choice(numbers_list)
        else:
            if param_exist == 0:
                if (figure_type in equal_signs_list) or (figure_type in signs_list):
                    figure_type = random.choice(numbers_list + letters_list + numbers_list)
                    if figure_type in letters_list:
                        param_exist = figure_type
                else:
                    if eqSign_exist:
                        figure_type = random.choice(numbers_list + letters_list + numbers_list+signs_list)
                        if figure_type in letters_list:
                            param_exist = figure_type
                    else:
                        figure_type = random.choice(numbers_list + letters_list + numbers_list + signs_list+equal_signs_list)
                        if figure_type in letters_list:
                            param_exist = figure_type
                        if figure_type == '=':
                            eqSign_exist=1
            else:
                if (figure_type in equal_signs_list) or (figure_type in signs_list):
                    figure_type = random.choice(numbers_list + [param_exist,param_exist,param_exist,param_exist,param_exist] )
                else:
                    if eqSign_exist:
                        figure_type = random.choice(numbers_list +  [param_exist,param_exist,param_exist,param_exist,param_exist] + signs_list)
                    else:
                        figure_type = random.choice(numbers_list + [param_exist,param_exist,param_exist,param_exist,param_exist] + signs_list + equal_signs_list)
                        if figure_type == '=':
                            eqSign_exist = 1


        figure_file_name = random.choice(os.listdir(path + '/' + figure_type))
        fig_pic_w = imread(path + '/' + figure_type + '/' + figure_file_name)

        fig_pic = fig_pic_w < 200

        fig_width = random.randrange(-3, 3)
        fig_height = random.randrange(-5, 5)
        pic[5 + fig_height:fig_size + 5 + fig_height,(figure * fig_size) + 5 + fig_width:((figure + 1) * fig_size) + 5 + fig_width] = fig_pic



        final = (Image.fromarray(pic))
        image_caption = image_caption + ' ' + figure_type

    final.save('./equationParameter/B' + str(im) + '_0' + '.bmp')
    img_cvt = cv2.imread('./equationParameter/B' + str(im) + '_0' + '.bmp', cv2.IMREAD_GRAYSCALE)
    kernel = np.ones((3, 3), np.uint8)
    img_erosion = cv2.dilate(img_cvt, kernel, iterations=1)
    gaus_eros = scipy.ndimage.gaussian_filter(img_erosion, 1)
    cv2.imwrite('./equationParameter/D' + str(im) + '_0' + '.bmp', gaus_eros)
    caption.write('D' + str(im) + '	' + image_caption + '\n')
    os.remove('./equationParameter/B' + str(im) + '_0' + '.bmp')
    close_flag = 1

print('success =)')
