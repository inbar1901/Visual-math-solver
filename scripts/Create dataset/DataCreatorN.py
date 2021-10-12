"""
This module create dataset from separate digits and signs
it contains {[(
it is not our chosen data creator - not used to create the training/ tested data
"""
import random
import os
import pickle as pkl
import numpy as np
from scipy.misc.pilutil import imread, imresize, imsave, imshow
from PIL import Image, ImageOps

path = '/home/inbarnoa/PycharmProjects/MathSolver/DataSet/DataSetNumbers/extracted_images'
caption = open('/home/inbarnoa/PycharmProjects/MathSolver/train_caption_1.txt', 'a')

folder_amaunt = 27
equ_length = 15

numbers_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
equal_signs_list = ['=', r'\neq', '\leq', '\geq', '>', '\leq', '<']
signs_list = ['+', '-', '\div', '\ldots', '\cdot']
open_bra_list = ['\{', '(', '[']
close_bra_list = ['\}', ')', ']']
letters_list = ['A', 'b','C','d','e','f','G','H','i','j','k','l','M','N','o','p','q','R','S','T','u','v','w','X','y','z']

fig_size = 45
close_flag = 0  # means that if a close is taken we will take the other close as well
# increase numbers probability
# decrease close probability
for im in range(1):
    amountRand = random.randrange(1, equ_length)
    pic_width = random.randrange((amountRand * 45) + 10, (amountRand * 50) + 10)
    pic_height = random.randrange(55, 65)
    pic = np.array(Image.new(mode='1', size=(pic_width, pic_height)))
    image_caption = ''
    curl_bracket = False
    square_bracket = False
    round_bracket = False
    # creating the new picture
    for figure in range(amountRand):
        if figure == 0:
            figure_type = random.choice(numbers_list + open_bra_list + numbers_list + letters_list + numbers_list)
        elif not curl_bracket and not square_bracket and not round_bracket:
            figure_type = random.choice(numbers_list + open_bra_list + numbers_list + signs_list + numbers_list + equal_signs_list + letters_list + numbers_list)
        else:
            if curl_bracket:
                if figure == amountRand-1:
                    figure_type = '\}'
                    curl_bracket = False
                else:
                    figure_type = random.choice(numbers_list + ['\}'] + numbers_list + signs_list + numbers_list + letters_list + numbers_list)
                    if figure_type == '\}':
                        curl_bracket = False
            elif square_bracket:
                if figure == amountRand-1:
                    figure_type = ']'
                    square_bracket = False
                else:
                    figure_type = random.choice(numbers_list + [']'] + numbers_list + signs_list + numbers_list + letters_list + numbers_list)
                    if figure_type == ']':
                        square_bracket = False
            else:
                if figure == amountRand-1:
                    figure_type = ')'
                    round_bracket = False
                else:
                    figure_type = random.choice(numbers_list + [')'] + numbers_list + signs_list + numbers_list + letters_list + numbers_list)
                    if figure_type == ')':
                        round_bracket = False

        if figure_type == '\{':
            curl_bracket = True
        if figure_type == '[':
            square_bracket = True
        if figure_type == '(':
            round_bracket = True


        #figure_type = get_fig_map[random.randrange(0, folder_amaunt)]
        figure_file_name = random.choice(os.listdir(path + '/' + figure_type))
        fig_pic_w = imread(path + '/' + figure_type + '/' + figure_file_name)
        fig_pic = fig_pic_w < 200
        fig_width = random.randrange(-5, 5)
        fig_height = random.randrange(-5, 5)
        pic[5 + fig_height:fig_size + 5 + fig_height,(figure * fig_size) + 5 + fig_width:((figure + 1) * fig_size) + 5 + fig_width] = fig_pic
        final = (Image.fromarray(pic))
        image_caption = image_caption + ' ' + figure_type
    final.save('./image_train_1/Z' + str(im) +  '_0' + '.bmp')
    caption.write('Z' + str(im) + '	' + image_caption + '\n')
    close_flag = 1

print('success =)')
