import numpy as np
from lxml import html
from lxml.etree import tostring
import bs4
import mechanize
import json
import urllib2
import MySQLdb as mdb
def rf_price(output_list):
       """get output_list from dataclean and train random forest