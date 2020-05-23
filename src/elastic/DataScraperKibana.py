import requests
import csv

field_names = ['IP', 'indice_name', 'size']

def main():
    print('Started...')
    #openKibanaList()
    #testParsing()

def testParsing():
    searchKibana('http://100.25.105.61:5601/api/console/proxy?path=_cat/indices&method=GET', '100.25.105.61:5601')

def openKibanaList():
    with open('data/Kibana.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            url = "http://" + row['IP'] + ':' + row['Port'] + "/api/console/proxy?path=_cat/indices&method=GET"
            ip = row['IP'] + ':' + row['Port']
            searchKibana(url, ip)


def searchKibana(url, ip):
    headers = {'kbn-version': ''}
    try:
        request = requests.post(url, data='', headers=headers)
        data = request.text
        test = data.split()
        print(url)
        dumpKibanaData(test, ip)
    except:
        print("Couldn't connect to: " + url)


def dumpKibanaData(data, ip):
    i = 0
    name = ""
    for d in data:
        if i == 0:
            name = ""
        if i == 2:
            name = d
        elif i == 9:
            i = 0
            if d.find("mb") != -1:
                #print(name + " < 1GB")
                continue
            elif d.find("gb") != -1:
                size = float(d.replace("gb", ""))
                size_string = str(size) + "GB"
                list = [ip, name, size_string]
                #print(ip + " : " + name + " : " + str(size) + "GB")
                if size < 10:
                    #print('1 -> 10')
                    append_list_as_row("1-10gb.csv", list)
                elif 10 <= size < 50:
                    #print('10 -> 50')
                    append_list_as_row("10-50gb.csv", list)
                elif 50 <= size < 100:
                    #print('50 -> 100')
                    append_list_as_row("50-100gb.csv", list)
                elif 100 <= size < 500:
                    #print('100 -> 500')
                    append_list_as_row("100-500gb.csv", list)
                elif 500 <= size < 1000:
                    #print('500 -> 1000')
                    append_list_as_row("500-1000gb.csv", list)
            elif d.find("tb") != -1:
                size = float(d.replace("tb", ""))
                size_string = str(size) + "TB"
                list = [ip, name, size_string]
                #print(ip + " : " + name + " : " + str(size) + "TB")
                if size < 10:
                    #print('1 -> 10')
                    append_list_as_row("1-10tb.csv", list)
                elif 10 <= size < 50:
                    #print('10 -> 50')
                    append_list_as_row("10-50tb.csv", list)
                elif 50 <= size < 100:
                    #print('50 -> 100')
                    append_list_as_row("50-100tb.csv", list)
                elif 100 <= size < 500:
                    #print('100 -> 500')
                    append_list_as_row("100-500tb.csv", list)
                elif 500 <= size < 1000:
                    #print('500 -> 1000')
                    append_list_as_row("500-1000tb.csv", list)
            continue
        i += 1


def append_list_as_row(file_name, list_of_elem):
    with open('elastic/' + file_name, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(list_of_elem)
        print(list_of_elem)


if __name__ == '__main__':
    main()