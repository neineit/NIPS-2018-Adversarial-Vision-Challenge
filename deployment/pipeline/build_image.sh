#!/bin/bash

echo "Retrieving model version and model folder name .."

MODEL_VERSION=$( echo $2 | grep -o '[0-9.a-zA-Z]*$')
MODEL_FOLDER=${2%-$MODEL_VERSION}
BUCKET_NAME_ARG=$3
ZONE=$4
PROJECT_ID=$1
INSTANCE_NAME=$( echo $2 | sed 's/\./-/g')


echo "Model Folder: $MODEL_FOLDER"
echo "Model Version: $MODEL_VERSION"

echo "Update repositories .."
apt-get update 

echo "Update required libs .."
apt-get install -y apt-transport-https ca-certificates curl software-properties-common curl

echo "Add GPG keys .."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

echo "Add official Docker repository .."
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

echo "Update repositories .."
apt-get update 

echo "Install docker .."
apt-get install -y docker-ce

cp -r vq-layer $MODEL_FOLDER

echo "Building Docker Image .."
docker build -t gcr.io/$PROJECT_ID/$MODEL_FOLDER:$MODEL_VERSION  --build-arg INSTANCE_NAME_ARG=$INSTANCE_NAME --build-arg ZONE_ARG=$ZONE --build-arg PROJECT_ID_ARG=$PROJECT_ID --build-arg MODEL_ID_ARG=$MODEL_FOLDER-$MODEL_VERSION --build-arg BUCKET_NAME_ARG=$3 $MODEL_FOLDER

echo "Pushing Docker Image .."
docker push gcr.io/$PROJECT_ID/$MODEL_FOLDER:$MODEL_VERSION