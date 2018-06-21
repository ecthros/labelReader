from PIL import Image
from PIL import ImageFilter
import utils.logger as logger
from utils.rotate import rotate
from io import BytesIO

# Determines if we should show images after cropping them
SHOW_IMAGES = False
# Name of the labels
LABEL_NAME = 'label'

# This method returns the area to crop out of a given image.
# Its input is a line, which comes from the output from darknet.
def extract_info(line, KERAS, DARKNET):
	if KERAS:
		nameplate_info = line.split()
		nameplate_confidence = nameplate_info[1]
		nameplate_left_x = int(nameplate_info[2][1:][:-1])
		nameplate_top_y = int(nameplate_info[3][:-1])
		nameplate_right_x = int(nameplate_info[4][1:][:-1])
		nameplate_bottom_y = int(nameplate_info[5][:-1])
	
		area = (nameplate_left_x, nameplate_top_y, nameplate_right_x, (nameplate_bottom_y))
	elif DARKNET:
		nameplate_info = line.split()
		nameplate_confidence = nameplate_info[1]
		nameplate_left_x = int(nameplate_info[3])
		nameplate_top_y = int(nameplate_info[5])
		nameplate_width = int(nameplate_info[7])
		nameplate_height = int(nameplate_info[9][:-1])
	
		area = (nameplate_left_x, nameplate_top_y, (nameplate_left_x + nameplate_width), (nameplate_top_y + nameplate_height))
	return area

# Uses PIL to crop an image, given its area.
def crop_image(image, area):
	img = Image.open(image)
	cropped_image = img.crop(area)

	# Rotation should happen here
	rotated_image = rotate(cropped_image)

	size = (3200, 3200)
	rotated_image.thumbnail(size, Image.ANTIALIAS)
	
	if SHOW_IMAGES:
		logger.good("Showing cropped image")
		rotated_image.show()


	return rotated_image

# Determines where an asset is in the picture, returning
# a set of coordinates, for the top left, top right, bottom
# left, and bottom right of the tag
# Returns a string, where the string is the contents of the cropped file.
def locate_asset(self, image, lines=""):
	
	cropped_images = []

	for line in str(lines).split('\n'):

		if LABEL_NAME in line:
			# Extract the nameplate info
			area = extract_info(line, self.KERAS, self.DARKNET)
			# Open image
			cropped_images.append(crop_image(image, area))
	if cropped_images == []:
		logger.bad("No label found in image.")
	else:
		logger.good("Found " + str(len(cropped_images)) + " label(s) in image.")
			
	return cropped_images
