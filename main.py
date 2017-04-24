#!/usr/bin/python
import argparse
import datamaster_connecttodb
import datamaster_getfilemeta
import datamaster_logging

parser = argparse.ArgumentParser(description='Collect File(s) Metadata')
parser.add_argument('-d',default=0,help='depth [0]',type=int)
parser.add_argument('-l',default=0,help='array in memory limit [0]',type=int)
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

dbconnect=datamaster_connecttodb.connectodb(H,s,u,p,t)
if dbconnect is None:
	datamaster_logging.log('Failed to connect, logging only')

files=datamaster_getfilemeta.traversedir(pathname,d)
sysid=datamaster_connecttodb.getsysid(dbconnect)

fileinfos=[]
for f in files:
	datamaster_logging.log('Testing file:'+f['pathname'])
	if datamaster_connecttodb.checkfileexistsindb(dbconnect,f):
		datamaster_logging.log('Skipping file ['+f['pathname']+'], file exists in db')
		continue
	fileinfos.append(datamaster_getfilemeta.getallfinfo(f,sysid))
	if len(fileinfos)>=l and l!=0 and dbconnect is not None:
		try:
			success=datamaster_connecttodb.saveinfotodb(dbconnect,fileinfos)
			if success is True:
				fileinfos=[]
			else:
				datamaster_logging.log('Failed to saveinfotodb',success,fileinfos,f,files,pathname,d)
				fileinfos=[]
		except:
				datamaster_logging.log('Failed to saveinfotodb',Error,fileinfos,f,files,pathname,d)
				fileinfos=[]
	datamaster_logging.log('Info',True,fileinfos,f,files,pathname,d)
