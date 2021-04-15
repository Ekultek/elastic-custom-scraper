# Elasticdump Tool

### Introduction

- If you find a cluster on the internet and want to download it, run Elasticdump. A great tool.

### Prerequisites:

- Homebrew installed
- NPM/NodeJS installed

### Instructions:

1. Go to the address of the database. Something like `<clusterip>:9200/_cat/indices?s=docs.count&v`. Copy all index names.
   Use Google Sheets or Excel to split the data into columns and retrieve just the index names.
2. Past all index names you want to download into `index_names.txt`
3. Run `./download_indices.sh` from the Terminal. Most of the time, you can remove the $User and $Password variable. Also you
will need to adjust for HTTP vs HTTPS. Defaults to the latter.
