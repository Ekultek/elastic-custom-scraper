import requests

writetofile = input("Name of file to write too? \n\n")
siteorcsv = input("Check out a specific site or load default CSV? Please, no http:// or www if entering site. Simply enter 'default' to use default CSV \n\n")


def write(data, filename=writetofile):
    f = open(filename, "a")
    f.write(data + '\r\n')
    f.close()


def write_array(lines, filename):
    for line in lines:
        f = open(filename, "a")
        f.write(line + '\r\n')
        f.close()


def get_domain_status(url):
    return requests.head(url, timeout=3).status_code


def get_request(url, c_headers):
    return requests.request("GET", url, headers=c_headers, timeout=7)


def file_to_array(filename):
    with open(filename) as file_in:
        lines = []
        for line in file_in:
            lines.append(line.rstrip())
    print('LOADED ' + str(len(lines) + ' DOMAINS'))
    return lines


def get_domains_from_file(u_input):
    switcher = {
        'default': 'sitelist.txt',
        'test': 'this_file.txt',
    }
    return file_to_array(switcher.get(u_input, u_input))  # switcher.get(input, default_response)


def loop_and_check_domains(domain_list):
    for domain in domain_list:
        response = get_request("https://api.securitytrails.com/v1/domain/" + domain + "/subdomains",
                               { 'accept': "application/json", 'apikey': "jgmfGzQL6sTuupwAqDK3jiKJXy8YDw9z" })
        json_data = response.json()
        print(json_data)
        write_array(json_data["subdomains"], 'subdomains/'+domain+'.txt')
        for subdomain in json_data["subdomains"]:
            final_count = len(json_data["subdomains"])
            request_subdomain = "http://" + subdomain + "." + domain
            print(request_subdomain + " " + str(count) + '/' + str(final_count))
            count = count + 1
            try:
                status_result = str(get_domain_status(request_subdomain)) + "," + request_subdomain
                print(status_result + "\n")
                write(status_result)
            except:
                print("TIMEOUT!")
                continue


loop_and_check_domains(get_domains_from_file(siteorcsv))
