#!/bin/bash

: ${HOST_USER:=pi}
: ${HOST:=armprosthetic}
: ${DEST:=$HOST_USER@$HOST:/home/$HOST_USER/Project/}

for FILE in model_training data common rpi_zero_soft_arm Dockerfile docker-compose.yml requirements.txt
do 
    rsync -r $FILE $DEST
    echo "Copied $FILE to $HOST"
done 