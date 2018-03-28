#!/usr/bin/env python
#coding=utf-8
# _*_ coding:utf-8 _*_

import urllib
import os
import urllib2
#import requests
from bs4 import BeautifulSoup
import re
import sys
import numpy as np

reload(sys)
sys.setdefaultencoding("utf8")

url = "https://en.wikipedia.org"
#for i in range(100)
pages = set()



def savefile(content, titlename):
	#newpageurl = pageurl[0:6] + pageurl[6:].replace('/', '_')
	titlename = titlename.replace('/', '_')
	name1 =  '/Users/libingzhang/Documents/2018/wiki/' + titlename + '.txt' 
	#if(not (os.path.exists(name))):
	#	os.mkdir(pageurl)
	output = open(name1, 'a+')
	#print >> output,"\n %s" % (pageurl)
	print >> output, "%s" % content
	output.close()
	#output.write(str(content)+"\n")
	

def wiki(pageurl, titlename):
	#newurl = url+pageurl
	try:
		html = urllib.urlopen(url+pageurl).read()
		html = html.decode('UTF-8')
		wikihtml = BeautifulSoup(str(html), "lxml")
		div = wikihtml.find(name = 'div', id = 'mw-content-text')
		#print div
		ps = div.find_all(name = 'p')
		#print << output, "%s" % html
		#print ps
		for p in ps:
			ptxt = p.get_text()
			savefile(ptxt, titlename)
			#print(ptxt)
		print(html)
	except urllib2.URLError, e:
		if hasattr(e,"code"):
			print e.code
		if hasattr(e,"reason"):
			print e.reason


def getlinks(pageurl):
	global pages
 	try:
 		html = urllib.urlopen(url+pageurl)
 	except urllib2.URLError, e:
		if hasattr(e,"code"):
			print e.code
			#getlinks("/wiki/Biomedical_engineering")
		if hasattr(e,"reason"):
			print e.reason
			#getlinks("/wiki/Biomedical_engineering")
		getlinks("/wiki/Biomedical_engineering")
 	obj = BeautifulSoup(html,'html.parser')

 	#for link in obj.find_all("a", href = re.compile("^(/wiki/)")):
 	for link in (obj.find_all("a", title = re.compile("(engineer)|(Bio)|(Medical)|(medical)|(clinic)|(Clinic)|(diag)|(drugs)|(therapy)"))):# or obj.find_all("a", title = re.compile("(Bio)"))): 
 		if link in obj.find_all("a", href = re.compile("^(/wiki/)")):
 			if not re.search("\.(jpg|JPG|svg|gif)$", link["href"]): #and not re.search("^(:)", link["href"]):
 				if 'href' in link.attrs:
 					if link.attrs['href'] not in pages:
 						titlename = link.attrs['title']
 						newPage = link.attrs['href']
 						#print >> output,"\n %s" % (pageurl)
 						wiki(pageurl, titlename)
 						pages.add(newPage)
 						getlinks(newPage)

 						if(len(pages) % 500 == 0):
 							pageurl = "/wiki/Biomedical_engineering"
count = 20
getlinks("/wiki/Biomedical_engineering")
#output.close()
