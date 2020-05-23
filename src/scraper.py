import requests
import json
import io
import pickle
from pybinaryedge import BinaryEdge
import pandas as pd

writetofile = input("Name of file to write too? \n\n")

# Writing Function
def write(data, filename=writetofile):
    filename2 = "../results/" + writetofile
    f = open(filename2, "a")
    f.write(data + '\r\n')
    f.close()

def get_target_ips(search_query):
    ### BINARYEDGE SEARCH
    be = BinaryEdge('a68a0cb1-3c15-44e6-b79d-1ca7e7ea368d')
    #search_query = 'elasticsearch.docs:>50000 elasticsearch.size_in_bytes:>500000000 elasticsearch.size_in_bytes:<50000000000'

    ### ITERATE THROUGH BINARY EDGE RESULTS
    flag = 0
    api_results_set = 1
    ip_list = []
    ip_list_str = ""
    while flag == 0:
        results = be.host_search(search_query,page=api_results_set)
        # Detect if this is last results set
        if len(results['events'])!=20:
            flag = flag + 1
            break
        # Print targets and add to global list 20 at a time
        else:
            for ip in results['events']:
                if api_results_set > 30: # limiting this block of code to 7 API result sets
                    flag = flag + 1
                    break
                else:
                    cluster_target = ip['target']['ip'] + ":" + str(ip['target']['port'])
                    ip_list.append(cluster_target)
                    ip_list_str = ip_list_str + str(cluster_target) + ", "
                    print(cluster_target)
            api_results_set = api_results_set + 1
    print(ip_list_str)
    write(ip_list_str)
    return ip_list

#def get_indices():
    #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_fwf.html


def search_keywords(ip_list, keywords):
    ### GLOBAL CLUSTER SEARCHES - REQUESTS

    for ip in ip_list:
        for keyword in keywords:
            print("***REQUESTS***\n")
            print(keyword)
            query = 'http://' + ip + '/_search?q=' + keyword + '&pretty'
            #query = 'http://' + ip + '/_cat/indices?s=index&v'

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
                write(json.dumps(json_object, indent=2))
            except:
                continue
            print(ip + "   " + keyword)

### SPECIFIC INDEX SEARCHES - PANDAS
# load different set of data
# check for indices above XYZ criteria
# search index

# START OF THE PROGRAM
ip_list = get_target_ips('elasticsearch.size_in_bytes:>1000000000 country:"US"')
print(ip_list)
#keyword_list = ['patient', 'Bearer', 'Basic', 'https', 'api_key', 'secret', 'private','aws']
keyword_list_cn = ['病毒','海军','清华大学']
keyword_list = ["gmail", "cookie"]
search_keywords(ip_list, keyword_list)

