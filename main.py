#!/usr/bin/python
import argparse
import sys
import scentgather_connecttodb
import scentgather_getfilemeta
import scentgather_logging

parser = argparse.ArgumentParser(description='Collect File(s) Metadata')
parser.add_argument('-d',default=0,help='depth [0] (0 for infinite)',type=int)
parser.add_argument('-l',default=100,help='array in memory limit [100] (0 for infinite)',type=int) #for large directories, 0 will make huge logfiles and arrays
parser.add_argument('-H',default='localhost',help='db hostname [localhost]')
parser.add_argument('-s',default='scentgather',help='db schema [scentgather]')
parser.add_argument('-u',default='root',help='db username [root]')
parser.add_argument('-p',default='',help='db password []')
parser.add_argument('-t',default='sqlite',choices=['mysql','sqlite','json','xml','oracle','sqlserver','mariadb'],help='db type [sqlite]')
parser.add_argument('--verbose', action='store_true', help='print log messages to stdout')
parser.add_argument('--quick', action='store_true', help='skips files according to their pathname only (not accurate, use carefully)')
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

dbconnect=scentgather_connecttodb.connectodb(H,s,u,p,t)
if dbconnect is None:
	scentgather_logging.log('Failed to connect, logging only')

files=scentgather_getfilemeta.traversedir(pathname,d)
sysid=scentgather_connecttodb.getsysid(dbconnect)

fileinfos=[]
for f in files:
	scentgather_logging.log('Testing file:'+f['pathname'])
	if scentgather_connecttodb.checkfileexistsindb(dbconnect,f):
		scentgather_logging.log('Skipping file ['+f['pathname']+'], file exists in db')
		continue
	fileinfos.append(scentgather_getfilemeta.getallfinfo(f,sysid))
	if len(fileinfos)>=l and l!=0 and dbconnect is not None:
		try:
			success=scentgather_connecttodb.saveinfotodb(dbconnect,fileinfos)
			if success is True:
				fileinfos=[]
			else:
				scentgather_logging.log('Failed to saveinfotodb',success,fileinfos,f,files,pathname,d)
				fileinfos=[]
		except:
				scentgather_logging.log('Failed to saveinfotodb', sys.exc_info()[0],fileinfos,f,files,pathname,d)
				fileinfos=[]
	scentgather_logging.log('Info',True,fileinfos,f,files,pathname,d)
