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

parser = argparse.ArgumentParser(description='Spreads bilingual phrases according to their box.')
parser.add_argument('--discard_length_1',action='store_true')
args = parser.parse_args(sys.argv[1:])

numWordsTranslatedByRules=0
numWordsTranslatedByRulesLength1=0
numWordsTranslaredWordforWordInsideRules=0
numWordsTranslaredWordforWordOutsideRules=0

for line in sys.stdin:
	parts=line.split()
	numWords=int(parts[0])
	if len(parts)==2:
			numWordsTranslaredWordforWordOutsideRules+=numWords
	elif '|' in line:
		if args.discard_length_1 and parts[0]==parts[1]:
			numWordsTranslatedByRulesLength1+=numWords
		else:
			numWordsTranslatedByRules+=numWords
	else:
		numWordsTranslaredWordforWordInsideRules+=numWords

totalWords=numWordsTranslatedByRules+numWordsTranslaredWordforWordInsideRules+numWordsTranslaredWordforWordOutsideRules+numWordsTranslatedByRulesLength1

print "Num. words translated by rules: "+str(numWordsTranslatedByRules)+" ("+str( numWordsTranslatedByRules*100.0/ totalWords)+"%)"
print "Num. words translated by rules with length 1: "+str(numWordsTranslatedByRulesLength1)+" ("+str( numWordsTranslatedByRulesLength1*100.0/ totalWords)+"%)"
print "Num. words translated word-for-word inside rules: "+str(numWordsTranslaredWordforWordInsideRules)+" ("+str( numWordsTranslaredWordforWordInsideRules*100.0/ totalWords)+"%)"
print "Num. words translated word-for-word outside rules: "+str(numWordsTranslaredWordforWordOutsideRules)+" ("+str( numWordsTranslaredWordforWordOutsideRules*100.0/ totalWords)+"%)"
