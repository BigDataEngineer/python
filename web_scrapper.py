import urllib.request
import re
from bs4 import BeautifulSoup
import sys

processed_page_list=[]
master_list_uniq_fqdn_url_list=[]
counter_get_url_page=0
counter_get_links=0
wds_list={}
biggest_v=None
most_frequent_word=None

def get_url_page(url):
    global wds_list
    global counter_get_url_page
    global wds_list
    global biggest_v
    global most_frequent_word
    print('most_frequent_word, occurence',most_frequent_word,biggest_v)
    counter_get_url_page=counter_get_url_page+1
    print('counter_get_url_page',counter_get_url_page)
    try:
        url_response=urllib.request.urlopen(url)
    except Exception as ex:
        print(url)
        print(processed_page_list)
        print(ex)
    try:
        data=url_response.read().decode()
    except Exception as ex:
        print('Exception raised')
        print(ex)
        #print(processed_page_list)
        #print(master_list_uniq_fqdn_url_list)
        #print(wds_list)
        print('most_frequent_word, occurence',most_frequent_word,biggest_v)
        sys.exit(1)
    lines_list=data.splitlines()
    for line in lines_list:
        line=line.strip()
        words=line.split()
        for word in words:
            wds_list[word]=wds_list.get(word,0)+1
    for (k,v) in wds_list.items():
        if biggest_v is None or v>biggest_v:
            biggest_v=v
            most_frequent_word=k
    #get_links(data,url)
    processed_page_list.append(url)
    #return(data,url)

    lines_list=data.splitlines()

    for line in lines_list:
        line=line.strip()
        words=line.split()
        for word in words:
            wds_list[word]=wds_list.get(word,0)+1
    get_links(data,url)

def get_links(data,url):
    global counter_get_links
    global most_frequent_word
    global initial_url
    counter_get_links=counter_get_links+1
    print('counter_get_links',counter_get_links,url)
    soup = BeautifulSoup(data, 'html.parser')
    href_list=[]
    fqdn_url_list=[]
    for i in soup.findAll('a'):
        try:
            href_list.append(i.get('href').strip())
        except:
            print('something went wrong')
            print(url)
            print('most_frequent_word, occurence',most_frequent_word,biggest_v)
            continue
    for i in href_list:
        if re.search(r'^/',i):
            print(i)
            fqdn_url_list.append(initial_url+i)

    uniq_fqdn_url_list=[]
    for i in fqdn_url_list:
        if i not in uniq_fqdn_url_list:
            uniq_fqdn_url_list.append(i)
    #print(uniq_fqdn_url_list)
    for i in uniq_fqdn_url_list:
        if i not in master_list_uniq_fqdn_url_list:
            master_list_uniq_fqdn_url_list.append(i)
    for i in master_list_uniq_fqdn_url_list:
        if i not in processed_page_list:
            get_url_page(i)

    #return uniq_fqdn_url_list

initial_url=input('Enter URL:')
get_url_page(initial_url)


#data_from_get_url_page,url_from_get_url_page=get_url_page(initial_url)
#list_from_uniq_fqdn_url_list=[]
#list_from_uniq_fqdn_url_list=get_links(data_from_get_url_page,url_from_get_url_page)
