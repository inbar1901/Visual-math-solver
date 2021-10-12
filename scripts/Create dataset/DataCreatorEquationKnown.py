"""
This module create a requested equation
the figures are selected from the same groups (from the clustering)
the equation is wide using erosion and gaussian filter 3x3
notice to update the run number and the requested equation
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
import matplotlib.pyplot as plt

path = '/home/inbarnoa/PycharmProjects/MathSolver/DataSet/DataSetNumbers/extracted_images'
caption = open('/home/inbarnoa/PycharmProjects/MathSolver/equation_numbers_caption_1.txt', 'a')

folder_amaunt = 27
equ_length = 15

numbers_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0','1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
equal_signs_list = ['=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=','=']
signs_list = ['+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot','+', '-', '\cdot']
number_group= np.full(15,-1)
run_number = 18
model_path = r'/home/inbarnoa/PycharmProjects/MathSolver/clustering_model'
numberDict = {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"=":10,"+":11,"-":12,"\cdot":13,"*":13,
              'A':14, 'b':14,'C':14,'d':14,'e':14,'f':14,'G':14,'H':14,'i':14,'j':14,'k':14,'l':14,'M':14,'N':14,'o':14
                 ,'p':14,'q':14,'R':14,'S':14,'T':14,'u':14,'v':14,'w':14,'X':14,'y':14,'z':14}


fig_size = 45
close_flag = 0  # means that if a close is taken we will take the other close as well
# increase numbers probability
# decrease close probability
Equation = "50+11*7="

amountRand = len(Equation)
pic_width = random.randrange((amountRand * 45) + 10, (amountRand * 50) + 10)
pic_height = random.randrange(60, 70)
pic = np.array(Image.new(mode='1', size=(pic_width, pic_height)))
# creating the new picture
for idx,figure_type in enumerate(Equation):
    if number_group[numberDict[figure_type]] == -1:
        number_group[numberDict[figure_type]] = random.randrange(0, 9, 1)
    if figure_type == "*":
        figure_type = "\cdot"
    kmeans_data_path = model_path + '/imageKmeanData' + figure_type + '_run' + str(run_number) + '.txt'
    imageKmeansData = open(kmeans_data_path)
    imageKmeansData = imageKmeansData.readlines()
    matched_lines = [line for line in imageKmeansData if
                     "Kmeans Label: " + str(number_group[numberDict[figure_type]]) in line]
    random_image_in_group = random.choice(matched_lines)
    random_image_in_group = random_image_in_group.split()[2]
#   if figure_type=="A":
#        random_image_in_group = "A_7759.jpg"
    figure_file_path = r'/home/inbarnoa/PycharmProjects/MathSolver/DataSet/DataSetNumbers/extracted_images/' + figure_type + '/' + random_image_in_group
    fig_pic_w = imread(figure_file_path)
    plt.imshow(fig_pic_w)
    fig_pic = fig_pic_w < 200
    plt.imshow(fig_pic)
    fig_width = random.randrange(3, 7)
    fig_height = random.randrange(-5, 5)
    pic[5 + fig_height:fig_size + 5 + fig_height,(idx * fig_size) + 5 + fig_width:((idx + 1) * fig_size) + 5 + fig_width] = fig_pic



    final = (Image.fromarray(pic))


final.save('./equationNumbers/B' + Equation + '_0' + '.bmp')
img_cvt = cv2.imread('./equationNumbers/B' + Equation + '_0' + '.bmp', cv2.IMREAD_GRAYSCALE)
plt.imshow(img_cvt)
kernel = np.ones((3, 3), np.uint8)
img_erosion = cv2.dilate(img_cvt, kernel, iterations=1)
gaus_eros = scipy.ndimage.gaussian_filter(img_erosion, 1)
plt.imshow(gaus_eros)
cv2.imwrite('./equationNumbers/C' + Equation + '_0' + '.bmp', gaus_eros)
os.remove('./equationNumbers/B' + Equation + '_0' + '.bmp')
close_flag = 1

print('success =)')
