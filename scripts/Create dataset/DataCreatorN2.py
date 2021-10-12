"""
This module create dataset from separate digits and signs
it can contain multiple parameters and doesn't have a rule so the equation will be leagel
it is not our chosen data creator - not used to create the tested data
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
caption = open('/home/inbarnoa/PycharmProjects/MathSolver/val_caption_4.txt', 'a')

folder_amaunt = 27
equ_length = 15

numbers_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0','1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
equal_signs_list = ['=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=']
signs_list = ['+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot']
letters_list = ['A', 'b','C','d','e','f','G','H','i','j','k','l','M','N','o','p','q','R','S','T','u','v','w','X','y','z']

fig_size = 45
close_flag = 0  # means that if a close is taken we will take the other close as well
# increase numbers probability
# decrease close probability
for im in range(500):
    amountRand = random.randrange(1, equ_length)
    pic_width = random.randrange((amountRand * 45) + 10, (amountRand * 50) + 10)
    pic_height = random.randrange(55, 65)
    pic = np.array(Image.new(mode='1', size=(pic_width, pic_height)))
    image_caption = ''

    # creating the new picture
    for figure in range(amountRand):
        if figure == 0:
            figure_type = random.choice(numbers_list + numbers_list + letters_list + numbers_list)
        else:
            figure_type = random.choice(numbers_list + numbers_list + signs_list + numbers_list + equal_signs_list + letters_list + numbers_list)


        #figure_type = get_fig_map[random.randrange(0, folder_amaunt)]
        figure_file_name = random.choice(os.listdir(path + '/' + figure_type))
        fig_pic_w = imread(path + '/' + figure_type + '/' + figure_file_name)

        fig_pic = fig_pic_w < 200
        #fig_pic_w = fig_pic_w.astype('uint8')

        #img_cvt = cv2.cvtColor(np.array(fig_pic_w), cv2.COLOR_RGB2GRAY)
        #img_cvt = cv2.imread((path + '/' + figure_type + '/' + figure_file_name), cv2.IMREAD_GRAYSCALE)
        # a = np.array(fig_pic_w)
        # img_cvt = cv2.imread(a, 0)
        #kernel = np.ones((3, 3), np.uint8)
        #img_erosion = cv2.erode(img_cvt, kernel, iterations=1)
        #gaus_eros = scipy.ndimage.gaussian_filter(img_erosion, 0.5)
        #fig_pic = Image.fromarray(255 - fig_pic_w)

        fig_width = random.randrange(-5, 5)
        fig_height = random.randrange(-5, 5)
        pic[5 + fig_height:fig_size + 5 + fig_height,(figure * fig_size) + 5 + fig_width:((figure + 1) * fig_size) + 5 + fig_width] = fig_pic



        final = (Image.fromarray(pic))
        image_caption = image_caption + ' ' + figure_type

    final.save('./Image-val4-wide/B' + str(im) + '_0' + '.bmp')
    img_cvt = cv2.imread('./Image-val4-wide/B' + str(im) + '_0' + '.bmp', cv2.IMREAD_GRAYSCALE)
    kernel = np.ones((3, 3), np.uint8)
    img_erosion = cv2.dilate(img_cvt, kernel, iterations=1)
    gaus_eros = scipy.ndimage.gaussian_filter(img_erosion, 1)
    cv2.imwrite('./Image-val4-wide/A' + str(im) +  '_0' + '.bmp', gaus_eros)
    #gaus_eros.save('./Image-test4-wide/A' + str(im) +  '_0' + '.bmp')
    caption.write('A' + str(im) + '	' + image_caption + '\n')
    close_flag = 1

print('success =)')
