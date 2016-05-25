==================================
foodFetcher spider and web crawler
==================================

I needed a simple web crawler for my academic research to store results in MarkLogic database. While there are many great web crawling tools
over there, some of them are dependent of hadoop and Solr (like Apache Nutch) and some (like in few Scrapy tutorials) were storing results
in MongoDB. In addition, all the sample code I was able to find had problems with content encoding and text extraction. BTW, that applies to Nutch
as well. So, quick research showed that Scrapy was a good framework that would allow building a spider/crawler quickly and integrating a custom
content pipeline. At the same time it is written in python and MarkLogic provides an official API for it. Finally, comparing free text extraction
python libraries, BeautifulSoup apperas to be the most robust for handling mixed text encoding, special characters and html pages with bunch of
garbage in them. Although some fellows complain it is slow but it performs reasonably fast for our purposes.

So, this is how foodFetcher was born. foodFetcher=python,scrapy,BeautifulSoup,MarkLogic.

About
=====
foodFetcher crawls your web sites and stores information in MarkLogic database. It is based on scrapy framework and is written in python.
The output can be stored in MarkLogic database and/or optionally in local file filesystem in either json or xml format.

Prerequisites
=============
	- Python 3 (was developed and tested in 3.5.1)
	- BeautifulSoup4 (python text manipulation library)
	- Scrapy (was developed and tested in 1.1.0)
	- MarkLogic Python API

Installation
=============
Install prerequisites, clone repository and you are ready to go.
foodFetcher was tested and found to run well on Mac OS X (10.11), Centos 7 and on Windows 7 through Cygwin (2.5.1).
On Windows python, scrapy and MarkLogic Python API have to be installed through Cygwin setup tools, not windows installers.
Scrapy has to be installed using pip (pip3). It also requires certain cygwin development packages to be present (e.g. xslt-devel, openssl-devel, etc.)
but process is quite trivial.

Configuration
=============
Crawler accepts three input files:
	- list of initial URL's to crawl
	- allowed domains (to control how far you want the crawler to go)
	- list of regex rules to exclude certain URL's from being crawled.

Sample config files are provided in project's root folder.

For scrapy and MarkLogic configuration there is a foodFetcher/settings.py file with default settings you shoud be good to start with.
Please refer to scrapy documentation for scrapy standard settings.

How to run
==========
Check crawler.sh file with sample command line arguments. if you want to run it in a completely automated fashion or trigger from crontab entry do:
nohup ./crawler.sh &

Additional tools
================
There are few unix and windows script files in database directory to manually create the MarkLogic database and wipe it out if necessary.
Creating the database manually is not required as the foodFetcher automatically creates it if it does not already exist.
ml_test.py file is for the demonstration purposes of using MarkLogic API to ingest a local file.
For bulk ingestion of crawler results there are ml_ingest unix and windows scripts relying on MarkLogic mlcp tool (was tested on mlcp version 8.0-5).

Support
=======
This is my hobby garage project, so no techsupport, sorry!

Disclaimer
==========
With great tools comes the great responsibility. To make sure your intenet-wide experiments done is respectful manner please consider reading this well-written post:
https://learn.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/

settings.py file already contains settings to respect robots.txt and run at reduced thread count.
foodFetcher is provided for educational and demo purposes and author bears no responsibilty if the source code has been modified for harmful actions.
