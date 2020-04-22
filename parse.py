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

num_threads = 50

myLock = Lock() #mysql
myLock2 = Lock() #schetchiki
i = 0

con = MySQLdb.connect(host="localhost", user="root", passwd="", db="hack")
cur = con.cursor()
con.autocommit(True)
cur.execute('SET NAMES `utf8`')

cur.execute("UPDATE sites SET is_parse = 'N' WHERE is_parse = 'P'")

def pars():
	global con
	global cur
	global myLock
	global i

	while True:
		myLock.acquire()
		try:	
			cur.execute("SELECT id, domain FROM sites WHERE is_parse = 'N' LIMIT 1")
		except:			
			pass	
		result = cur.fetchone()	
		if result:	
			try:
				cur.execute("UPDATE sites SET is_parse = 'P' WHERE id = %s", [result[0]])
			except:			
				pass
		myLock.release()
		if result:					
			#try:
		
			url = result[1]
			is_inj = 'N'
			inj_url = None

			fgc = core_hack.file_get_content(url)
			links = core_hack.get_links(fgc['html'])
			links_f = core_hack.format_links(url, fgc['final_url'], links)
			links_inj = core_hack.inj_links(links_f);
			for lnk in links_inj:
				fgc = core_hack.file_get_content(lnk)
				if core_hack.check_is_inj(fgc['html']):
					is_inj = 'Y'
					inj_url = lnk
					break

		
			#except:			
			#	pass	
			myLock.acquire()
			try:
				cur.execute("UPDATE sites SET is_parse = 'Y', is_inj = %s, inj_url = %s WHERE id = %s", [is_inj, inj_url, result[0]])
			except:			
				pass
			myLock.release()
			myLock2.acquire()
			i += 1
			myLock2.release()
		else:
			time.sleep(5)

def showstat():
	global i
	global done
	while True:
		print "position:" + str(i)
		time.sleep(1)

worker1 = Thread(target=showstat)
worker1.setDaemon(True)
worker1.start()

for i1 in range(num_threads):	
	worker = Thread(target=pars)
	worker.setDaemon(True)
	worker.start()
worker.join()
worker1.join()

#SELECT 
#(SELECT COUNT(*) FROM sites) AS count_all,
#(SELECT COUNT(*) FROM sites WHERE is_parse = 'Y') AS is_parse,
#(SELECT COUNT(*) FROM sites WHERE is_parse = 'N') AS is_not_parse,
#(SELECT COUNT(*) FROM sites WHERE is_inj = 'Y') AS is_inj,
#((SELECT COUNT(*) FROM sites WHERE is_parse = 'Y') / (SELECT COUNT(*) FROM sites WHERE is_inj = 'Y')) AS rate

#c:\\Python27\\python z:\\python\\hack\\parse.py