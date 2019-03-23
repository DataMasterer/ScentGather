# ScentGather
Previously, DataMaster, A system for mastering data and file preprocessing

The first part will be a python script to traverse directories and collect file(s) metadata into a db (currently sqlite)

## Motivation: 
- I try to organize my files into folders, with timestamp-names, with proper extensions, etc.
- However!! If I want a different view of all my files I still need a bunch of programs to analyze, reorganize/sort and endanger my precious files
- How about a solution that non-intrusively collects all possible metadata about your chosen files, locally, on your system to protect your privacy and your files?
- How about a solution that allows you or any third-party (if you wish) to control the metadata, enhance it and if you wish, apply it in ways you cannot imagine!

- Finally, imagine, the possibilities once you have the metadata on all your files, reorganizing would be the simplest thing...chronologically, according to tags you add (or added by third-party analysis), according to people you tag (not the same as the previous tags), even according to who is taking the pictures, or the locations taken, or any kind of content that exists....and that's just speaking of images...

## Features:
- Traverse Directories and gather files to a certain depth
- Gather file(s) metadata
- Log progress
- Save metadata to db

## Dependencies:
- Native Libraries: os, sys, time, datetime, sqlite3, hashlib, platform, argparse, shutil
- External Libraries: [file_metadata](https://pypi.python.org/pypi/file-metadata)

## Usage:
```
./main.py -h
usage: main.py [-h] [-d D] [-l L] [-H H] [-s S] [-u U] [-p P]
               [-t {mysql,sqlite,json,xml,oracle,sqlserver,mariadb}]
               pathname

Collect File(s) Metadata

positional arguments:
  pathname              pathname to recursively follow

optional arguments:
  -h, --help            show this help message and exit
  -d D                  depth [0]
  -l L                  array in memory limit [0]
  -H H                  db hostname [localhost]
  -s S                  db schema [datamaster]
  -u U                  db username [root]
  -p P                  db password []
  -t {mysql,sqlite,json,xml,oracle,sqlserver,mariadb}
                        db type [sqlite]
```

## Dependencies:
  file-metadata python library: to install: pip install file-metadata
