from PIL import Image
from PIL import ImageFilter
import utils.logger as logger
from utils.rotate import rotate
from config import *
from typing import Tuple, List
import sys
i = 0
def crop_image(image, area:Tuple) -> object:
	''' Uses PIL to crop an image, given its area.
	Input:
		image - PIL opened image
		Area - Coordinates in tuple (xmin, ymax, xmax, ymin) format '''
	img = Image.open(image)
	cropped_image = img.crop(area)

	# Rotation should happen here
	rotated_image = rotate(cropped_image)

	size = (3200, 3200)
	rotated_image.thumbnail(size, Image.ANTIALIAS)
	global i
	rotated_image.save("asdf" + str(i) + ".jpg", "JPEG")
	i += 1

	if SHOW_IMAGES:
		logger.good("Showing cropped image")
		rotated_image.show()

	return rotated_image


def locate_asset(self, image, classifier, lines="") -> List:
	''' Determines where an asset is in the picture, returning
	 a set of coordinates, for the top left, top right, bottom
	 left, and bottom right of the tag
	 Returns:
	 [(area, image)]
	 	Area is the coordinates of the bounding box
	 	Image is the image, opened by PIL.'''
	cropped_images = []

	for line in str(lines).split('\n'):

		if LABEL_NAME + ":" in line:
			# Extract the nameplate info
			area = classifier.extract_info(line)
			# Open image
			cropped_images.append((area, crop_image(image, area)))
	if cropped_images == []:
		logger.bad("No label found in image.")
	else:
		logger.good("Found " + str(len(cropped_images)) + " label(s) in image.")

	return cropped_images
