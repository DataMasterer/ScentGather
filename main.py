#!/usr/bin/python
import argparse
from connecttodb import *
from getfilemeta import *
from logging import *

parser = argparse.ArgumentParser(description='Collect File(s) Metadata')
parser.add_argument('-d',default=0,help='depth')
parser.add_argument('-l',default=0,help='array in memory limit')
parser.add_argument('-H',default='localhost',help='db hostname')
parser.add_argument('-s',default='datamaster',help='db schema')
parser.add_argument('-u',default='root',help='db username')
parser.add_argument('-p',default='',help='db password')
parser.add_argument('-t',default='sqlite',choices=['mysql','sqlite','json','xml','oracle','sqlserver','mariadb'],help='db type')
parser.add_argument('pathname',help='pathname to recursively follow')
parser.parse_args()

quit()

dbconnect=connecttodb(H,u,p,t)
if dbconnect is None:
	log('Failed to connect, logging only')

files=traversedir(pathname,d)

fileinfos=[]
for f in files:
	fileinfos.append(getallfinfo(f))
	if len(fileinfos)>=limit and limit!=0 and dbconnect is not None:
		success=saveinfotodb(dbconnect,fileinfos)
		if success:
			fileinfos=[]
		else:
			log('Failed to saveinfotodb',success,fileinfos,f,files,pathname,d)
			fileinfos=[]
	log('Info',true,fileinfos,f,files,pathname,d)
