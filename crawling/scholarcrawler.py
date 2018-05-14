#!/usr/bin/env python3

import argparse
import logging
import math
import os.path
import sys
import time
import requests
import urllib
import threadpool
import telnetlib
import selenium
import random
import pandas as pd
from urllib.parse import urlparse
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase

class googlescholarSpider():
    name = "Google Scholar"
    allowed_domains = ["google.com"]
    start_urls = ["http://scholar.google.com/"]

    def __init__(self, start_url='', *args, **kwargs):
        citation_get()
        if start_url:
            self.start_urls = [start_url]
        super(googlescholarSpider, self).__init__(*args, **kwargs)
    
    def storenodes(self, eo1, eo2, eotype):
        co_writer_1 = citation[0:eo1]
        co_writer_2 = citation[eo1+1:eo2]
        publication_name = citation[eo2+1:eotype]

    list_css_rules = {
        '.gs_r': {
            'citation-text': '.gs_fl > a:nth-child(1)::text',
            'citation-url': '.gs_fl > a:nth-child(1)::attr(href)',
        }
    }
    
 

def tnt(L):  
    tn = telnetlib.Telnet(L[0])  
    time.sleep(2)  
    ...  
    idx = tn.expect(["Username:", "login:"], timeout=5)  
    ...  
    time.sleep(3)  
    x = tn.read_very_eager()  
    tn.close()  
    ...  
    return

pool = threadpool.ThreadPool(10)
requests = threadpool.makeRequests()
pool = ThreadPool(poolsize)
pool.putRequest(req)
session = requests.Session()
global citation_num

pick_brow = random.randint(1,5)
if pick_brow == 1:
    browser = webdriver.Chrome()
elif pick_brow == 2:
    browser = webdriver.Firefox()
elif pick_brow == 3:
    browser = webdriver.Safari()
elif pick_brow == 4:
    browser = webdriver.InternetExplorer()
elif pick_brow == 5:
    browser = webdriver.PhantomJS()

REQUEST_HEADERS = {"User-Agent": browser, "Accept-Charset": "UTF-8,*;q=0.5"}

parser = argparse.ArgumentParser(description='google scholar citation reachout')
parser.add_argument('-URL_1st page', type=str, help='first page')
parser.add_argument('-TIME_interval', action='store', type=int, default=random.randint(20,100),
                    help='request interval')
parser.add_argument('-FORMAT', action='store', const=True, default=False,
                    help='Download format')
parser.add_argument('-CIT_name', action='store', default="citation.bib",
                    help='Citation format')
opts = parser.parse_args()

def queue():
    if query.find(',') < 0:
        return query
    phrases = []
    for phrase in query.split(','):
        phrase = phrase.strip()
        if phrase.find(' ') > 0:
            phrase = '"' + phrase + '"'
        phrases.append(phrase)
    return ' '.join(phrases)


def each_citation():
    if not os.path.exists(opts.citation_name):
        with open(opts.citation_name, 'w+') as f:
            f.write("% -*-coding: utf-8 -*-\n\n")
        return 0
    with open(opts.citation_name, 'r') as f:
        citation_list = f.readlines()
        i = len(citation_list) - 1
        while i > -1:
            if citation_list[i].startswith("% ["):
                break
            else:
                i -= 1
        if i < 0:
            return 0
        last_line = citation_list[i].strip()
        start_number = int(last_line[last_line.index('[') + 1: last_line.index(']')])
        return start_number


def citation_get():
    total_citations_num = get_total_citations_num()
    citation_num = each_citation()
    
    if citation_num > total_citations_num:
        sys.exit(2)
        
    #properties
    papers_per_page = 10
    citation_num_total = 0
    page_num = 0
    
    while True:
        params = {"cstart": papers_per_page * page_num, "pagesize": papers_per_page}
        soup = thisbs(opts.google_scholar_uri, params)
        paper_records = soup("tr", {"class": 'gsc_a_tr'})
        
        for p in paper_records:
            
            paper_title = p.find('a', {"class": "gsc_a_at"}).getText()
            citations_anchor = p.find('a', {"class": 'gsc_a_ac'})
            
            if citations_anchor['href']:
                
                citation_num_curr_paper = int(citations_anchor.getText())
                citation_num_total += citation_num_curr_paper
                
                if citation_num_total <= citation_num:
                    continue
                
                start_index = citation_num_curr_paper - (citation_num_total - citation_num)
                get_citations_by_paper(citations_anchor['href'], citation_num_curr_paper, start_index)

            else:
                continue

        next_button = soup.find('button', {"id": "gsc_bpf_next"})
        if "disabled" in dict(next_button.attrs):
            break
        else:
            page_num += 1


def get_total_citations_num():
    """
    Get the total citation number from user's google scholar homepage
    """
    soup = thisbs(opts.google_scholar_uri)
    total_citations_num = int(soup("td", {"class": "gsc_rsb_std"})[0].getText())
    return total_citations_num


def get_citations_by_paper(citations_uri, count, start_index):
    for c in range(0, int(math.ceil((count - start_index) / 10.0))):
        soup = thisbs(citations_uri, {"start": c * 10 + start_index})
        for citation_record in soup('div', {"class": "gs_r"}):
            save_citation(citation_record)


def save_citation(citation_record):
    cite_anchor = citation_record.find('a', {'class': 'gs_nph'})
            
    if not cite_anchor or not cite_anchor['onclick']:
        return
    
    citation_id = cite_anchor['onclick'].split(',')[1][1:-1]
    params = {"q": "info:%s:scholar.google.com/" % citation_id, "output": "cite"}
    soup = thisbs("https://scholar.google.com/scholar", params)
    bib_anchor = soup.find('a', {"class": "gs_citi"})
    
    if not bib_anchor:
        return
    
    soup = thisbs(bib_anchor['href'])
    citation_num += 1

    citation_entry = bibtexparser.loads(soup.getText()).entries[0]
    citationID = citation_entry['ID'] # e.g., melville2004review
    citation_entry["gscholar_id"] = citation_id
    g_bib_entry = bibtexparser.dumps(db)
    bib_entry = "%% [%d]\n%s" % (citation_num, g_bib_entry)
    
    with open(opts.citation_name, "ab+") as f:
        f.write(bib_entry.encode('utf-8'))


def thisbs(page_url, params=None):
    try:
        time.sleep(opts.request_interval)
        res = session.get(page_url, params=params, headers=REQUEST_HEADERS, timeout=10)
        res.encoding = 'UTF-8'
        if res.status_code != 200:
            raise Exception("Bad response status code %d" % res.status_code)
        soup = BeautifulSoup(res.text, "html.parser")
        if soup.h1 and soup.h1.text == "Please show you're not a robot":
            raise Exception("Meeting captcha errors")
        return soup
    except Exception as err:
        sys.exit(1)


def main():
    if opts.should_download and not os.path.exists(opts.download_dir):
        os.mkdir(opts.download_dir)
    citation_get()
    #queue()
    


if __name__ == "__main__":
    client = MongoClient(host='localhost', port=27017)
    db=client['test']
    collection = db['BME']
    main()
