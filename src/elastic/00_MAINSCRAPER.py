import os, json, requests, pprint, configparser, uuid
from datetime import datetime
from google.cloud import storage
from google.cloud import logging as glogging
from pybinaryedge import BinaryEdge



#######
### SETUP FUNCTION
#######

def setup_config():
    config = configparser.ConfigParser()
    config.read('keywords.txt')

    #now = datetime.now()
    #date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    writetofile = config['default']['writetofile'] + '_' + str(uuid.uuid1()) + '.json'
    return writetofile, config



######
### PRE-START
######
writetofile, config = setup_config()



######
### REST OF PROGRAM
######

def setup_logging():
    logging_client = glogging.Client()
    log_name = "ehr-log-crun-001"
    return logging_client.logger(log_name)


# Writing Function
def write(data, filename=writetofile):
    f = open(writetofile, "a", encoding="utf-8")
    #f.write(data + '\r\n')
    print("write")
    with open(writetofile, 'a') as outfile:
        outfile.write(data)
        #outfile.write(',')


def complete_run():
    if int(config["default"]["writetolocal"]) == 0:
        ### upload to GCS
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(config["default"]["gcs_bucket"])
            blob = bucket.blob(writetofile)
            blob.upload_from_filename(writetofile)
            os.remove(writetofile)
        except Exception as e:
            print(e)
    else:
        x = 1


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
                if api_results_set > int(config['default']['api_page_results']): # limiting this block of code to 7 API result sets
                    flag = flag + 1
                    break
                else:
                    cluster_target = ip['target']['ip'] + ":" + str(ip['target']['port'])
                    ip_list.append(cluster_target)
                    ip_list_str = ip_list_str + str(cluster_target) + ", "
                    print(cluster_target)
            api_results_set = api_results_set + 1
    print(ip_list_str)
    write(ip_list_str, writetofile)
    write("\n")
    return ip_list

#def get_indices():
    #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_fwf.html


def search_keywords(ip_list):
    ### GLOBAL CLUSTER SEARCHES - REQUESTS
    keywords = config['default']['keywords'].split(',')

    for ip in ip_list:
        for keyword in keywords:
            print("***REQUESTS***\n")
            print(ip, keyword)
            query = 'http://' + ip + '/_search?q=' + keyword + '&pretty'
            #query = 'http://' + ip + '/_cat/indices?s=index&v'

            # Test connection and try querying the cluster
            try:
                r = requests.get(query, timeout=20)
            except Exception as e:
                print(e)
                continue

            # Test for pulling json object
            try:
                json_object = r.json()
                pretty_json = json.dumps(json_object, indent=2)
                pretty_json_decoded = pretty_json.encode('ascii').decode('unicode-escape')

                metadataIpKeyword = ip + "   " + keyword
                print(pretty_json_decoded)


                write(metadataIpKeyword)
                write(pretty_json_decoded)
            except Exception as e:
                print(e)
                continue

    complete_run()

### SPECIFIC INDEX SEARCHES - PANDAS
# load different set of data
# check for indices above XYZ criteria
# search index



######
### START OF THE PROGRAM
######

if __name__ == '__main__':
    ip_list = get_target_ips(config['default']['search'])
    print(ip_list)
    #keyword_list_cn = ['"岳庆芝"'] #'"涉恐人员"','"出入境边检系统"','"黑名单"','"公安部七类重点人员基础信息"','"两客一危"','"新网上办案系统"','"成都市肆零肆网络科技有限公司"']
    search_keywords(ip_list)

