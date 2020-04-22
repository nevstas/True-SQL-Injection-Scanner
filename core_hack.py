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


class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_302(self, req, fp, code, msg, headers):
		return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
	http_error_301 = http_error_303 = http_error_307 = http_error_302

def check_trim_http_url(url):
	url = url.strip()
	if not url.startswith("http://") and not url.startswith("https://"):
		url = "http://" + url
	return url

def file_get_content(url):
	try:	
		url = check_trim_http_url(url)
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0', 
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
				'Accept-Charset':'utf-8;q=0.7,*;q=0.7',
				'Accept-Encoding':'deflate'}
		cookieprocessor = urllib2.HTTPCookieProcessor()
		opener = urllib2.build_opener(MyHTTPRedirectHandler, cookieprocessor)
		urllib2.install_opener(opener)
		req=urllib2.Request(url, None, headers)
		response = urllib2.urlopen(req, timeout=10)
		final_url = response.geturl()
		str = response.read()			

		p = re.compile("^http[s]?:\/\/[^\/]+$")
		m = p.search(final_url)
		if m:
			final_url = final_url + '/'
		return {'final_url': final_url, 'html': str}
	except:			
		return {'final_url': url + '/', 'html': ''}
	

def get_links(html):
	p = re.compile('''<a\s+(?:[^>]*?\s+)?href=(["'])(.*?)(["'])''')
	d = re.findall(p, html)
	links = []
	for lnk in d:
		links.append(lnk[1])
	links = list(set(links)) #remove dupl
	return links

def format_links(url, final_url, links):
	format_l = []
	for lnk in links:
		if url in lnk:
			lnk = check_trim_http_url(lnk)
			format_l.append(lnk)
		elif 'http://' in lnk or 'https://' in lnk:
			pass
		else:
			if lnk.startswith("/"):
				p = re.compile("(.*?\..*?)\/")
				m = p.search(final_url)
				final_url_home = m.group(1)
				format_url = final_url_home + lnk
				format_url = check_trim_http_url(format_url)
				format_l.append(format_url)
			else:
				p = re.compile("(.*?\..*\/)")
				m = p.search(final_url)
				if m:
					final_url_path = m.group(1)
					format_url = final_url_path + lnk
				else:
					format_url = final_url + lnk
				format_l.append(format_url)
	return format_l

def inj_links(links):
	get_par_to_do = []
	links_inj = []
	for lnk in links:
		result1 = lnk.split("?")
		if len(result1) == 1:
			continue
		params = result1[1].split("&")
		for par in params:
			p = par.split("=");
			get_par_to_do.append(p[0])
	get_par_to_do = list(set(get_par_to_do)) #remove dupl
	for lnk in links:
		result1 = lnk.split("?")
		if len(result1) == 1:
			continue
		params = result1[1].split("&")
		for par in params:
			p = par.split("=");
			if len(p) == 1:
				continue
			if p[0] in get_par_to_do:
				lnk = lnk.replace(p[0] + '=' + p[1], p[0] + '=' + p[1] + "'")
				links_inj.append(lnk)
				get_par_to_do.remove(p[0])
				break
	
	return links_inj[:100]

def check_is_inj(html):
	result = False
	if 'You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near' in html:
		result = True
	try:	
		html = unicode(html, "utf-8")
		if 'You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near' in html:
			result = True
	except:		
		pass
	return result
