REM Setting up the Database for the foodFetcherCrawl application

REM Update if required
SET USERNAME="admin"
SET PASSWORD="admin"

echo "Setting up the app server and databases - "
curl --anyauth --user %USERNAME%:%PASSWORD% -X POST -d@"ML_DB_SETUP.json" -i -H "Content-type: application/json" http://localhost:8002/v1/rest-apis

echo "Done."
