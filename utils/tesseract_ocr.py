from utils.ocr import OCR
import pyocr
import pyocr.builders
import sys

class TesseractOCR(OCR):

	def initialize(self):
		tools = pyocr.get_available_tools()
		if len(tools) == 0:
			print("No tools found, do you have Tesseract installed?")
			sys.exit(1) # TODO fix
		self.tool = tools[0]
		self.langs = tool.get_available_languages()

	def ocr(images):
		# TODO: please improve this
		txt = tool.image_to_string(Image.open('tilted.jpg'), lang=langs[0], builder=pyocr.builders.TextBuilder())
		print("==========RESULT==========\n" + txt + "\n==========================")