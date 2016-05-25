#Cleanup up the Database for the foodFetcherCrawl application

USERNAME="admin" #update if required
PASSWORD="admin" #update if required

echo 'Removing the app server and databases'
curl --anyauth --user $USERNAME:$PASSWORD -X DELETE 'http://localhost:8002/v1/rest-apis/foodfetchercrawl-app-server?include=content&include=modules'

echo 'Done.'
