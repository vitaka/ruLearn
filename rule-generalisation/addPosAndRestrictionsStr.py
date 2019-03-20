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


import sys,re,argparse, ruleLearningLib
from ruleLearningLib import AT_ParsingError

parser = argparse.ArgumentParser(description='')
parser.add_argument('--tag_groups_file_name',required=True)
parser.add_argument('--tag_sequences_file_name',required=True)
parser.add_argument('--rich_ats',action='store_true')
parser.add_argument('--only_lexical',action='store_true')
parser.add_argument('--for_tt1_beam',action='store_true')
parser.add_argument('--print_box_index_from_dict')
args = parser.parse_args(sys.argv[1:])

include_restrictions= not args.rich_ats and not args.for_tt1_beam

if not args.for_tt1_beam:
	ruleLearningLib.AT_LexicalTagsProcessor.initialize(args.tag_groups_file_name,args.tag_sequences_file_name)

boxesInvDict=dict()
if args.print_box_index_from_dict:
	for l in open(args.print_box_index_from_dict):
		l=l.rstrip('\n').decode('utf-8')
		parts=l.split('\t')
		boxesInvDict[parts[1]]=parts[0]

for line in sys.stdin:
	line=line.rstrip('\n').decode('utf-8')

	pieces=line.split(u' | ')
	freqstr=pieces[0]
	atstr=u'|'.join(pieces[1:5])

	at = ruleLearningLib.AlignmentTemplate()

	try:
		at.parse(atstr)
		if not args.for_tt1_beam:
			at.add_explicit_empty_tags()
		if not args.print_box_index_from_dict:
			if args.only_lexical:
				print at.get_tags_str().encode('utf-8')+" | "+line.encode('utf-8')
			else:
				print at.get_pos_list_str(include_restrictions).encode('utf-8')+" | "+line.encode('utf-8')
		else:
			key= at.get_tags_str() if args.only_lexical else at.get_pos_list_str(include_restrictions)
			print boxesInvDict[key]

	except AT_ParsingError as detail:
		print >> sys.stderr, "Error parsing AT from line: "+line.encode('utf-8')
		print >> sys.stderr, "Detail: "+str(detail)
		exit(1)
