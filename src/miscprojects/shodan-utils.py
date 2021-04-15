import shodan
from itertools import chain, starmap
import pandas as pd


## Shodan Set Up
SHODAN_API_KEY = "LpQnI9CLLWyiSvpfmO1qPrXiZY0bya8U"
api = shodan.Shodan(SHODAN_API_KEY)


## Json Helper Function
def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


## Additional JSON Helper
def flatten_json_iterative_solution(dictionary):
    """Flatten a nested json file"""

    def unpack(parent_key, parent_value):
        """Unpack one level of nesting in json file"""
        # Unpack one level only!!!

        if isinstance(parent_value, dict):
            for key, value in parent_value.items():
                temp1 = parent_key + '_' + key
                yield temp1, value
        elif isinstance(parent_value, list):
            i = 0
            for value in parent_value:
                temp2 = parent_key + '_' + str(i)
                i += 1
                yield temp2, value
        else:
            yield parent_key, parent_value

            # Keep iterating until the termination condition is satisfied

    while True:
        # Keep unpacking the json file until all values are atomic elements (not dictionary or list)
        dictionary = dict(chain.from_iterable(starmap(unpack, dictionary.items())))
        # Terminate condition: not any value in the json file is dictionary or list
        if not any(isinstance(value, dict) for value in dictionary.values()) and \
                not any(isinstance(value, list) for value in dictionary.values()):
            break

    return dictionary


## Shodan Search Execute
try:
        # Search Shodan
        results = api.search('product:elastic GB country:cn')
        # Show the results
        cluster_addresses = []
        print('Results found: {}'.format(results['total']))
        for result in results['matches']:
                nested_ip = json_extract(result, 'ip_str')
                nested_port = json_extract(result, 'port')
                nested_elastic = json_extract(result, 'elastic')
                #nested_port = json_extract(result, 'port')
                #nested_port = json_extract(result, 'port')

                flat_result = flatten_json_iterative_solution(result)

                #print(nested_ip)
                #print('IP: {}'.format(result['ip_str']))
                #print(result['data'])
                #print('')

                pd.json_normalize(result, max_level=2)

                # Indices
                the_indices = list(result["elastic"]["indices"].keys())

                for item in result.items():
                    if(isinstance(item, dict)):
                        print(item.items())


                cluster_addresses.append(nested_ip + ":" + str(nested_port))
except shodan.APIError as e:
        print('Error: {}'.format(e))

pd.set_option("display.max_columns", 60)
pd.set_option('display.width', 1000)
df = pd.json_normalize(result, max_level=2)
df.loc[:, df.columns.str.startswith('elastic')]


# from elasticsearch_dsl import connections, Search
# from elasticsearch import Elasticsearch
#
# #es = elasticsearch.Elasticsearch(['http://80.79.123.186:9200/'])
#
# s = Search(index="wf_organ_20191001").using(Elasticsearch('http://118.144.34.60:10001/')).query("query_string", query="新疆")
#
#
# #Search(using=es, index=*)
# response = s.execute()
#
# print(response)
#
# for hit in response.hits:
#     print(hit)


