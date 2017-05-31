#!/bin/bash
docker build -f Dockerfile -t dockerflask .
if docker ps -a | grep --quiet flask3example; then 
docker stop flask3example
docker rm flask3example ;
fi
#docker run --name  flask3example -d -p 8000:8000 --net=host manuelmarcano22/dockerflask
docker run --name  flask3example -d -p 80:80 -p 8080:8080 --net=host dockerflask
#Open interactive
#docker run --name  flask3example  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix   -it -p 80:80 -p 8080:8080 --net=host dockerflask
#docker run --name  flask3example -it -p 8080:8080 --net=host dockerflask
#Docker Hub
