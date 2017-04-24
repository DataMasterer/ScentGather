import datamaster_getfilemeta
import datamaster_logging
import sys

def connectodb(hostname='localhost',schema='datamaster',username='root',password='',dbtype='sqlite'):
	if dbtype=='sqlite':
		import sqlite3
		conn=sqlite3.connect(schema+'.db')
		c=conn.cursor()
		c.execute("PRAGMA foreign_keys=1")
		c.executescript('''
		CREATE TABLE IF NOT EXISTS exif
		(
			exifID INTEGER PRIMARY KEY,
			exifname text UNIQUE NOT NULL
		);

		CREATE TABLE IF NOT EXISTS platforms
		(
			systemID INTEGER PRIMARY KEY,
			architecture text,
			machine text,
			node text,
			platform text,
			processor text,
			system text
		);

		CREATE TABLE IF NOT EXISTS files
		(
			fileID INTEGER PRIMARY KEY,
			filename text NOT NULL,
			pathname text UNIQUE NOT NULL,
			inode INT,
			systemID INT,
			lastmodDate text,
			lastaccessDate text,
			apparentcreationDate text,
			discovereddeletionDate text,
			insertiondate text DEFAULT CURRENT_TIMESTAMP,
			sizeInBytes INT,
			detectedformatID INT,
			ext INT,
			md5sum text,
			FOREIGN KEY (systemID) REFERENCES platforms(systemID)
		);

		CREATE TABLE IF NOT EXISTS files_exif
		(
			fileID INTEGER NOT NULL,
			exifID INTEGER NOT NULL,
			value text,
			PRIMARY KEY (exifID,fileID),
			FOREIGN KEY (fileID) REFERENCES files(fileID),
			FOREIGN KEY (exifID) REFERENCES exif(exifID)
		);
		''');
		return conn
	else:
		return None

def savesysinfotodb(dbconnect,sysinfo):
	import sqlite3
	if type(dbconnect) is sqlite3.Connection:
		c=dbconnect.cursor()
		res=c.execute('''
		SELECT systemID FROM platforms
		WHERE platform=?
		''',[sysinfo[3]])
		sysid=res.fetchall()
		if sysid is None or type(sysid) is not int and len(sysid)==0:
			c.execute('''
			INSERT INTO platforms
			(architecture,machine,node,platform,
			processor,system)
			VALUES (?,?,?,?,?,?)
			''',sysinfo)
			sysid=c.lastrowid
			dbconnect.commit()
		if type(sysid) is not int and len(sysid)==0:
			return False
		elif type(sysid) is not int:
			sysid=sysid[0][0]
	else:
		return False
	return sysid

def getsysid(dbconnect):
	return savesysinfotodb(dbconnect,datamaster_getfilemeta.getsysinfo())

def saveinfotodb(dbconnect,fileinfos):
	import sqlite3
	if type(dbconnect) is sqlite3.Connection:
		c=dbconnect.cursor()
		for f in fileinfos:
			f[0]=buffer(f[0])
			f[1]=buffer(f[1])
			c.execute('''
			INSERT OR IGNORE INTO files
			(filename,pathname,inode,systemID,
			lastmodDate,lastaccessDate,apparentcreationDate,
			discovereddeletionDate,insertiondate,sizeInBytes,
			detectedformatID,ext,md5sum)
			VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
			''',f[:-1])
			if type(c.lastrowid) is int:
				fid=c.lastrowid
				for k,v in list(f[-1].items()):
					c.execute('''
					INSERT OR IGNORE INTO exif 
					(exifName)
					VALUES (?)
					''',[str(k)])
					c.execute('''
					INSERT OR IGNORE INTO files_exif 
					(fileID,exifID,value)
					VALUES (?,(select exifID from exif where exifname=?),?)
					''',[fid,str(k),str(v)])
			else:
				dbconnect.rollback()
				return False
		dbconnect.commit()
		return True
	else:
		return False

def checkfileexistsindb(dbconnect,fileinfo):
	import sqlite3
	if type(dbconnect) is sqlite3.Connection:
		c=dbconnect.cursor()
		pathname=fileinfo['pathname']
		checksum=datamaster_getfilemeta.hashfile(pathname)
		res=c.execute('''
			SELECT 1 FROM files
			WHERE pathname=? and md5sum=?''', [buffer(pathname),checksum])
		fileexists=res.fetchall()
		if fileexists:
			return True
		return False
	else:
		return False

