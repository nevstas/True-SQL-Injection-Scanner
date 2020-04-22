from threading import Thread
from threading import Lock
import subprocess,time
import MySQLdb
import os

script_path = os.path.dirname(os.path.realpath(__file__))

sql_source = 'ru'
fl_name = script_path + '\\ru_domains.txt'

f=open(fl_name, 'r')
i = 0
done = False
def read_file_line_by_line():
	global f
	while True:
		line = f.readline()
		if not line:
			break
		yield line

def domain_import():
	global i
	global con
	global cur
	global done
	a=read_file_line_by_line()
	for b in a:
		try:
			sp = b.split(';')
			dm = sp[0].lower()

			cur.execute(
				'''SELECT 1 AS isset
				FROM sites		
				WHERE domain = %s		
				''', [dm])
			data = cur.fetchone()

			if not data:	
				cur.execute("INSERT INTO sites (`domain`, 'source') VALUES (%s, %s)", [dm])
		except:			
			pass
		i += 1
	done = True
	print "done"

def showstat():
	global i
	global done
	while True:
		if not done:
			print "position:" + str(i)
			time.sleep(1)

con = MySQLdb.connect(host="localhost", user="root", passwd="", db="hack")
cur = con.cursor()
con.autocommit(True)
cur.execute('SET NAMES `utf8`')

worker1 = Thread(target=showstat)
worker1.setDaemon(True)
worker1.start()

worker2 = Thread(target=domain_import)
worker2.setDaemon(True)
worker2.start()

#time.sleep(9999999) #!!!!!!!!!!!!!!!!!!!
worker1.join()
worker2.join()

#c:\\Python27\\python z:\\python\\hack\\import.py