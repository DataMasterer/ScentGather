def connectodb(hostname,schema,username,password,dbtype):
	if dbtype=='sqlite':
		import sqlite3
		conn=sqlite3.connect(schema+'.db')
		return conn
	else:
		return None

def saveinfotodb(dbconnect,fileinfos):
	if dbconnect is sqlite3.Connection:
		c=dbconnect.cursor()
		c.execute("PRAGMA foreign_keys=1")
		c.executescript('''
		CREATE TABLE IF NOT EXISTS exif
		(
			exifID INTEGER PRIMARY KEY,
			exifname text UNIQUE NOT NULL
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
			md5sum text
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
		for f in fileinfos:
			c.execute('''
			INSERT INTO files
			VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
			''',f[:-1])
			if c.lastrowid:
				fid=c.lastrowid
				for k,v in list(f[-1]):
					c.execute('''
					INSERT OR IGNORE INTO exif 
					VALUES (?,?)
					''',(None,k))
					c.execute('''
					INSERT OR IGNORE INTO files_exif 
					VALUES (?,(select exifID from exif where exifname=?),?)
					''',(fid,k,v))
			else:
				dbconnect.rollback()
				dbconnect.close()
				return False
		dbconnect.commit()
		dbconnect.close()
		return True
