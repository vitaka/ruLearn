# coding=utf-8
# -*- encoding: utf-8 -*-
#
# Copyright 2009-2016 Víctor M. Sánchez-Cartagena, Felipe Sánchez-Martínez, Universitat d'Alacant
#
# This file is part of ruLearn.
# ruLearn is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ruLearn is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ruLearn.  If not, see <http://www.gnu.org/licenses/>.
#

import sys,argparse,gzip

parser = argparse.ArgumentParser(description='Spreads bilingual phrases according to their box.')
parser.add_argument('--dir')
parser.add_argument('--dict')
parser.add_argument('--tt1_beam',action='store_true')
parser.add_argument('--input_not_sorted',action='store_true')
args = parser.parse_args(sys.argv[1:])

dir=args.dir

pack=u""
index=0

idsDict=dict()
idsDictInverse=dict()
b_createDict=True
b_writeBilphrases=False

if args.dict and args.dir:
	b_createDict=False
	b_writeBilphrases=True
	#parse dict
	for line in open(args.dict):
		line=line.strip()
		parts=line.split()
		if len(parts) == 2:
			idsDict[int(parts[0])]=parts[1]
			idsDictInverse[parts[1]]=int(parts[0])
elif args.dict or args.dir:
	print >> sys.stderr, "ERROR: wrong parameters"

fileDesc=None

writtenBoxes=set()

for line in sys.stdin:
	line=line.rstrip('\n').decode('utf-8')
	parts=line.split(u"|")
	packStr=parts[0]
	bilphrase=u"|".join(parts[1:])

	if packStr != pack:

		#close prev file
		if pack != u"":
			if fileDesc != None:
				if args.tt1_beam and not args.input_not_sorted:
					fileDesc.write("END_BILINGUAL_PHRASES\n")
				fileDesc.close()

		index+=1
		pack=packStr

		if b_createDict:
			idsDict[index]=pack

		#create a new file
		if b_writeBilphrases:
			if args.input_not_sorted:
				fileDesc=open(dir+"/newbilphrases/"+(str(idsDictInverse[pack]))+".bilphrases","a")
			else:
				fileDesc=gzip.open(dir+"/newbilphrases/"+str(index)+".bilphrases.gz","wb")
			if args.tt1_beam and not args.input_not_sorted:
				fileDesc.write("BILINGUAL_PHRASES\n")
			writtenBoxes.add(index)
	if b_writeBilphrases:
		fileDesc.write(bilphrase.encode('utf-8')+"\n")

if fileDesc != None:
	if args.tt1_beam and not args.input_not_sorted:
		fileDesc.write("END_BILINGUAL_PHRASES\n")
	fileDesc.close()

if b_writeBilphrases:
	nonWrittenBoxes=set(idsDict.keys())-writtenBoxes
	for nwbox in nonWrittenBoxes:
		if args.input_not_sorted:
			fileDesc=open(dir+"/newbilphrases/"+str(nwbox)+".bilphrases","a")
		else:
			fileDesc=gzip.open(dir+"/newbilphrases/"+str(nwbox)+".bilphrases.gz","wb")
		if args.tt1_beam and not args.input_not_sorted:
				fileDesc.write("BILINGUAL_PHRASES\n")
				fileDesc.write("END_BILINGUAL_PHRASES\n")
		fileDesc.close()

#print index
if b_createDict:
	for boxid  in idsDict.keys():
		print str(boxid)+"\t"+idsDict[boxid].encode('utf-8')
