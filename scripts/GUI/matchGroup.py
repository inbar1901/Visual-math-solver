"""
this function for a given figure, img of that figure and a run number
output a different image of the figure that it is in the same group as the original img in the given run number
used inside - isDigitAppear and isParamAppear
"""
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy
from scipy.ndimage import gaussian_filter
import cv2
import joblib

# finds the figure's group and returns a figure in the same group

def matchGroup(wanted_number, img, run_number):
    # variables to set
    model_path = r'/home/inbarnoa/PycharmProjects/MathSolver/clustering_model'
    folder_path = r'/home/inbarnoa/PycharmProjects/MathSolver/DataSet/DataSetNumbers/extracted_images/' + str(wanted_number)
    # constants
    IMG_HEIGHT = 11
    IMG_WIDTH = 11

    # importing to model to fit the new number to
    kmeans_filename = model_path + "/kmeans" + str(wanted_number) + "_" + str(run_number)
    kmeans = joblib.load(kmeans_filename)
    pca_filename = model_path + "/PCA" + str(wanted_number) + "_" + str(run_number)
    pca = joblib.load(pca_filename)

    # fitting the new number to model characteristics - needed always
    image_to_match = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH), interpolation=cv2.INTER_AREA)
    plt.imshow(image_to_match)
    plt.savefig(r"/home/inbarnoa/PycharmProjects/MathSolver/resized_nine.png")
    image_to_match = np.array(image_to_match)
    #image_to_match = np.array(img)
    image_to_match = image_to_match.astype('float32')
    image_to_match = image_to_match.reshape((1,-1))

    # matching the new number to the model
    reduced_data = pca.transform(image_to_match)
    result = kmeans.predict(reduced_data)
    print(result)

    # printing a figure from new number's group
    kmeans_data_path = model_path + '/imageKmeanData' + str(wanted_number) + '_run' + str(run_number) + '.txt'
    imageKmeansData = open(kmeans_data_path)
    imageKmeansData = imageKmeansData.readlines()
    matched_lines = [line for line in imageKmeansData if "Kmeans Label: " + str(result[0]) in line]
    random_image_in_group = random.choice(matched_lines)
    random_image_in_group = random_image_in_group.split()[2]
    random_image_in_group_path = folder_path + '/' + random_image_in_group

    # importing the new number
    random_image = cv2.imread(random_image_in_group_path, cv2.IMREAD_GRAYSCALE)

    # fitting the new number to model characteristics - needed only on original photos
    ret, thresh1 = cv2.threshold(random_image, 200, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3, 3), np.uint8)
    img_erosion = cv2.dilate(thresh1, kernel, iterations=1)
    gaus_eros = scipy.ndimage.gaussian_filter(img_erosion, 1)
    return gaus_eros,result[0]

# wanted_number = 9
# folder_path = r'/home/inbarnoa/PycharmProjects/MathSolver/DataSet/DataSetNumbers/extracted_images/' + str(wanted_number)
# #image_path = folder_path + r'/9_1127.jpg'
# image_path = r'A18_0_9.jpg'
#
# # create figure
# fig = plt.figure(figsize=(10, 7))
#
# # setting values to rows and column variables
# rows = 1
# columns = 2
#
# # reading images
# original_Image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
# random_img,group = matchGroup(wanted_number, original_Image)
# # Adds a subplot at the 1st position
# fig.add_subplot(rows, columns, 1)
# # showing image
# plt.imshow(random_img)
# plt.axis('off')
# plt.title("random image")
#
# # Adds a subplot at the 2nd position
# fig.add_subplot(rows, columns, 2)
#
# # showing image
# plt.imshow(original_Image)
# plt.axis('off')
# plt.title("Cluestered Image")
#

print(":)")