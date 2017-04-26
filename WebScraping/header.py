from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import re
import apiData
import pymysql
import json
import math
from datetime import date
import urllib.parse


tDate = date.today()

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='iprospect', db='scraping',charset='utf8')
cur = conn.cursor()