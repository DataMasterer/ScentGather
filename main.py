#!/usr/bin/python
import argparse
from connecttodb import *
from getfilemeta import *
from logging import *

parser = argparse.ArgumentParser(description='Collect File(s) Metadata')
parser.add_argument('-d',default=0,help='depth [0]')
parser.add_argument('-l',default=0,help='array in memory limit [0]')
parser.add_argument('-H',default='localhost',help='db hostname [localhost]')
parser.add_argument('-s',default='datamaster',help='db schema [datamaster]')
parser.add_argument('-u',default='root',help='db username [root]')
parser.add_argument('-p',default='',help='db password []')
parser.add_argument('-t',default='sqlite',choices=['mysql','sqlite','json','xml','oracle','sqlserver','mariadb'],help='db type [sqlite]')
parser.add_argument('pathname',help='pathname to recursively follow')
args=parser.parse_args()
d=args.d
l=args.l
H=args.H
s=args.s
u=args.u
p=args.p
t=args.t
pathname=args.pathname

dbconnect=connectodb(H,s,u,p,t)
if dbconnect is None:
	log('Failed to connect, logging only')

files=traversedir(pathname,d)

fileinfos=[]
for f in files:
	fileinfos.append(getallfinfo(f['filename']))
	if False and len(fileinfos)>=limit and limit!=0 and dbconnect is not None:
		success=saveinfotodb(dbconnect,fileinfos)
		if success:
			fileinfos=[]
		else:
			log('Failed to saveinfotodb',success,fileinfos,f,files,pathname,d)
			fileinfos=[]
	log('Info',True,fileinfos,f,files,pathname,d)
