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

import sys, ruleLearningLib, argparse

if __name__=="__main__":
	DEBUG=False

	parser = argparse.ArgumentParser(description='Chooses alignment templates.')
	parser.add_argument('--alignment_template',required=True)
	parser.add_argument('--tag_groups_file_name',required=True)
	parser.add_argument('--emptyrestrictionsmatcheverything',action='store_true')
	parser.add_argument('--tt1_beam',action='store_true')
	args = parser.parse_args(sys.argv[1:])

	ruleLearningLib.AT_LexicalTagsProcessor.initialize(args.tag_groups_file_name,None)

	#parse AT
	myAT=ruleLearningLib.AlignmentTemplate()
	myAT.parse(args.alignment_template.decode('utf-8'))
	if DEBUG:
		print >> sys.stderr, "AT: "+ myAT.to_string()

	for line in sys.stdin:
		line=line.strip().decode('utf-8')
		bilphrase=ruleLearningLib.AlignmentTemplate()
		if not args.tt1_beam:
			bilphrase.parse(u'|'.join(line.split(u'|')[1:]))
		else:
			bilphrase.parse(u'|'.join(line.split(u'|')[1:]),True)
		if not args.tt1_beam:
			bilphrase.add_explicit_restrictions()
		if DEBUG:
			print >> sys.stderr, "Checking: "+bilphrase.to_string()
		if not args.tt1_beam:
			#IMPORTANT NOTE: Since we are processing only the bilphrases correctly reproduced, and we are processing ATs
			#from more specific to most general, matching = reproducing
			#NOT SURE ABOUT THIS!!
			if myAT.is_subset_of_this(bilphrase,True,args.emptyrestrictionsmatcheverything):
				print line.encode('utf-8')
		else:
			if myAT.matches_segment(bilphrase.parsed_sl_lexforms,bilphrase.parsed_restrictions, False,True,bilphrase.parsed_restrictions_tt1):
				result=myAT.apply(bilphrase.parsed_sl_lexforms,bilphrase.tl_lemmas_from_dictionary,bilphrase.parsed_restrictions)
				if result == bilphrase.parsed_tl_lexforms:
					print line.encode('utf-8')
