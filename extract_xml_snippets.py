#!/usr/bin/env python

import argparse
import json
import os
import shutil

from pathlib import Path

def process_source(content, snipfolder, fpath, fnum, ext):
	if not ext:
		return()
	fname = os.path.basename(fpath)
	outname = snipfolder + "/" + fname.replace(".", "_") + "_snip" + str(fnum) + ext
	outfile = open(outname, "wt")
	outfile.write(content)
	outfile.close
	
def process_file(filename, snipfolder):
	code = False
	filenum = 1
	source = ""
	ext = ""
	f = open(filename, "rt")
	for line in f:
		if code:
			source = source + line.replace("&#xD;", "").replace("<body>", "").replace("</body>","")
		if line.find("<language>") >= 0:
			if line.find("C++") >= 0:
				ext = ".cpp"
			code = True
		if line.find("</body>") >= 0:
			process_source(source, snipfolder, filename, filenum, ext)
			filenum = filenum + 1
			code = False
	f.close()
	print("  - {} code segments extracted".format(filenum -1))
	

parser = argparse.ArgumentParser(description='Extract source embedded within specified XML format files into .snippet_scan folder (or -o folder) ready for snippet analysis using Detect script.', prog='extract_xml_snippets.py')
parser.add_argument("-s", "--sourcepath", type=str, default='.', help='Path to scan', required=True)
parser.add_argument("-e", "--extension", type=str, help='File extension(s) to scan for (multiple extensions can be specified)', action='append', nargs=1)
parser.add_argument("-d", "--deletesnippetfolder", action='store_true', help='Delete .snippet_scan folder if it exists')
parser.add_argument("-o", "--outputfolder", type=str, default='.snippet_scan', help='Specify output folder (default .snippet_scan)')

args = parser.parse_args()

snipfolder = args.sourcepath + '/' + args.outputfolder
if os.path.isdir(snipfolder):
	if args.deletesnippetfolder:
		shutil.rmtree(snipfolder)
		#os.rmdir(snipfolder)
		os.mkdir(snipfolder)
	else:
		print("{} folder exists already - use --deletesnippetfolder option to delete".format(snipfolder))
		exit()
else:
	os.mkdir(snipfolder)

for ext in args.extension:
    if (ext[0][0] != '.'):
        myext = '.' + ext[0]
    else:
    	myext = ext[0]
		
    for filename in Path(args.sourcepath).rglob("*" + myext):
        print("Processing file: {}".format(filename))
        process_file(filename, snipfolder)
