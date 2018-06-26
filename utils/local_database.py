from utils.database import Database


bose_qc25 = {
"065252Z80341129AE": "Active",
"065252Z80571416AE": "Inactive"
}

DATABASE = {
    "715053-0010": bose_qc25
}

class LocalDatabase(Database):
	def initialize(self):
		return bose_qc25
