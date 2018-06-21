import requests
import json
import time
from utils.ocr import OCR
from config import *

class AzureOCR(OCR):
	def initialize(self):
		self.SUBSCRIPTION_KEY = SUBSCRIPTION_KEY
		self.SHOW_RESPONSE = SHOW_RESPONSE

	# Prints the response from Cognitive Services.
	def print_response(self, response):
		txt = ""
		for line in response['recognitionResult']['lines']:
			txt += line['text']
		if self.SHOW_RESPONSE:
			if response["status"] == "Succeeded":
				#print(response['recognitionResult']['lines'])
				print("")
				print("==========RESULT==========")
				for line in response['recognitionResult']['lines']:
					print(line['text'])
				print("==========================")
				print("")
			else:
				print("Processing failed:")
				print(response)
		return txt

	#Performs OCR on a single image
	def ocr_one_image(self, image_data):
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
				time.sleep(1)
				r2 = requests.get(response.headers['Operation-Location'], headers={'Ocp-Apim-Subscription-Key': self.SUBSCRIPTION_KEY})
				get_response = r2.json()
				#print(get_response)
			self.print_response(get_response)
			return get_response
		print(response)

	def pic_to_string(image):
		''' Uses PIL and StringIO to save the image to a string for further processing '''
		output_string = BytesIO()
		pil_image.save(output_string, format="JPEG")
		string_contents = output_string.getvalue()
		output_string.close()
		return string_contents

	# Sends an opened image to Azure's cognitive services.
	# returns a JSON object with all the words and bounding boxes in the object.
	# Accepts an array of images.
	def ocr(self, images):
		responses = []

		for image_data in images: 
			ocr_result = self.ocr_one_image(self.pic_to_string(image_data))
			responses.append(ocr_result)

		return responses
