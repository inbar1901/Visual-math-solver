"""
This module create dataset from separate digits and signs
it create equation contain numbers, one parameter and math operation and one '=' in the middle
it create the equation wide (using erosion and gaussian filter)
output also a caption to the equation in order to create ground truth
it create the equation such that every figure is from the same clustering group - similar handwrite.
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
number_group= np.full(15,-1)
run_number = 18
model_path = r'/home/inbarnoa/PycharmProjects/MathSolver/clustering_model'
numberDict = {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"=":10,"+":11,"-":12,"\cdot":13,
              'A':14, 'b':14,'C':14,'d':14,'e':14,'f':14,'G':14,'H':14,'i':14,'j':14,'k':14,'l':14,'M':14,'N':14,'o':14
                 ,'p':14,'q':14,'R':14,'S':14,'T':14,'u':14,'v':14,'w':14,'X':14,'y':14,'z':14}
fig_size = 45
folder_name = 'equationParameter'

# increase numbers probability
# decrease close probability
for im in range(10):
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

        if number_group[numberDict[figure_type]] == -1:
            number_group[numberDict[figure_type]] = random.randrange(0, 9, 1)
        kmeans_data_path = model_path + '/imageKmeanData' + figure_type + '_run' + str(run_number) + '.txt'
        imageKmeansData = open(kmeans_data_path)
        imageKmeansData = imageKmeansData.readlines()
        matched_lines = [line for line in imageKmeansData if
                         "Kmeans Label: " + str(number_group[numberDict[figure_type]]) in line]
        random_image_in_group = random.choice(matched_lines)
        random_image_in_group = random_image_in_group.split()[2]
        figure_file_path = path + '/' + figure_type + '/' + random_image_in_group
        fig_pic_w = imread(figure_file_path)

        fig_pic = fig_pic_w < 200

        fig_width = random.randrange(0, 5)
        fig_height = random.randrange(-5, 5)
        pic[5 + fig_height:fig_size + 5 + fig_height,(figure * fig_size) + 5 + fig_width:((figure + 1) * fig_size) + 5 + fig_width] = fig_pic

        final = (Image.fromarray(pic))
        image_caption = image_caption + ' ' + figure_type

    final.save('./' + folder_name + '/B' + str(im) + '_0' + '.bmp')
    img_cvt = cv2.imread('./' + folder_name + '/B' + str(im) + '_0' + '.bmp', cv2.IMREAD_GRAYSCALE)
    kernel = np.ones((3, 3), np.uint8)
    img_erosion = cv2.dilate(img_cvt, kernel, iterations=1)
    gaus_eros = scipy.ndimage.gaussian_filter(img_erosion, 1)
    img_name = 'E' + str(im)
    cv2.imwrite('./' + folder_name + '/' + img_name + '_0' + '.bmp', gaus_eros)
    caption.write(img_name + '	' + image_caption + '\n')
    os.remove('./' + folder_name + '/B' + str(im) + '_0' + '.bmp')
    close_flag = 1

print('success =)')
