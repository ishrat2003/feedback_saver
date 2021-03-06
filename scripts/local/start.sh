echo "Starting local environment"
echo -e "----------------------------\n"
NETWORK_NAME='feedbacksaverapi'
DB_CONTAINER_NAME='samdbfeedbacksaverapi'
LOCAL_DB_PATH='/database/dynamodb'

sam build --template-file ./api/template.yaml

# pip3 install -U nltk
# python3 -m nltk.downloader punkt -d ./story-survey-api/nltk
# python3 -m nltk.downloader averaged_perceptron_tagger -d ./story-survey-api/nltk
# python3 -m nltk.downloader stopwords -d ./story-survey-api/nltk

echo "\n1. Network"
echo -e "----------------------------\n"

echo "Deleting $NETWORK_NAME"
docker network rm "$NETWORK_NAME"

echo "Creating $NETWORK_NAME"
docker network create -d bridge "$NETWORK_NAME"


echo -e "\n2. Dynamodb"
echo -e "----------------------------\n"

echo "Stopping dynamodb container $DB_CONTAINER_NAME"
docker rm "$DB_CONTAINER_NAME"

echo "Starting dynamodb container $DB_CONTAINER_NAME"
echo "$PWD$LOCAL_DB_PATH/data:/home/dynamodblocal/data"
docker run -d -v "$PWD$LOCAL_DB_PATH/data:/home/dynamodblocal/data" -p 8000:8000 --network "$NETWORK_NAME" --name "$DB_CONTAINER_NAME" amazon/dynamodb-local -jar DynamoDBLocal.jar -dbPath '/home/dynamodblocal/data'

echo -e "\n3. Starting application"
echo -e "----------------------------\n"

echo "Validating Cloud Formation template"
sam validate --template-file ./api/template.yaml 

echo "Starting"
sam local start-api  --template-file ./api/template.yaml  --env-vars env.json --port 3500

echo -e "----------------------------\n"
echo "Finished"
