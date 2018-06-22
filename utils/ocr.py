from abc import ABC, abstractmethod

class OCR(ABC):
	@abstractmethod
	def initialize(self):
		''' Initialize the OCR '''
		pass

	@abstractmethod
	def ocr(self, images):
		''' OCR an image.
		Input: An array of (area, image)s, opened by PIL and pre-processed 
		Return: An array of (area, message), where the message is from OCR'''
		pass

	def __init__(self):
		self.initialize()