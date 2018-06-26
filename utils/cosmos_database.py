from utils.database import Database
import pydocumentdb.documents as documents
import pydocumentdb.document_client as document_client
import requests
import traceback
import urllib3
from config import *
from collections import ChainMap

def test_ssl_connection(client):
	try:
		databases = list(client.ReadDatabases())
		return True
	except requests.exceptions.SSLError as e:
		print("SSL error occured. ", e)
	except OSError as e:
		print("OSError occured. ", e)
	except Exception as e:
		print(traceback.format_exc())
	return False

def ObtainClient():
	connection_policy = documents.ConnectionPolicy()
	connection_policy.SSLConfiguration = documents.SSLConfiguration()
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	connection_policy.SSLConfiguration.SSLCaCerts = False
	return document_client.DocumentClient(HOST, {'masterKey': MASTER_KEY}, connection_policy)

def GetDocumentLink(database_id, collection_id, document_id):
	return "dbs/" + database_id + "/colls/" + collection_id + "/docs/" + document_id

class CosmosDatabase(Database):

	def initialize(self):
		client = ObtainClient()
		if test_ssl_connection(client) == True:
			database = client.ReadDocument(GetDocumentLink(DATABASE_ID, COLLECTION_ID, "active_products"))['products']
			if database == []:
				return -1
			self.database = ChainMap(*database)
		else:
			return -1
		return self.database

