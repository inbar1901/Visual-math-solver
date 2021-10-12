"""
this module recieve an string of equation and an image of the equation
it perform CC to separate the connected componnets,
calculate the statitic of the height and width of figures in the equation
and output an array that for each letter in the equation give the x boundingBox
"""

import cv2
import matplotlib.pyplot as plt
# find bounding box for each figure in equation
import numpy as np


def find_figures_in_eq(equation, img):
    ret,binary_img = cv2.threshold(img, 100, 255, 0)
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(binary_img, connectivity=8)
    plt.imshow(output)
    sortStat = sorted(stats, key=lambda x: x[0])
    idx_to_remove =[0]
    for idx in range(2,len(sortStat)):
        if sortStat[idx-1][2]>sortStat[idx][2]:
            end_short = sortStat[idx][2] + sortStat[idx][0]
            start_short = sortStat[idx][0]
            end_long = sortStat[idx-1][2] + sortStat[idx-1][0]
            start_long = sortStat[idx-1][0]
        else:
            end_short = sortStat[idx-1][2] + sortStat[idx-1][0]
            start_short = sortStat[idx-1][0]
            end_long = sortStat[idx][2] + sortStat[idx][0]
            start_long = sortStat[idx][0]
        list_short = range(start_short,end_short)
        list_long = range(start_long,end_long)
        intersection =set(list_short).intersection(list_long)
        if len(intersection) > 0.7 * (end_short-start_short):
            sortStat[idx][0]= min(sortStat[idx-1][0],sortStat[idx][0])
            sortStat[idx][2] = max(sortStat[idx-1][0]+sortStat[idx - 1][2],sortStat[idx][0]+sortStat[idx][2]) - sortStat[idx-1][0]
            sortStat[idx][1] = min(sortStat[idx - 1][1], sortStat[idx][1])
            sortStat[idx][3] = max(sortStat[idx - 1][1] + sortStat[idx - 1][3],
                                       sortStat[idx][1] + sortStat[idx][3]) - sortStat[idx][1]
            sortStat[idx][4] = -1
            idx_to_remove.append(idx-1)
    idx_to_remove.reverse()
    for id in idx_to_remove:
        del sortStat[id]
    #[ (del sortStat[idx]) for idx in idx_to_remove.reverse()]
#    [ np.delete(sortStat,l) for l in sortStat if l == [0,0,0,0,0]]
    # finding the digit's locations in x axis
    x_bb = []
    mean_spacing_x = 0
    mean_spacing_y = 0
    mean_height = 0
    counter = 0
    signs_list = ['+', '-', '\cdot','*','=']

    for idx,digit in enumerate(equation):
        # calculating digit's statistics
        if idx != len(equation)-1:
            mean_spacing_x += sortStat[idx+1][0] - (sortStat[idx][0]+sortStat[idx][2])
        if digit not in signs_list:
            counter += 1
            mean_spacing_y += sortStat[idx][1]
            mean_height += sortStat[idx][3]
        x_bb.append([equation[idx], [sortStat[idx][0], sortStat[idx][2]+sortStat[idx][0]]])

    mean_spacing_x = mean_spacing_x / len(equation)
    mean_spacing_y = mean_spacing_y / counter
    mean_height = mean_height / counter

    return x_bb, int(mean_spacing_x), int(mean_spacing_y), int(mean_height)

