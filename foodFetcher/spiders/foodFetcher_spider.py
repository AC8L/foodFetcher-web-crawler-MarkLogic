__author__ = 'sazari'
# -*- coding: utf-8 -*-

import scrapy
from foodFetcher.items import foodFetcherItem

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import uuid
import re
import hashlib
from datetime import datetime

class foodFetcherSpider(CrawlSpider):
    name = 'foodFetcher'
    allowed_domains = ['localhost']
    start_urls = ['http://localhost']
        
    def __init__(self, urlList, ignoreRegexList, allowDomains):
        if urlList:
            with open(urlList, 'r') as f:
                self.start_urls = f.readlines()
        if ignoreRegexList:
            with open(ignoreRegexList, 'r') as f:
                self.ignore_rules = f.readlines()
        if allowDomains:
            with open(allowDomains, 'r') as f:
                self.allowed_domains = f.readlines()
                
    def parse(self, response):
        for href in response.xpath('*//a/@href'):
            full_url = response.urljoin(href.extract())
            self.logger.info('-------%s extracted url: %s', self.name, full_url)

            valid_url = True
            for ignore_rule in self.ignore_rules:
                p = re.compile(ignore_rule, re.IGNORECASE)
                if not p.search(full_url) == None:
                    valid_url = False
                    self.logger.info('-------%s extracted url: %s matching ignore rule: %s', self.name, full_url, ignore_rule)
                    break
                
            if valid_url:
                yield scrapy.Request(full_url, callback=self.parse_response)

    def parse_response(self, response):
        self.logger.info('---------------------------------%s crawling: %s', self.name, response.url)
        soup = BeautifulSoup(response.body, "lxml")

        myuuid = str(uuid.uuid4())
        myuuid = myuuid.replace('-', '')
        
        item = foodFetcherItem()
        item['uuid'] = myuuid
        item['crawledTime'] = datetime.utcnow().isoformat()         
        item['title'] = soup.title.string       
        item['url'] = response.url.lower()
        item['fullText'] = self.clean_text(soup)
        item['titleSHA1'] = hashlib.sha1(item['title'].encode('utf-8') ).hexdigest()
        item['urlSHA1'] = hashlib.sha1(item['url'].encode('utf-8') ).hexdigest()
        item['fullTextSHA1'] = hashlib.sha1(item['fullText'].encode('utf-8') ).hexdigest()
        
        yield item
        
    def clean_text(self, soup):
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        txt = '\n'.join(chunk for chunk in chunks if chunk)
        txt = txt.replace('\n', ' ').replace('\r', '')
        txt = re.sub(u"[^\x20-\x7f]+",u"",txt)
        return txt
