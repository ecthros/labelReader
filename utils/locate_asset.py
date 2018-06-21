from PIL import Image
from PIL import ImageFilter
import utils.logger as logger
from utils.rotate import rotate
from config import *

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
def locate_asset(self, image, classifier, lines=""):
	
	cropped_images = []

	for line in str(lines).split('\n'):

		if LABEL_NAME in line:
			# Extract the nameplate info
			area = classifier.extract_info(line)
			# Open image
			cropped_images.append(crop_image(image, area))
	if cropped_images == []:
		logger.bad("No label found in image.")
	else:
		logger.good("Found " + str(len(cropped_images)) + " label(s) in image.")
			
	return cropped_images
