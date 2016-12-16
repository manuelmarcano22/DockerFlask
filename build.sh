docker build  -t dockerflask .
docker stop flask3example
docker rm flask3example
docker run --name flask3example -d -p 8000:8000 --net=host flask3
#Docker Hub
