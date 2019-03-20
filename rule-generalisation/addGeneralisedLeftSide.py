#!/usr/bin/python
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


import sys,ruleLearningLib,argparse

parser = argparse.ArgumentParser(description='Sums frequencies')
parser.add_argument('--freq_at_the_beginning',action='store_true')
args = parser.parse_args(sys.argv[1:])


for line in sys.stdin:
	genlist=list()
	line=line.strip().decode('utf-8')
	parts=line.split(u" | ")
	if len(parts) > 1:
		freq=parts[0]
		wordssec=parts[1]
		words=wordssec.split()
		for word in words:
			wordclean=word.strip()
			tags=ruleLearningLib.remove_lemmas_one(wordclean)
			taglist=ruleLearningLib.parse_tags(tags)
			genlist.append(u"<"+taglist[0]+u">")
			genStr=u" ".join(genlist)
			partsoutput=list()
			if args.freq_at_the_beginning:
				partsoutput.extend(parts)
				partsoutput.append(genStr)
			else:
				partsoutput.append(genStr)
				partsoutput.extend(parts[1:])
				partsoutput.append(freq)
		print u" | ".join(partsoutput).encode('utf-8')
