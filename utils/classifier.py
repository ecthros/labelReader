from abc import ABC, abstractmethod

class Classifier(ABC):
	@abstractmethod
	def initialize():
		pass

	@abstractmethod
	def classify_image(image):
		pass

	def __init__(self):
		self.initialize()