import datetime
import time
import os.path
import shutil

logfilename='logfile.log'

def log(msg,errmsg=None,dump=None,listelem=None,elemparent=None,pathname=None,depth=None):
	global logfilename
	ts=time.time()
	logstring=[]
	logstring=logstring+[datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')]
	logstring=logstring+[msg,';',errmsg]
	if elemparent is list and listelem in elemparent:
		logstring=logstring+[elemparent.index(listelem)/len(elemparent)]
	else:
		logstring=logstring+[None]
	logstring=logstring+[pathname,depth,dump]
	print logstring
	with open(logfilename,'a') as f:
		f.write('\t'.join(map(str,logstring))+'\n')

def archivelog():
	global logfilename
	ts=time.time()
	if os.path.exists(logfilename):
		shutil.copy(logfilename,logfilename+'.'+datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S'))
	with open(logfilename,'w') as f:
		f.write('')
