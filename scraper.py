import requests
import json
import io
from pybinaryedge import BinaryEdge
import pandas as pd


def get_target_ips(search_query):
    ### BINARYEDGE SEARCH
    be = BinaryEdge('a68a0cb1-3c15-44e6-b79d-1ca7e7ea368d')
    search_query = 'elasticsearch.docs:>50000 elasticsearch.size_in_bytes:>500000000 elasticsearch.size_in_bytes:<50000000000'

    ### ITERATE THROUGH BINARY EDGE RESULTS
    flag = 0
    count = 1
    api_results_set = 1
    ip_list = []
    while flag == 0:
        results = be.host_search(search,page=count)
        # Detect if this is last results set
        if len(results['events'])!=20:
            flag = flag + 1
            break
        # Print targets and add to global list 20 at a time
        else:
            count = count + 1
            for ip in results['events']:
                if api_results_set > 7: # limiting this block of code to 7 API result sets
                    flag = flag + 1
                    break
                else:
                    cluster_target = ip['target']['ip'] + ":" + str(ip['target']['port'])
                    ip_list.append(cluster_target)
                    print(cluster_target)
            api_results_set = api_results_set + 1
    return api_results_set


def search_keywords(ip_list, keywords):
    f = open('results.json','a')
    ### GLOBAL CLUSTER SEARCHES - REQUESTS
    for ip in ip_list:
        print("***REQUESTS***\n")
        #query = 'http://' + ip + '/_cat/indices?s=index&v'
        query = 'http://' + ip + '/_search?q=*https*&pretty'


        # Test connection and try querying the cluster
        try:
            r = requests.get(query, timeout=20)
        except:
            continue

        # Test for pulling json object
        try:
            json_object = r.json()
            pretty_json = json.dumps(json_object, indent=2)
            print(ip)
            print(pretty_json)
            f.write(pretty_json)
        except:
            continue

        # Pause before continuing to next iteration

        print(ip)
    f.close()
    #sec = input('Let us wait for user input\n')


### SPECIFIC INDEX SEARCHES - PANDAS
# load different set of data
# check for indices above XYZ criteria
# search index

def write(filename, data):
    f = open(filename, "a")
    f.write(data + '\r\n')
    f.close()

# START OF THE PROGRAM
ip_list = get_target_ips('elasticsearch.indices:*logstash* country:"US"')
keyword_list = ['Bearer', 'Basic', 'https', 'api_key', 'secret']
search_keywords(ip_list, keyword_list)

