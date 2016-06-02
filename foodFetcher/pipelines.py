__author__ = 'sazari'
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem

import pathlib
import os
import json
from xml.dom import minidom
import dicttoxml
import xml.etree.ElementTree as ET

from marklogic.models import Database, Connection, Host, Forest
from marklogic.models.utilities.exceptions import UnexpectedManagementAPIResponse
from requests.auth import HTTPDigestAuth

# Pipeline to write crawled output to MarkLogic
# Utilizes official MarkLogic API for Python
# https://developer.marklogic.com/code/marklogic-python
class ProcessingPipeline(object):
    def __init__(self):
        self.name = settings['BOT_NAME']
        self.OUTFolder = settings['OUT_FOLDER']
        log.msg("---{0} OUT_FOLDER={1}".format(self.name, self.OUTFolder), level=log.DEBUG)
        if not os.path.exists(self.OUTFolder):
            os.makedirs(self.OUTFolder)

        self.fmt = settings['MARKLOGIC_FORMAT']
        self.DO_MarkLogic = settings['MARKLOGIC_UPLOAD']
        if self.DO_MarkLogic:
            self.KeepOrig = settings['MARKLOGIC_KEEP_ORIGINAL_FILE']
            self.ML_Host = settings['MARKLOGIC_HOSTNAME']
            log.msg("---{0} MARKLOGIC_HOSTNAME={1}".format(self.name, self.ML_Host), level=log.DEBUG)
            self.admin = settings['MARKLOGIC_ADMIN']
            self.password = settings['MARKLOGIC_PASSWORD']
            self.db_name = settings['MARKLOGIC_DB']
            log.msg("---{0}: MarkLogic Database initialization: {1}".format(self.name, self.db_name), level=log.DEBUG)
            self.conn = Connection(self.ML_Host, HTTPDigestAuth(self.admin, self.password))
            self.db = Database.lookup(self.conn, self.db_name)
            if self.db == None:
                log.msg("---{0}: MarkLogic Database {1} does not exist, creating on host: {2}.".format(self.name, self.db_name, self.ML_Host), level=log.DEBUG)
                hosts = Host.list(self.conn)
                self.db = Database(self.db_name, hosts[0])
                self.db.create(self.conn)
            else:
                log.msg("---{0}: MarkLogic Database {1} already exists on host: {2}.".format(self.name, self.db_name, self.ML_Host), level=log.DEBUG)                    
    
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            file_path = os.path.join(self.OUTFolder, item['urlSHA1']) + '.' + self.fmt
            if not os.path.isfile(file_path):
                with open(file_path, 'w') as f:
                    if self.fmt.lower() == 'xml':
                        out_str = self.Item2XML(item)
                    elif self.fmt.lower() == 'json':
                        out_str = self.Item2Json(item)
                    else:
                        raise DropItem("---{0}: invalid MarkLogic data format {1}!".format(self.fmt))
                        
                    f.write(out_str)
                    log.msg("---{0} Crawl Results were written to {1} file!".format(self.name, self.fmt), level=log.DEBUG, spider=spider)

                if self.DO_MarkLogic:
                    ML_DocURI = "/{0}CrawlingResults/{1}.{2}".format(self.name, item['urlSHA1'], self.fmt)
                    log.msg("---{0} Crawl MarkLogic Pipeline. Trying to ingest {1}".format(self.name, ML_DocURI), level=log.DEBUG, spider=spider)
                    coll_name = "{0}CrawlingResults".format(self.name)
                    self.db.load_file(self.conn, file_path, ML_DocURI, [ coll_name ])
                    log.msg("---{0} Crawl Results were written to MarkLogic database!".format(self.name), level=log.DEBUG, spider=spider)
                    if not self.KeepOrig:
                        os.remove(file_path)
            else:
                log.msg("---{0} Crawl duplicate url results found, ignoring!".format(self.name), level=log.DEBUG, spider=spider)
            
        return item

    def Item2XML (self, item):
        root_name = "{0}CrawlingResult".format(self.name)
        my_xml = ET.Element( root_name )
        my_id = ET.SubElement(my_xml, 'uuid')
        my_time = ET.SubElement(my_xml, 'crawledTime')
        my_url = ET.SubElement(my_xml, 'url')
        my_title = ET.SubElement(my_xml, 'title')
        my_fullText = ET.SubElement(my_xml, 'fullText')
        my_titleSHA1 = ET.SubElement(my_xml, 'titleSHA1')
        my_urlSHA1 = ET.SubElement(my_xml, 'urlSHA1')
        my_fullTextSHA1 = ET.SubElement(my_xml, 'fullTextSHA1')

        my_id.text = item['uuid']
        my_time.text = item['crawledTime']
        my_url.text = item['url']
        my_title.text = item['title']
        my_fullText.text = item['fullText']
        my_urlSHA1.text = item['urlSHA1']
        my_titleSHA1.text = item['titleSHA1']
        my_fullTextSHA1.text = item['fullTextSHA1']
        out_str = ET.tostring(my_xml, 'utf-8')
        reparsed = minidom.parseString(out_str)
        out_str = reparsed.toprettyxml(indent="  ")
        if not isinstance(out_str, str):
            out_str = out_str.decode("UTF-8")
        return out_str

    def Item2Json(self, item):
        return json.dumps(dict(item))


