"""
This module create the thin Dataset,
without any restriction for the equation
just random number of digits in each equation from 1 to equ_length
it also write to the caption file the ground truth of the equation to perform the training
"""

import random
import os
import pickle as pkl
import numpy as np
from scipy.misc.pilutil import imread, imresize, imsave, imshow
from PIL import Image, ImageOps

path = '/home/inbarnoa/PycharmProjects/MathSolver/DataSet/DataSetNumbers/extracted_images'
caption = open('/home/inbarnoa/PycharmProjects/MathSolver/trainNewData/trainCaption.txt', 'a')

folder_amaunt = 27
equ_length = 15
get_fig_map = {
    0:'0',
    1:'1',
    2:'2',
    3:'3',
    4:'4',
    5:'5',
    6:'6',
    7:'7',
    8:'8',
    9:'9',
    10:'=',
    11:'(',
    12:')',
    13:'[',
    14:']',
    15:'{',
    16:'}',
    17:'+',
    18:'geq',
    19:'gt',
    20:'div',
    21:'ldots',
    22:'leq',
    23:'lt',
    24:'neq',
    25:'times',
    26:'-'
}
fig_size = 45
close_flag = 0 # means that if a close is taken we will take the other close as well
# increase numbers probability
# decrease close probability
for im in range(2000):
    amountRand = random.randrange(1,equ_length)
    pic_width = random.randrange((amountRand * 45)+10, (amountRand * 50)+10)
    pic_height = random.randrange(55, 65)
    pic = np.array(Image.new(mode='1', size=(pic_width,pic_height)))
    image_caption = ''
    # creating the new picture
    for figure in range(amountRand):
        figure_type = get_fig_map[random.randrange(0,folder_amaunt)]
        figure_file_name = random.choice(os.listdir(path+'/'+figure_type))
        fig_pic_w = imread(path+'/'+figure_type+'/'+figure_file_name)
        fig_pic= fig_pic_w<200
        fig_width = random.randrange(-5, 5)
        fig_height = random.randrange(-5, 5)
        pic[ 5+fig_height:fig_size+5+fig_height, (figure*fig_size)+5+fig_width:((figure+1)*fig_size)+5+fig_width] = fig_pic
        final =(Image.fromarray(pic))
        image_caption = image_caption + ' ' + figure_type
    final.save('./trainNewData/A'+str(im)+'.bmp')
    caption.write('A'+str(im)+'	'+image_caption+'\n')
    close_flag = 1


print('success =)')

