# Application of Transfer Learning Tuning to a Convolutional Neural Network for Image classification to the analysis of collisions in High Energy Physics



## table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Original Repositories](#contained-repositories)
* [Requirements](#requirements)
* [How to download project](#how-to-download-project)
* [How to get json files](#how-to-get-json-files)
* [How to Create Images](#how-to-create-images)
* [How to tune a Transfer Learning Model](#how-to-tune-a-transfer-learning-model)

## General Info
This project is based of this paper: https://arxiv.org/pdf/1708.07034.pdf

The program of LHC and CMS records the collision of high energy physics and shares the data in the worldwide LHC Computing Grid, which gives a platform for physicists in 42 countries.With CMS open data, this research applied convolutional neural network to classify tt + jets, W + jets and Drell-Yan processes. We compare the performance of five well-known CNN models and test transfer learning in particle classification.

Project process:

JSON files -> Image Dataset -> Augmented Dataset (optional) -> Transfer Learning Model -> classification results

## Technologies

* Google colab
* Jupyter notebooks 

## Orignal Repositories

* For Image Creation : https://github.com/CeliaFernandez/Image-Creation
* For json file Creation : https://github.com/laramaktub/json-collisions
* For Augmentation : https://github.com/mdbloice/Augmentor

## Requirements

All required module can be found in the requirements.txt file


## How to get json files
[json-collisons README.md](https://github.com/jzyee/cms_image_classification/blob/master/json-cms-master/README.md)

## How to Create Images

1. After creating the [json files](https://github.com/jzyee/cms_image_classification/blob/master/json-cms-master/README.md)
transfer the json files 
- from folder: json-cms/AnalysisFW/python/outputjsons 
- to folder: json_files
2. Run [create_images.ipynb](https://github.com/jzyee/cms_image_classification/blob/master/create_images.ipynb) 
</br>
This will create the images in the CreatedImages folder

## How to Create Augmented Images(optional)

- not advised if user is planning to use the free gpu from provided by google colab. User will require a stronger GPU for training to have decent training times

1. Run [create_augments.ipynb](https://github.com/jzyee/cms_image_classification/blob/master/create_augments.ipynb)

This will create the images in the CreatedImages/output folder



## How to Tune a Transfer Learning Model

In this part, we can use Google Colaboratory to run the notebook as it provides GPU accelerators which help accelerate the training process. You will need a google drive account to upload your dataset into.
</br>
1. Upload the CreatedImages folder to your google drive
2. Rename the folders DYjets Images,TTjets Images,Wjets Images to 0,1,2 respectively.
2.	Download a model that you would like to use or all the .ipynb files  in this folder, and their filenames represent the different models and activation function (e.g. “vgg19_quark_classification_RMSprop.ipynb” means using VGG19 model with RMSprop as its activation function)
</br>
An example of how to download an .ipynb file:

    wget https://github.com/jzyee/cms_image_classification/blob/master/Training_Model/incepV3_quark_classification.ipynb


2.	Open the link: https://colab.research.google.com, create a new python3 notebook, and upload the .ipynb files via “File->Upload notebook” in the menu at the top left of the page. Then you can see the codes are successfully loaded in google colaboratory.
3.	To use GPU accelerator, you can change the setting via “Runtime->Change runtime type->Hardware accelerator->GPU->SAVE”. If loaded successfully, in the third cell it would print out ‘Found GPU at: /device:GPU:0’.
4.	To rerun the codes, images are needed. According to our codes, images should be uploaded to your google drive.In the fifth cell, it  will grant you access to your google drive by mounting the drive. You will need to change the image paths accordingly to where you have stored them on your drive
5.	If you run all the cells in the notebook, the trained models will be saved along with fitting history. This is so that you can load the model at a later time to carry the prediction again without the training.
6. Congratulations you have carried out transfer learning model tuning!

