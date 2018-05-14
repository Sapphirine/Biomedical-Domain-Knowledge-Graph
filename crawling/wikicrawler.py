# -*- coding: utf-8 -*-
"""
@author: YC.L
"""

import sys
import time
import argparse
import re
import requests
import urllib
from urllib.parse import urlparse
from pymongo import MongoClient
from bs4 import BeautifulSoup


t = 5.0
graphs = 3
agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
url = "https://en.wikipedia.org"
pages = set()  
links = []


def load_urls(session_file):

    try:
        with open(session_file) as fin:
            for line in fin:
                visited_urls.add(line.strip())
    except FileNotFoundError:
        pass


def scrap(base_url, article, output_file, session_file):

    full_url = base_url + article
	try:
		html = urllib.request.urlopen(url+pageurl)
	except urllib.error.URLError as e:
		if hasattr(e,"code"):
			print (e.code)
			#getlinks("/wiki/Biomedical_engineering")
		if hasattr(e,"reason"):
			print (e.reason)
			#getlinks("/wiki/Biomedical_engineering")
		getlinks("/wiki/Biomedical_engineering")
	obj = BeautifulSoup(html,'html.parser')
	t = {}
	t['name']=pageurl
 	#for link in obj.find_all("a", href = re.compile("^(/wiki/)")):
	for link in (obj.find_all("a", title = re.compile("(engineer)|(Bio)|(Medical)|(medical)|(clinic)|(Clinic)|(diag)|(drugs)|(therapy)"))):# or obj.find_all("a", title = re.compile("(Bio)"))): 
		if link in obj.find_all("a", href = re.compile("^(/wiki/)")):
 			if not re.search("\.(jpg|JPG|svg|gif)$", link["href"]): #and not re.search("^(:)", link["href"]):
 				if 'href' in link.attrs:
 					if link.attrs['href'] not in pages:
 						titlename = link.attrs['title']
 						newPage = link.attrs['href']
 						titlename.replace('.', '1')
 						titlename.replace('_', '1')
 						titlename.replace('$', '1')
 						t[titlename] = newPage
 						#print >> output,"\n %s" % (pageurl)
 						wiki(pageurl, titlename)
 						pages.add(newPage)
 						findlist.append(newPage)
	print(t)
	collection.insert_one(t)

	thispage = findlist[0]
	del findlist[0]
	getlinks(thispage, client, db, collection)

	if full_url in visited_urls:
		return
	visited_urls.add(full_url)
    

def main():
    initial_url = "/wiki/Biomedical_engineering"
    pending_urls.append(initial_url)

    counter = 0
    while len(pending_urls) > 0:
        try:
            counter += 1
            if counter > articles_limit:
                break
            try:
                next_url = pending_urls.pop(0)
            except IndexError:
                break

            time.sleep(interval)
            article_format = next_url.replace('/wiki/', '')[:35]
            print("{:<7} {}".format(counter, article_format))
            scrap(base_url, next_url, output_file, session_file)
        except KeyboardInterrupt:
            input("\n> PAUSED. Press [ENTER] to continue...\n")
            counter -= 1



if __name__ == '__main__':
    client = MongoClient(host='localhost', port=27017)
    db=client['test']
    #db.authenticate("fxghjmf11","wretchmaycry")
    collection = db['BME']
    main()