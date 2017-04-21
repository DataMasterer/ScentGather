import hashlib
import sys
import os
from logging import log

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
        log('Scanning %s...' % dirName)
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
	log('traversedir started')
	filelist=[]
	# traverse root directory, and list directories as dirs and files as files
	for root, dirs, files in os.walk(parentFolder):
		path = root.split(os.sep)
		# Get the path to the file
		pathlen=len(path) - 1
		print(pathlen * '---', os.path.basename(root))
		log(pathlen * '---', os.path.basename(root))
		if len(path)<=depth: 
			for file in files:
				pathname = os.path.join(root, file)
				filelist.append({pathname:file})
		if len(path)-1==depth: dirs[:]=[];
	return filelist
