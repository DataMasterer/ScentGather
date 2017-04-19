import datetime
import time
import os.path
import shutil

def log(msg,errmsg=None,dump=None,listelem=None,elemparent=None,pathname=None,depth=None):
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
	#if os.path.exists('logfile.log'):
		#shutil.copy('logfile.log','logfile.log.'+datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S'))
	with open('logfile.log','a') as f:
		f.write('\t'.join(map(str,logstring))+'\n')
