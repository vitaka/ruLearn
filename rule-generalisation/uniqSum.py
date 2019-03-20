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

import sys,argparse

parser = argparse.ArgumentParser(description='Sums frequencies')
parser.add_argument('--freq_at_the_beginning',action='store_true')
parser.add_argument('--max',action='store_true')
args = parser.parse_args(sys.argv[1:])

prevContent=u""
prevSum=0

for line in sys.stdin:
	line=line.decode('utf-8').strip()
	parts=line.split(u" | ")
	if args.freq_at_the_beginning:
		freq=int(parts[0])
		content=u" | ".join(parts[1:])
	else:
		freq=int(parts[-1])
		content=u" | ".join(parts[:-1])
	if content == prevContent:
		if args.max:
			if freq > prevSum:
				prevSum=freq
		else:
			prevSum+=freq
	else:
		if prevContent!=u"":
			print str(prevSum).zfill(8)+" | "+prevContent.encode('utf-8')
		prevContent=content
		prevSum=freq

if prevContent!=u"":
			print str(prevSum).zfill(8)+" | "+prevContent.encode('utf-8')
