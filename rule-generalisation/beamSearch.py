# -*- encoding: utf-8 -*-
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


#stdinput: sentences to be translated
from beamSearchLib import RuleList, ParallelSentence, RuleApplicationHypothesis
from ruleLearningLib import AlignmentTemplate
import ruleLearningLib
import argparse
import gzip
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='compute possible coverages of rules and associated 1-BLEU score')
    parser.add_argument('--alignment_templates',required=True)
    parser.add_argument('--alternative_alignment_templates')
    parser.add_argument('--tag_groups_file_name',required=True)
    parser.add_argument('--tag_sequences_file_name',required=True)
    parser.add_argument('--target_language',default='ca')
    parser.add_argument('--apertium_data_dir')
    parser.add_argument('--final_boxes_index')
    parser.add_argument('--beam_size',default='1000')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--minimum_covered_words', action='store_true')
    parser.add_argument('--allow_incompatible_rules', action='store_true')
    parser.add_argument('--rbpe', action='store_true')
    parser.add_argument('--tt1_beam', action='store_true')
    args = parser.parse_args(sys.argv[1:])

    if args.debug:
        DEBUG=True
        ruleLearningLib.DEBUG=True

    if args.rbpe:
        ruleLearningLib.RBPE=True

    ruleLearningLib.AT_LexicalTagsProcessor.initialize(args.tag_groups_file_name,args.tag_sequences_file_name)

    ruleList=RuleList()

    RuleApplicationHypothesis.set_target_language(args.target_language)
    RuleApplicationHypothesis.set_apertium_data_dir(args.apertium_data_dir)
    RuleApplicationHypothesis.set_minimum_covered_words(args.minimum_covered_words)

    #load alignment templates
    if args.alignment_templates.endswith(".gz"):
        gfile=gzip.open(args.alignment_templates)
    else:
        gfile=open(args.alignment_templates)
    for line in gfile:
        line=line.strip().decode('utf-8')
        at=AlignmentTemplate()
        at.parse(line)
        ruleList.add(at)
    gfile.close()
    ruleLists=[ruleList]

    if args.alternative_alignment_templates:
        altRuleList=RuleList()
        gfile=gzip.open(args.alternative_alignment_templates)
        for line in gfile:
            line=line.strip().decode('utf-8')
            at=AlignmentTemplate()
            at.parse(line)
            altRuleList.add(at)
        gfile.close()
        ruleLists=[ruleList,altRuleList]

    boxesCoverage=False
    boxesDic=dict()
    if args.final_boxes_index:
        for line in open(args.final_boxes_index):
            parts=line.split("\t")
            boxesDic[parts[1].strip()]=int(parts[0])
        boxesCoverage=True

    numLine=0
    for line in sys.stdin:
        numLine+=1
        line=line.rstrip('\n').decode('utf-8')
        parts=line.split('|')
        if len(parts) > 5 and not args.tt1_beam:
            #wrong sentence
            print ""
        else:
            parallelSentence=ParallelSentence()
            parallelSentence.parse(line, parseTlLemmasFromDic=True,forRBPE=args.rbpe)
            if not args.tt1_beam:
                parallelSentence.add_explicit_empty_tags()
            finalHypotheses=parallelSentence.compute_coverages_and_bleu(ruleLists,int(args.beam_size),boxesCoverage,boxesDic,args.allow_incompatible_rules,args.tt1_beam)
            print u"|||".join([unicode(h) for h in finalHypotheses]).encode('utf-8')
            print >> sys.stderr, "finished line "+str(numLine)
