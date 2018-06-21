from fuzzywuzzy import fuzz
from fuzzywuzzy import process
bose_qc25 = {
"065252Z80341129AE": "ACTIVE",
"065252Z80571416AE": "DISABLED"
}

DATABASE = {
    "715053-0010": bose_qc25
}


def lookup_database(txt):
	''' Input: 
	txt ((area, string) tuple) - Contains the bounding box of the image and the accompanying string.
	This methodwill look up the string and determine if the product is active or disabled.'''
	if txt is None:
		return
	for line in txt:
		lines = line[1].split('\n')
		max = 0
		bestGuess = "UNKNOWN"
		bestWord = ""
		keys = bose_qc25.keys()
		for l in lines:
			for word in l.split(' '):
				if word != "":
					(guess, confidence) = process.extractOne(word, keys)
					if confidence > max:
						max = confidence
						bestGuess = guess
						bestWord = word
		if bestGuess == "UNKNOWN":
			print("Unknown product - " + str(line[0]))
		else:
			print(bestWord)
			print(str(bose_qc25[bestGuess]) + " product - " + str(line[0]) + ", confidence: " + str(max))

