from fuzzywuzzy import fuzz

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
		for key in bose_qc25.keys():
			lines = line[1].split('\n')
			for l in lines:
				for word in l.split(' '):
					if fuzz.ratio(key, word) > 80:
						print(line[0])
						print(bose_qc25[key])

