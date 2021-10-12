"""
This module create an table of <NumberOfGruops>X<10Examples> for each digit and save it
the porpuse is to see how good is our clustering into groups using K-means and PCA
it uses the output of clustering.py module
notice to update to run number to match the clustering.py run number
and to update the requested figures to create the example matrix for (letters/digits)
"""
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy
from scipy.ndimage import gaussian_filter
import cv2
import joblib

# creates examples matrix for each group

run_number = 18
folder_path = r'/home/inbarnoa/PycharmProjects/MathSolver/DataSet/DataSetNumbers/extracted_images/'
model_path = r'/home/inbarnoa/PycharmProjects/MathSolver/clustering_model'
numbers_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
letters_list = ['A', 'b','C','d','e','f','G','H','i','j','k','l','M','N','o','p','q','R','S','T','u','v','w','X','y','z']
# create figure
fig = plt.figure(figsize=(15, 50))
groups_amount = 30
rows = groups_amount
columns = 5


for wanted_figure in numbers_list+letters_list:
    for group in range(groups_amount):
        kmeans_data_path = model_path + '/imageKmeanData' + wanted_figure + '_run' + str(run_number) + '.txt'
        imageKmeansData = open(kmeans_data_path)
        imageKmeansData = imageKmeansData.readlines()
        matched_lines = [line for line in imageKmeansData if "Kmeans Label: " + str(group) in line]
        for exp in range(5):
            random_image_in_group = random.choice(matched_lines)
            random_image_in_group = random_image_in_group.split()[2]
            random_image_in_group_path = folder_path + wanted_figure + '/' + random_image_in_group

            # reading images
            Image1 = cv2.imread(random_image_in_group_path)
            ax=fig.add_subplot(rows, columns, group*5 + exp +1)
            plt.imshow(Image1)
            ax.set_yticks([])
            ax.set_xticks([])
            # plt.axis('off')
            if exp == 0:
                ax.set_ylabel("group:" + str(group) + " ", fontsize=20)
            # plt.title("group: " + str(group) + "figure name: " + random_image_in_group)

    fig.suptitle("number: " +wanted_figure,fontsize=30,fontweight='bold')
    plt.savefig(r"/home/inbarnoa/PycharmProjects/MathSolver/clustering_model/example_matrix_" + wanted_figure + "_run_" + str(run_number))



print(":)")