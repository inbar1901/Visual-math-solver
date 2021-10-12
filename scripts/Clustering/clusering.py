"""
this module perform the PCA and Kmeans division into groups
for each digit or sign it takes all the data (all images of the digit)
resize (11X11) using the createDataset.py file, perform PCA and then divide into roups with K-means
the output is log file with the labels for each image. log file per digit.
notice to update the run number and the digits/letters you want to perform the process to.
for k-mean divide into 2 groups there is comment part to show how the data is divided
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from createDataset import create_dataset
import joblib
from sklearn.mixture import GaussianMixture


# variables to set
path = '/home/inbarnoa/PycharmProjects/MathSolver/DataSet/DataSetNumbers/extracted_images'
run_number = 18
groups_amount = 30

# constants
numbers_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
letters_list = ['A', 'b','C','d','e','f','G','H','i','j','k','l','M','N','o','p','q','R','S','T','u','v','w','X','y','z']
signs_list = ['=','-','+','\cdot']
h = 0.5  # point in the mesh [x_min, x_max]x[y_min, y_max].  Step size of kmeans mesh. Decrease to increase the quality of the VQ.

# iterations over all figures in DataSetNumbers
for figure in os.listdir(path):
    if figure in numbers_list+letters_list+signs_list: # if we want to cluster the figure
        outputData = open('/home/inbarnoa/PycharmProjects/MathSolver/clustering_model/imageKmeanData' + str(figure) + '_run' + str(run_number) + '.txt', 'a')
        digit_path = path + r'/' + str(figure)
        data, labels = create_dataset(digit_path, figure)

        # creating clustering model
        pca = PCA(n_components=20)
        pca.fit(data)
        reduced_data = pca.transform(data)
        filename = "/home/inbarnoa/PycharmProjects/MathSolver/clustering_model/PCA" + str(figure) + "_" + str(run_number)
        joblib.dump(pca, filename)

        # model = GaussianMixture(n_components=10)
        kmeans = KMeans(init="k-means++", n_clusters=groups_amount, n_init=4)
        kmeans.fit(reduced_data)
        filename = "/home/inbarnoa/PycharmProjects/MathSolver/clustering_model/kmeans" + str(figure) + "_" + str(run_number)
        joblib.dump(kmeans, filename)

        # writing to LogFile the model details
        LISTDIR = os.listdir(digit_path)
        for i in range(len(reduced_data)):
            outputData.write('image name: ' + LISTDIR[i] + '\t Kmeans Label: '+str(kmeans.labels_[i])+'\n')
        #            outputData.write('image name: ' + LISTDIR[i] + '\t PCA location: '+ str(reduced_data[i])+'\t Kmeans Label: '+str(kmeans.labels_[i])+'\n')
        # # Plot the decision boundary. For that, we will assign a color to each
        # x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
        # y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
        # xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        #
        # # Obtain labels for each point in mesh. Use last trained model.
        # Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
        #
        # # Put the result into a color plot
        # Z = Z.reshape(xx.shape)
        # plt.figure(1)
        # plt.clf()
        # im = plt.imshow(Z, interpolation="nearest",
        #            extent=(xx.min(), xx.max(), yy.min(), yy.max()),
        #            cmap=plt.cm.Paired, aspect="auto", origin="lower")
        # plt.colorbar()
        # plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
        # # Plot the centroids as a white X
        # centroids = kmeans.cluster_centers_
        # plt.scatter(centroids[:, 0], centroids[:, 1], marker="x", s=169, linewidths=3,
        #             color="w", zorder=10)
        # plt.title("K-means clustering on the digits dataset (PCA-reduced data)\n"
        #           "Centroids are marked with white cross - run " + str(run_number))
        # plt.xlim(x_min, x_max)
        # plt.ylim(y_min, y_max)
        # plt.xticks(())
        # plt.yticks(())
        #
        # #plt.show()
        # plt.savefig("/home/inbarnoa/PycharmProjects/MathSolver/clustering_model/map" + str(figure) + "_" + str(run_number) + ".jpeg")


