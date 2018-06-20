import requests
import json
import time

SUBSCRIPTION_KEY = ""
SHOW_RESPONSE = True

# Prints the response from Cognitive Services.
def print_response(response):
	if SHOW_RESPONSE:
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

#Performs OCR on a single image
def ocr_one_image(image_data):
	request_url = "https://westus.api.cognitive.microsoft.com/vision/v2.0/recognizeText?mode=Printed"
	headers  = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY, 'Content-Type': "application/octet-stream"}
	data	 = image_data

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
			r2 = requests.get(response.headers['Operation-Location'], headers={'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY})
			get_response = r2.json()
			#print(get_response)
		print_response(get_response)
		return get_response
	print(response)

# Sends an opened image to Azure's cognitive services.
# returns a JSON object with all the words and bounding boxes in the object.
# Accepts an array of images.
def ocr(images):
	responses = []

	for image_data in images: 
		ocr_result = ocr_one_image(image_data)
		responses.append(ocr_result)

	return responses

####### Just here for testing #######
if __name__ == "__main__":

	SHOW_RESPONSE = True
	image = "cropped.jpg"
	with open(image, 'rb') as myfile:
		image_data = myfile.read()
		ocr_one_image(image_data)
####################################
