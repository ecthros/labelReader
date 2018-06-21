from abc import ABC, abstractmethod

class OCR(ABC):
	@abstractmethod
	def initialize(self):
		pass

	@abstractmethod
	def ocr(self, images):
		pass

	def __init__(self):
		self.initialize()