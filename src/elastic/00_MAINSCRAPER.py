import json
import requests
import pprint
from pybinaryedge import BinaryEdge

writetofile = input("Name of file to write too? \n\n")
writetofile_meta = ''

# Writing Function
def write(data, filename=writetofile):
    filename2 = "../../results/json/" + writetofile
    #f = open(filename2, "a", encoding="utf-8")
    #f.write(data + '\r\n')
    print("write")
    with open(filename2, 'a') as outfile:
        outfile.write(data)
        #outfile.write(',')
def get_target_ips(search_query):
    ### BINARYEDGE SEARCH
    be = BinaryEdge('9e580d9d-13ca-4ac6-8f2d-791a67ce4eca')
    #search_query = 'elasticsearch.docs:>50000 elasticsearch.size_in_bytes:>500000000 country:"CN"'

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
                if api_results_set > 20: # limiting this block of code to 7 API result sets
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
            print(ip, keyword)
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
                pretty_json_decoded = pretty_json.encode('ascii').decode('unicode-escape')

                print(ip + "   " + keyword)
                print(pretty_json_decoded)


                print("maybe write")
                write(pretty_json_decoded)
            except:
                print("ERROR")
                continue


### SPECIFIC INDEX SEARCHES - PANDAS
# load different set of data
# check for indices above XYZ criteria
# search index

# START OF THE PROGRAM
#write("hello")
ip_list = get_target_ips('elasticsearch.docs:<1000000000 elasticsearch.docs:>10000 country:"CN"')
print(ip_list)
#keyword_list = ['patient', 'Bearer', 'Basic', 'https', 'api_key', 'secret', 'private','aws']
keyword_list_cn = ['人'] #'"涉恐人员"','"出入境边检系统"','"黑名单"','"公安部七类重点人员基础信息"','"两客一危"','"新网上办案系统"','"成都市肆零肆网络科技有限公司"']
search_keywords(ip_list, keyword_list_cn)

