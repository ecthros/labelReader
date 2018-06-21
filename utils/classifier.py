from abc import ABC, abstractmethod

class Classifier(ABC):
	@abstractmethod
	def initialize(self):
		pass

	@abstractmethod
	def classify_image(self, image):
		pass

	def __init__(self):
		self.initialize()