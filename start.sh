#!/bin/bash
source activate iraf27
python /root/simpleapp.py -p 8080
#uwsgi --http-socket vimos.manuelpm.me:8080 -w wsgi --master --processes 10 --threads 5 --stats 127.0.0.1:9191 --offload-threads 4

