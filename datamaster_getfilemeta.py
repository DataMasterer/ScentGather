import hashlib
import sys
import os
import platform
import datetime
import time
import datamaster_logging
from file_metadata.generic_file import GenericFile

def getsysinfo():
	sysinfo=[str(platform.architecture()),platform.machine(),
	platform.node(),platform.platform(),platform.processor(),
	platform.system()]
	return sysinfo
	
def hashfile(path, blocksize = 65536):
#src: http://pythoncentral.io/finding-duplicate-files-with-python/
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def findDup(parentFolder):
#src: http://pythoncentral.io/finding-duplicate-files-with-python/
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        datamaster_logging.log('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups

def traversedir(parentFolder,depth):
	datamaster_logging.log('traversedir started')
	filelist=[]
	# traverse root directory, and list directories as dirs and files as files
	for root, dirs, files in os.walk(parentFolder):
		path = root.split(os.sep)
		# Get the path to the file
		pathlen=len(path) - 1
		print(pathlen * '---', os.path.basename(root))
		datamaster_logging.log(pathlen * '---', os.path.basename(root))
		if len(path)-1==depth and depth!=0: dirs[:]=[];
		else: 
			for file in files:
				pathname = os.path.join(root, file)
				filelist.append({'pathname':pathname,'filename':file})
	return filelist

def getallfinfo(targetfile,sysid):
	pathname=targetfile['pathname']
	filename=targetfile['filename']
	fileext=''.join(os.path.splitext(pathname)[1:])
	filehash=hashfile(pathname)
	datamaster_logging.log('getallfinfo started')

	gf=GenericFile.create(pathname)
	analysis={}
	prefix='analyze_'
	suffix=''
	methods = sorted(dir(gf))
	for method in methods:
		if method.startswith(prefix) and method.endswith(suffix):
			try:
				analysis.update(getattr(gf, method)())
			except:
				pass

	fstat=os.stat(pathname)
	ts=time.time()
	insts=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	fileinfo=[filename,pathname,fstat.st_ino,sysid,
	fstat.st_mtime,fstat.st_atime,fstat.st_ctime,None,insts,
	fstat.st_size,None,fileext,filehash,analysis]
	datamaster_logging.log(pathname,dump=fileinfo)
	datamaster_logging.log('getallfinfo done')
	return fileinfo
