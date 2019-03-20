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

from beamSearchLib import RuleApplicationHypothesis,RuleList,ParallelSentence
from pulp.constants import LpStatusOptimal, LpStatus
import argparse
import ruleLearningLib
import sys,gzip,math
from ruleLearningLib import debug,AlignmentTemplate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='select rules which maximise 1-BLEU score')
    parser.add_argument('--tag_groups_file_name',required=True)
    parser.add_argument('--tag_sequences_file_name',required=True)
    parser.add_argument('--only_n_first')
    parser.add_argument('--only_hyps_with_maximum_local',action='store_true')
    parser.add_argument('--discard_sentences_all_maximum',action='store_true')
    parser.add_argument('--beam',action='store_true')
    parser.add_argument('--beam_size',default='10000')
    parser.add_argument('--super_heuristic',action='store_true')
    parser.add_argument('--select_boxes_minimum',action='store_true')
    parser.add_argument('--compute_key_segment_breaking_prob',action='store_true')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--final_boxes_index')
    parser.add_argument('--alignment_templates')
    parser.add_argument('--sentences')
    parser.add_argument('--supersegments_with_maximum_score')
    parser.add_argument('--input')
    parser.add_argument('--apertium_data_dir')
    parser.add_argument('--target_language',default='ca')
    parser.add_argument('--rbpe', action='store_true')
    parser.add_argument('--tt1_beam', action='store_true')
    parser.add_argument('--ternary_search', default='0')
    args = parser.parse_args(sys.argv[1:])

    if args.debug:
        DEBUG=True
        ruleLearningLib.DEBUG=True

    if args.rbpe:
        ruleLearningLib.RBPE=True

    ruleLearningLib.AT_LexicalTagsProcessor.initialize(args.tag_groups_file_name,args.tag_sequences_file_name)

    RuleApplicationHypothesis.set_apertium_data_dir(args.apertium_data_dir)
    RuleApplicationHypothesis.set_target_language(args.target_language)

    print >> sys.stderr, "Loading ATs ..."
    ruleList=RuleList()
    #load alignment templates
    if args.alignment_templates:
        if args.alignment_templates.lower().endswith(".gz"):
            gfile=gzip.open(args.alignment_templates)
        else:
            gfile=open(args.alignment_templates)
        for line in gfile:
            line=line.strip().decode('utf-8')
            at=AlignmentTemplate()
            at.parse(line)
            ruleList.add(at)
        gfile.close()
    print >> sys.stderr, "... done"

    print >> sys.stderr, "Loading sentences ..."
    #load sentences
    sentences=list()
    if args.sentences:
        if args.sentences.lower().endswith(".gz"):
            gfile=gzip.open(args.sentences)
        else:
            gfile=open(args.sentences)
        for line in gfile:
            line=line.strip().decode('utf-8')
            parallelSentence=ParallelSentence()
            parallelSentence.parse(line, parseTlLemmasFromDic=True,forRBPE=args.rbpe)
            parallelSentence.add_explicit_empty_tags()
            sentences.append(parallelSentence)
        gfile.close()
    print >> sys.stderr, "... done"

    boxesInvDic=dict()
    boxesDic=dict()
    if args.final_boxes_index:
        for line in open(args.final_boxes_index):
            parts=line.split("\t")
            boxesInvDic[int(parts[0])]=parts[1].strip()
            boxesDic[parts[1].strip()]=int(parts[0])


    nfirst=None
    if args.only_n_first:
        nfirst=int(args.only_n_first)
    if args.supersegments_with_maximum_score:
        nfirst=1

    ll_hypothesis=list()

    if args.input:
        inputfile=gzip.open(args.input)
    else:
        inputfile=sys.stdin

    print >> sys.stderr, "Loading scores ..."
    for line in inputfile:
        line=line.decode('utf-8').strip()
        parts=line.split(u"|||")
        if nfirst != None:
            parts=parts[:nfirst]
        ll_hypothesis.append([ RuleApplicationHypothesis.create_and_parse(part) for part in parts if len(part) > 0])
    if args.input:
        inputfile.close()
    print >> sys.stderr, "... done"

    print >> sys.stderr, "Maximising score of "+str(len(ll_hypothesis))+" sentences"

    if args.only_hyps_with_maximum_local or args.super_heuristic or args.select_boxes_minimum:

        #remove all non-maximum hypotheses
        for numSentence,l_hypothesis in enumerate(ll_hypothesis):
            firstNotMaximumIndex=len(l_hypothesis)
            if firstNotMaximumIndex > 0:
                maximumScore=l_hypothesis[0].get_score()
                for index in range(len(l_hypothesis)):
                    if l_hypothesis[index].get_score() < maximumScore:
                        firstNotMaximumIndex=index
                        break
                if firstNotMaximumIndex == len(l_hypothesis) and args.discard_sentences_all_maximum:
                    l_hypothesis[:]=[RuleApplicationHypothesis()]
                else:
                    l_hypothesis[:]=l_hypothesis[:firstNotMaximumIndex]
            debug("Sentence "+str(numSentence)+": "+str(firstNotMaximumIndex)+" hypothesses with maximum BLEU")


    if args.beam:
        appliedRules,valueOfSolution=RuleApplicationHypothesis.select_rules_maximize_score_with_beam_search(ll_hypothesis, beamSize=int(args.beam_size), isDiff=True)
        for ruleid in sorted(appliedRules):
            print str(ruleid)
        print >> sys.stderr, "Value: "+str(valueOfSolution)
    elif args.super_heuristic:
        appliedRules=RuleApplicationHypothesis.select_rules_maximize_score_with_super_heuristic(ll_hypothesis)
        for ruleid in sorted(appliedRules):
            print str(ruleid)
    elif args.select_boxes_minimum or args.compute_key_segment_breaking_prob:

        supersegmentsWithMaxScore=list()
        if args.supersegments_with_maximum_score:

            print >> sys.stderr, "Loading supersegments ..."
            #load supersegments
            gfile=gzip.open(args.supersegments_with_maximum_score)
            for line in gfile:
                line=line.strip().decode('utf-8')
                parts=line.split(u"|||")
                supersegmentsWithMaxScore.append([ RuleApplicationHypothesis.create_and_parse(part) for part in parts if len(part)>0])
            gfile.close()
            print >> sys.stderr, "... done"

        print >> sys.stderr, "Computing box scores ..."
        appliedRules=RuleApplicationHypothesis.select_rules_maximize_score_boxes_applied(ll_hypothesis,boxesInvDic,ruleList,sentences,supersegmentsWithMaxScore,args.compute_key_segment_breaking_prob,args.tt1_beam)
        print >> sys.stderr, "... done"

        if args.compute_key_segment_breaking_prob:
            print >> sys.stderr, "Reoptimizing ..."
            bestRulesReoptimized=ParallelSentence.optimize_boxes_applied_rescoring_bleu(sentences,ruleList,appliedRules,boxesInvDic,args.tt1_beam,int(args.ternary_search))
            print >> sys.stderr, "... done"
            for ruleid in sorted(bestRulesReoptimized):
                print str(ruleid)
        else:
            for ruleid in sorted(appliedRules):
                print str(ruleid)
    else:
        status,solution,valueOfSolution=RuleApplicationHypothesis.select_rules_maximize_score(ll_hypothesis)
        if status == LpStatusOptimal:
            #print ids of rules
            appliedRules=set()
            for hyp in solution:
                appliedRules.update(hyp.get_applied_rules())
            appliedRulesSorted=sorted(appliedRules)
            for ruleid in appliedRulesSorted:
                print str(ruleid)
            print >> sys.stderr, "Value: "+str(valueOfSolution)
        else:
            print >> sys.stderr, "Wrong Status: "+str(LpStatus[status])
