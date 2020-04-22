# -*- coding: windows-1251 -*-
from threading import Thread
from threading import Lock
import subprocess,time
import MySQLdb
import csv
from datetime import datetime
import os

script_path = os.path.dirname(os.path.realpath(__file__))

con = MySQLdb.connect(host="localhost", user="root", passwd="", db="hack")
cur = con.cursor()
con.autocommit(True)
cur.execute('SET NAMES `utf8`')

cur.execute("SELECT id, domain, inj_url, source FROM sites WHERE is_inj = 'Y' AND is_import_to_bitrix = 'N'")
result = cur.fetchall()	

arr = []
first_line = ['ID', 'Название сделки', 'Стадия сделки', 'Язык', 'Сайт']
arr.append(first_line)
sql_update = []

for row in result:
	arr.append([row[0], 'Сделка №' + str(row[0]), 'Новая, проверить уязвимость', row[3], row[2]])
	sql_update.append(str(row[0]))

if len(arr) != 1:
	flname = datetime.today().strftime('%Y-%m-%d %H-%M-%S')
	with open(script_path + '\\' + flname + '.csv', 'wb') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)
		for row in arr:
			filewriter.writerow(row)

sql_update_str = ', '.join(sql_update)
if sql_update_str:
	cur.execute("UPDATE sites SET is_import_to_bitrix = 'Y' WHERE id IN (" + sql_update_str + ")")

print "Exported:" + str(len(arr) - 1)

#c:\\Python27\\python z:\\python\\hack\\export.py