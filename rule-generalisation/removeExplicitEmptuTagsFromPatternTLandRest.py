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

import sys,re,argparse

parser = argparse.ArgumentParser(description='Bla bla.')
parser.add_argument('--short',action='store_true')
parser.add_argument('--emptyrestrictionsmatcheverything',action='store_true')
args = parser.parse_args(sys.argv[1:])

if args.short:
	requiredLength=5
	partsToSubstitute=[2,4]
else:
	requiredLength=6
	if args.emptyrestrictionsmatcheverything:
		partsToSubstitute=[0,3]
	else:
		partsToSubstitute=[0,3,5]
	#partsToSubstitute=[0,3,6]

for line in sys.stdin:
	line=line.strip().decode('utf-8')
	parts=line.split(u'|')
	if len(parts)==requiredLength:
		for partindex in partsToSubstitute:
			parts[partindex] = re.sub(r'<empty_tag_[^>]*>', '', parts[partindex])

	print u'|'.join(parts).encode('utf-8')
