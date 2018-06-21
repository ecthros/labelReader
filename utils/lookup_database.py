import fuzzywuzzy

bose_qc25 = {
"065252Z80341129AE": "ACTIVE",
"065252Z80571416AE": "DISABLED"
}

DATABASE = {
    "715053-0010": bose_qc25
}


def lookup_database(txt):
	for line in txt:
		for key in bose_qc25.keys():
			if key in line:
				print(bose_qc25[key])

