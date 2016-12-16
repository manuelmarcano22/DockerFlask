#!/bin/bash
docker build  -t dockerflask .
if docker ps -a | grep --quiet flask3example; then 
docker stop flask3example
docker rm flask3example ;
fi
docker run --name flask3example -d -p 8000:8000 --net=host dockerflask
#Docker Hub

