#!/bin/bash

docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -v mysql_data:/mnt/d/mysql/data -d mysql:8.0.42

