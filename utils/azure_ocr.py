import requests
import json
import time
from utils.ocr import OCR
from config import *
from io import BytesIO
from typing import Tuple, Dict, List

class AzureOCR(OCR):
	def initialize(self):
		self.SUBSCRIPTION_KEY = SUBSCRIPTION_KEY
		self.SHOW_RESPONSE = SHOW_RESPONSE

	def print_response(self, area:Tuple[float, float, float, float], response:Dict) -> str:
		''' Prints the response from Cognitive Services.
		Input:
			area - String describing the bounding box of the data
			response - The response for the image from Cognitive Services
		'''
		txt = ""
		for line in response['recognitionResult']['lines']:
			txt += line['text'] + '\n'
		if self.SHOW_RESPONSE:
			if response["status"] == "Succeeded":
				#print(response['recognitionResult']['lines'])
				print("")
				print("==RESULT==" + str(area))
				for line in response['recognitionResult']['lines']:
					print(line['text'])
				print("==========================")
				print("")
			else:
				print("Processing failed:")
				print(response)
		return txt

	def ocr_one_image(self, area:Tuple[float, float, float, float], image_data:object, threadList=-1, threadNum=None) -> None:
		''' Performs OCR on a single image
		Input:
			area - String that describe the bounding box of the data
			image_data - String of the data
		'''
		image_data = self.pic_to_string(image_data)
		try:
			request_url = "https://westus.api.cognitive.microsoft.com/vision/v2.0/recognizeText?mode=Printed"
			headers  = {'Ocp-Apim-Subscription-Key': self.SUBSCRIPTION_KEY, 'Content-Type': "application/octet-stream"}
			data     = image_data

			# Send the POST request and parse the response
			response = requests.request('post', request_url, headers=headers, data=data)

			if response.status_code == 202:
				get_response = {}
				get_response["status"] = "Running"
				#print(get_response)
				# Continue sending requests until it finished processing
				while get_response["status"] == "Running" or get_response["status"] == "NotStarted":
					#print(get_response)
					time.sleep(.2)
					r2 = requests.get(response.headers['Operation-Location'], headers={'Ocp-Apim-Subscription-Key': self.SUBSCRIPTION_KEY})
					get_response = r2.json()
					#print(get_response)
				res = self.print_response(area, get_response)
				if threadList != -1:
					threadList[threadNum] = (res)
				return res
			print(response)
		except Exception as e:
			print("OCR failed")
			print(e)
			return None


	def pic_to_string(self, image) -> str:
		''' Uses PIL and StringIO to save the image to a string for further processing 
		Input: image - an image opened by PIL
		Output: A string containing all the data of the picture'''
		output_string = BytesIO()
		image.save(output_string, format="JPEG")
		string_contents = output_string.getvalue()
		output_string.close()
		return string_contents
