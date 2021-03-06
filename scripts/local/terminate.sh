echo "Terminating local environment"
echo -e "----------------------------\n"
NETWORK_NAME='feedbacksaverapi'
DB_CONTAINER_NAME='samdbfeedbacksaverapi'
LOCAL_DB_PATH='/database/dynamodb'
LOCAL_DB_PORT=8000

echo "\n1. Dynamodb"
echo -e "----------------------------\n"

echo "Stopping dynamodb container $DB_CONTAINER_NAME"
docker network disconnect "$NETWORK_NAME" "$DB_CONTAINER_NAME"
docker stop "$DB_CONTAINER_NAME"
docker rm "$DB_CONTAINER_NAME"

echo "\n2. Network"
echo -e "----------------------------\n"
echo "Deleting $NETWORK_NAME"

docker network rm "$NETWORK_NAME"

echo -e "----------------------------\n"
echo "Finished"
