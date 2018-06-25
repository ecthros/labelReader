RobotIdentifier is a Machine Learning-based solution to identifying a robot based on a picture that contains its nameplate.

# The Approach

The identifier's approach is straightforward:

1. Determine if a nameplate/asset is in the picture
2. Identify where that nameplate is
3. Crop out the relevant asset
4. Rotate the cropped picture so the text is readable
5. Read characters in the cropped picture
6. Find the relevant information in a database and present it to the user

# Demonstration
<p align="center">
<img src="https://user-images.githubusercontent.com/14065974/41622209-bcca5a84-73c3-11e8-84e7-00eae15f3011.gif" alt="Demonstration" height="450">
</p>

### Details

RobotIdentifier uses the [Yolov3 algorithm](https://pjreddie.com) for object detection. The user can choose between the following to interact with the algorithm:
* [Darknet](https://github.com/AlexeyAB/darknet)  (Fast, C Implementation) 
* [Keras-Yolov3](https://github.com/qqwweee/keras-yolo3) (Python Implementation) 

This repository contains a model that has been trained on labels for headphones, and will need to be tuned for custom images. 
For Optical Character Recognition, RobotIdentifier sends the processed images to Azure Cognitive Services. Users need to create an account with Cognitive Services Vision to use the model. Since it takes a few seconds to send and receive the request, RobotIdentifier supports an alternative library, [Tesseract](https://github.com/tesseract-ocr/tesseract) for faster OCR.

The repository contains another model, [RotNet](https://github.com/d4nst/RotNet) to detect how much to rotate the image. This should work for most products, but may need to be trained to suit your needs.

# Getting Started

RobotIdentifier can run on Docker. It is recommended to install Docker and use the base image, continuumio/miniconda3:

```
docker pull continuumio/miniconda3
docker run -i -t [Image ID] /bin/bash
apt update
```

Then, clone the repository:

```
git clone https://github.com/ecthros/robotidentifier
cd robotidentifier
```

To install necessary dependencies, run:

`./install.sh`

This script will install necessary components and set up RobotIdentifier to run. Once finished, run:

`python robotidentifier.py [-k/-d] [-c/-t]`

Make sure to specify if you want Keras or Darknet to classify, and Cognitive Services or Tesseract for OCR.

### Classifier Training Notes

* Training can take several hours to complete, even with an excellent GPU.
* There are many ways to train the classifier, but [Darknet](https://github.com/AlexeyAB/darknet) is easy to use.
	* Follow the steps to train [here](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects). 
	* You will need approximately a hundred classified images, in various environments and lightings, to train the model.
* Labeling with [VoTT](https://github.com/Microsoft/VoTT) is much easier than anything else I have found.
	* VoTT also creates the cfg, data, and folders for you.
* Make sure your images are of the same aspect ratio, since Darknet will change the size to a fixed image (or, just change this parameter in Darknet)
