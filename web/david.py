# -*- coding: utf-8 -*- 
"""Takes the results of the train step and builds a production container 
@Author: David Crook - Microsoft Corporation - 2018 
@Author-Email: DaCrook@Microsoft.com 
Code is provided as is with no guarentees. 
""" 
import sys 
sys.path.append("../.") 
import json 
from Core.AbstractModel import IModel, resolve_model 
#from AutoEncoder-original import PointAutoEncoder 
from robotidentifier import RobotIdentifier

Algorithm = None 
i = 0
def init():
	Algorithm = RobotIdentifier()

def preprocess(data):
	image = data['image']
	filename = "image" + str(i) + ".jpg"
	fh = open(filename, "wb")
	i += 1
	fh.write(image)
	fh.close()
	return filename

def predict(data):
	return Algorithm.find_and_classify(filename)

def process_image(in_data):	 
	filename = preprocess(in_data) 
	data = predict(filename)
	return data


def run(string_body):
	""" 
	called on each web request. The body is the request body as a string. 
	""" 

	in_data = json.dumps(string_body) #converts to dictionary
	process_image(in_data)