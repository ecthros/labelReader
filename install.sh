#!/bin/bash

#Tested on Ubuntu 16.04.


if [ "`which sudo`" = "" ]; then
	#if we don't have sudo, grab it
	if [ "$(id -u)" != "0" ]; then
		echo "This install script needs to be run as root."
		exit -1
	fi
	echo -e "Installing Python"
	apt install -y python
	echo -e "\n\nInstalling Python Dependencies\n\n"
	apt install -y python-pip python-tk git unzip libsm6 libxext6 tesseract-ocr python-opencv libsm6 libxext6 gcc unzip wget
else
	echo -e "Installing Python"
	sudo apt install -y python
	echo -e "\n\nInstalling Python Dependencies\n\n"
	sudo apt install -y python-pip python-tk git unzip libsm6 libxext6 tesseract-ocr python-opencv libsm6 libxext6 gcc unzip
fi

pip install pillow requests opencv-python keras tensorflow matplotlib pexpect pyocr Cython fuzzywuzzy[speedup] pydocumentdb numpy

echo -e "\n\nInstalling RotNet\n\n"
git clone https://github.com/ecthros/RotNet
cd RotNet
mkdir rotnet_models
wget https://www.dropbox.com/s/ch5917qg0j9leyj/rotnet_models.zip?dl=0
unzip rotnet_models.zip?dl=0
mv rotnet_* rotnet_models
cd ..

echo -e "\n\nDownloading Weights\n\n"
wget https://www.dropbox.com/s/zh4cjvuqimgm24s/yolo-obj_1600.weights?dl=0
mv yolo-obj_1600.weights?dl=0 yolo-obj_1600.weights

echo -e "\n\nDownloading darknet\n\n"
wget https://www.dropbox.com/s/9nxzvyyi53bi4p4/darknet?dl=0
mv darknet?dl=0 darknet
chmod 755 darknet

echo -e "\n\nDownloading Keras-Yolo3\n\n"
git clone https://github.com/qqwweee/keras-yolo3
cd keras-yolo3
python convert.py ../yolo-obj.cfg ../yolo-obj_1600.weights model_data/yolo.h5
echo "label" > model_data/coco_classes.txt

#needed darknet. Moved to pwd.
