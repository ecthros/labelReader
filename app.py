#!/usr/bin/python
from flask import Flask, jsonify, request, abort
from robotidentifier import RobotIdentifier


app = Flask(__name__)

i = 0

@app.route('/api/v1.0/image', methods=['POST'])
def classify_image():
	global i
	i += 1
	print(request)
	if not request.data:
		print(request.data)
		abort(400)
	with open("image" + str(i) + ".jpg", "wb") as myfile:
		myfile.write(request.data)
	return jsonify({'return': identifier.find_and_classify("image" + str(i) + '.jpg')}), 201


@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
	global identifier
	identifier = RobotIdentifier()
	app.run(debug=True, host='0.0.0.0', port=80)
