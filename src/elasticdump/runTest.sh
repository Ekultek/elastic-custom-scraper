#!/bin/bash

while read -r line; do
 elasticdump --input=https://elastic:CgQoeyLP7vSs3QcVpFrYOEiI@theromanceofthe3kingdoms.es.us-central1.gcp.cloud.es.io:9243/$line --output=$line.json --limit 500 --sourceOnly --noRefresh --fileSize 50 MB
done < bactria.txt 
