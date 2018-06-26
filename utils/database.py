from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from typing import Tuple
from abc import ABC, abstractmethod
from utils.logger import *

class Database(object):

	@abstractmethod
	def initialize(self):
		''' This method should return the self.database parameter. self.database should be a dictionary
		with product identifiers as the key and values if they are enabled or not. '''
		pass

	def __init__(self):
		self.database = self.initialize()

	def lookup_database(self, txt:Tuple[Tuple[float, float, float, float], str]):
		''' Input:
		txt ((area, string) tuple) - Contains the bounding box of the image and the accompanying string.
		This methodwill look up the string and determine if the product is active or disabled.'''
		if txt is None:
			return
		products = ""
		for line in txt:
			lines = line[1].split('\n')
			max = 0
			bestGuess = "UNKNOWN"
			bestWord = ""
			keys = self.database.keys()
			for l in lines:
				for word in l.split(' '):
					if word != "":
						(guess, confidence) = process.extractOne(word, keys, scorer=fuzz.token_sort_ratio)
						if confidence > max:
							max = confidence
							bestGuess = guess
							bestWord = word

			if bestGuess == "UNKNOWN":
				print("Unknown product - " + str(line[0]))
			else:
				print(bestWord)
				product = (str(self.database[bestGuess]) + " product (" + bestGuess + ") - " + str(line[0]) + ", confidence: " + str(max))
				products += product
				print(product)
		return products

