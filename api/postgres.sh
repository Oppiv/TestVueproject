#!/usr/bin/env bash

container_name='demo-lesson-postgres'

docker stop "$container_name" && docker rm "$container_name"
docker run -d --name "$container_name" -p 5435:5432 -e POSTGRES_PASSWORD=master postgres:16 || echo "failed!"

echo -e "\nGREAT SUCCESS\n"
