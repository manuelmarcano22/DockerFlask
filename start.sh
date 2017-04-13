#!/bin/bash
source activate iraf27
#python /root/simpleapp.py -p 80
uwsgi --http-socket 127.0.0.1:8080 -w wsgi --master --processes 4 --threads 2 --stats 127.0.0.1:9191

