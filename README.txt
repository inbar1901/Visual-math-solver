Visual math solver scripts manual:
Goal: reading handwritten equations, solve them and write back the solution in similar handwrite

###### ---------- requirements ---------- ###### 
Python 3.6
Pytorch == 1.0
Libraries -
  pickle
  numpy
  cv2
  scipy
  os
  random
  tkinter
  PIL
  torch
  re
  sympy
  matplotlib
  joblib
  sklearn


###### ---------- Project's scripts ---------- ###### 

Train HMER:
1. Train - training the model
2. Attention_RNN.py - network's definition and functions used for training
3. gen_pkl.py - creating an ground-truth pkl, contains train/test images
4. data_iterator.py - loads data, used inside training
5. dictionart.txt - gives serial number to each figure that the network knows to recognize
6. Densnet_torchvision.py - used inside training

Test HMER:
1. Densnet_testway.py - test the testSet after training the model

Create Dataset (the first two are the final scripts, it's recommended to use those two):
1. DataCreatorNumOnlySameGroup.py - create equations only with numbers. Same figures are chosen from the same group.
2. DataCreatorParameterSameGroup.py- create equations with one parameter. Same figures are chosen from the same group.
3. DataCreator.py - creates random sequences with thin, sharp letters
 (contains more mathematic signs and brackets then in equations creating scripts, without equation rules)
4. DataCreatorN.py - creates random sequences with thin, sharp letters
 (contains more mathematic signs and brackets then in equations creating scripts, verifies that every open bracket has muching closing bracket)
5. DataCreatorN2.py - creates random sequences with wide letters
 (final project signs, verifies the equation doesn't start with a sign)
6. DataCreatorEquationKnown.py - creates specific equation (line 39) with wide figures. Same figures are taken from the same group
7.  DataCreatorNumOnly.py - creates numeric equations with wide figures.
8. DataCreatorParameter.py - creates parametric equations with wide figures.

Clustering figures:
1. clustering.py - perform the PCA and Kmeans division into groups
2. createExamples.py - creates examples matrix for each group for the listed figures
3. createDataset.py - creates 2 arrays, one of images class(type) names and one of the images

Run project:
1. OurTK.py - GUI
2. findFiguresInEq.py - use to find BB of each figure in the equation
3. isDigitAppear.py - use to build numeric equation handwritten solution
4. isParamAppear.py - use to build parametric equation handwritten solution
5. matchGroup.py - match a group in KMEANS clustering for the image of figure
6. for_test_V20.py - used inside GUI to run the algorithm and recognize the image according to model
7. DataPrePRocessingGui.py - pre process a white on black thin equation to netwotk's requirements

###### ---------- Using project's abilities ---------- ###### 

### ---------- Download Data ---------- ###
1. Download figures DataSet from https://www.kaggle.com/xainano/handwrittenmathsymbols and decompress it into DataSet folder
2. Original HMER dataset download from https://github.com/whywhs/Pytorch-Handwritten-Mathematical-Expression-Recognition
3. Download pretrained Densenet weights from https://download.pytorch.org/models/densenet121-a639ec97.pth

### ---------- Create PCA-KMEANS clustering ---------- ###
In clustering.py file:
  - Update path of figures DataSet (path, line 20)
  - Update run number for PCA & KMEANS clustering (run_number, line 21)
  - Choose amount of KMEANS groups (groups_amount, line 22)
  - Choose amount of PCA components (n_components, line 38)
  - Update model folder - where to save the models of PCA & KMEANS (filename - lines 41 and 47, one for PCA and one for KMEANS)
  - Run clustering.py (it will run also createDataset.py)

In order to create tables of examples of each clustering group ***Not necessary for working network
In createExamples.py file:
  - Update path of figures DataSet (folder_path, line 20)
  - Update run number for PCA & KMEANS clustering (run_number, line 21)
  - Update the PCA & KMEANS models folder path (model_path, line 21)
  - Verify that KMEANS group amount is as in the model (groups_amount, line 30)
  - Update path to save the example matrix in (plt.savefig path, line 54)
  - Run createExamples.py

### ---------- Create DataSet ---------- ###
To create dataset contains numeric and paramtric equations use:
1. DataCreatorNumOnlySameGroup.py
2. DataCreatorParameterSameGroup.py 
In the above scripts:
    - Update path of figures DataSet (path, line 18)
    - Update caption file path and name (caption, line 19)
    - Update run number of PCA & KMEANS clustering (run_number, line 28)
    - Update PCA & KMEANS model folder (model_path, line 29)
    - Choose amount of equations to create (num_equation, line 31)
    - Update equation saved folder (final.save path, line 79)

  ! Notice to create two dataset - train_set and test_set. Update differnt folder name for each set.

another options for creating equations: (if you choose some of the below, follow according the instructions above)
1. DataCreator.py 
2. DataCreatorN.py
3. DataCreatorN2.py
4. DataCreatorEquationKnown.py 
5. DataCreatorNumOnly.py 
6. DataCreatorParameter.py

### ---------- Prepare DataSets for Network ---------- ###
Compress dataset's images into pkl file. In gen_pkl.py file:
  ! Do the following twice - once for train_set and once for test_set
  - Update image dataset path - same path as in "create dataset" section (image_path, line 15). 
  - Update output file name (outFile, line 16)
  - Update caption file path (scpFile, line 25)
  - Run gen_pkl.py

### ---------- Train the network ---------- ###
In Train.py file:
  - Update train trainset (pkl file) and caption path (txt file) (datasets, line 50)
  - Update test testset (pkl file) and caption path (txt file) (valid_datasets, line 51)
  - Update dictionary path (dictionaries, line 52)
  - Update densenet121 file path (pthfile, line 280)
  - Update train run number in trainLoss, WER, succ graph names and in model save name (lines 537-538)
  - Run the training 

### ---------- Test the trained model ---------- ###
In Densenet_testway.py file:
  - Update test testset (pkl file) and caption path (valid_datasets, line 50)
  - Update dictionary path (dictionaries, line 51)
  - Update trained models path (encoder.load_state_dict, line 155 + attn_decoder1.load_state_dict, line 156)
  - Run Densenet_testway.py

### ---------- Activate Project ---------- ###
Occures through the GUI OurTK.py. In order to use it correctily:
In isDigitAppear.py file:
  - Update run number of PCA & KMEANS clustering (run_number, line 21)
  - Update PCA & KMEANS model folder (model_path, line 22)
  - Update path of figures DataSet (random_image_in_group_path, line 60 + random_img_path, line 36)

In isParamAppear.py file:
    - Update run number of PCA & KMEANS clustering (run_number, line 21)
    - Update PCA & KMEANS model folder (model_path, line 22)
    - Update path of figures DataSet (random_image_in_group_path, line 97 + random_img_path, lines 51-73  + eq_img_path, line 30)

In matchGroup.py file:
    - Update PCA & KMEANS model folder (model_path, line 19)
    - Update path of figures DataSet (folder_path, line 20)
    - Update equation saved folder (final.save path, line 34)

In HMER_v2.0/for_test_V20.py file:
  - Update dictionary name and path (dictionaries, line 22)
  - Update trained models path (encoder.load_state_dict, line 56 + attn_decoder1.load_state_dict, line 57)

In HMER_v2.0/OurTK.py file:
  - Update folder path to select image from (initialdir, line )
  - Run OurTK.py (runs inside - for_test_V20, isDigitAppear, isParamAppear, find_figures_in_eq, matchGroup)

Inside the GUI:
  1. Click "Load Equation" and choose the image equation you want to solve
  2. The image appear under "Your image:"
  3. Click "Start Detection"
  4. After detection is finished you will see the results:
    Recognized equation
    Solution
    Equation type - parametric/numeric
    Result image
