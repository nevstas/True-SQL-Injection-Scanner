# -*- coding: windows-1251 -*-
import base64
import hashlib
import re
from threading import Thread
from threading import Lock
import subprocess,time
from random import randint
from random import randrange
import os
import urllib
import urllib2

import socket
import MySQLdb

import core_hack

url = "cvlt.ru"

fgc = core_hack.file_get_content(url)
links = core_hack.get_links(fgc['html'])
links_f = core_hack.format_links(url, fgc['final_url'], links)
links_inj = core_hack.inj_links(links_f);
for lnk in links_inj:
	fgc = core_hack.file_get_content(lnk)
	if core_hack.check_is_inj(fgc['html']):
		print lnk

#c:\\Python27\\python z:\\python\\hack\\check_site.py