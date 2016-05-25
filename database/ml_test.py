# Test application to ingest small json to MArkLogic database
# using MarkLogic Python API
#
from marklogic.models import Database, Connection, Host, Forest
from marklogic.models.utilities.exceptions import UnexpectedManagementAPIResponse
from requests.auth import HTTPDigestAuth

filename='ml_test.json'
db_name = 'foodFetcherCrawl-db'
ML_DocPath = "/foodFetcherCrawlingResults/ml_test.json"
collection_name = "foodFetcherCrawlCollection"
conn = Connection('localhost', HTTPDigestAuth('admin', 'admin'))
db = Database.lookup(conn, db_name)
if db == None:
    print("Database does not exist")
else:
    db.load_file(conn, filename, ML_DocPath, [ collection_name ])
