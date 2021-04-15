#!/bin/bash

#user="elastic"
#password="editme"
url="192.168.0.1"
port="9200"

while read -r line; do
 elasticdump --input=https://$user:$password@$url:$port/$line --output=$line.json --limit 500 --sourceOnly --noRefresh --fileSize 400 MB
done < index_names.txt

#while read -r line; do
 #elasticdump --input=https://$user:$password@$url:$port/$line --output=$line.json --limit 500 --sourceOnly --noRefresh --fileSize 400 MB
#done < index_names.txt