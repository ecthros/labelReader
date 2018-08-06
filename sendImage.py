import sys
import requests
import time

start = time.time()

if len(sys.argv) != 2:
    print("USAGE: sendImage.py <Image_File>")

with open(sys.argv[1], 'rb') as myfile:
    image = myfile.read()

headers = {'Content-Type': 'application/octet-stream'}
request_url = "REQUEST_URL"

response = requests.post(request_url, headers=headers, data=image)
end = time.time()
print(response)
print(response.json()['return'])
print("Time Elapsed: " + str(end-start))
