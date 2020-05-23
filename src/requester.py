import requests
import pandas as pd

headers = {
    'accept': "application/json",
    'apikey': "jgmfGzQL6sTuupwAqDK3jiKJXy8YDw9z"
    }

writetofile = input("Name of file to write too? \n\n")
siteorcsv = input("Check out a specific site or load default CSV? Please, no http:// or www if entering site. Simply enter 'default' to use default CSV \n\n")

def write(data, filename=writetofile):
    f = open(filename, "a")
    f.write(data + '\r\n')
    f.close()

if siteorcsv == "default":
    df = pd.read_csv('sitelist.csv')
else:
    df = {}
    df["API_SITE"] = siteorcsv
    print(siteorcsv)

for specurl in df["API_SITE"]:
    if len(specurl) < 2:
        specurl = siteorcsv

    api_endpoint = "https://api.securitytrails.com/v1/domain/" + specurl + "/subdomains"
    response = requests.request("GET", api_endpoint, headers=headers, timeout=7)
    json_data = response.json()
    count = 0
    print(json_data)
    for subdomain in json_data["subdomains"]:
        final_count = len(json_data["subdomains"])
        request_subdomain = "http://" + subdomain + "." + specurl
        print(request_subdomain + " " + str(count) + '/' + str(final_count))
        count = count + 1
        try:
            r = requests.head(request_subdomain, timeout=3)
            status_result = str(r.status_code) + "," + request_subdomain
            print(status_result + "\n")
            write(status_result)
        except:
            print("TIMEOUT!")
            continue


