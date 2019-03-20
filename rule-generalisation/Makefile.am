bin_SCRIPTS= ruLearn-generateATs ruLearn-minimiseATs ruLearn-beamSearch ruLearn-selectRulesMaximiseScore ruLearn-generateApertiumFormat  ruLearn-removeRedundantRules ruLearn-evaluateRules

rulegen_SOURCES=ruLearn-generateATs.in ruLearn-minimiseATs.in ruLearn-beamSearch.in ruLearn-selectRulesMaximiseScore.in ruLearn-generateApertiumFormat.in ruLearn-removeRedundantRules.in ruLearn-evaluateRules.in

rulearnlibdir=$(libdir)
rulearnlib_DATA= shflags createModeForBeamSearchEvaluation.sh createModeWithLearnedRules.sh translate_apertium.sh mteval-v11b-nosgm.sh calculateStatsForPairedBootstrapResampling.sh createModeNoRules.sh empty-rules-for-translating.t1x mteval-v13-nosgm-segments.sh mteval-v11b.pl mteval-v13.pl tercom.7.25.jar evaluateBeamSearchHypothesis.sh generateLog-v11.pl

rulearnsharedir=$(datadir)/ruLearn
rulearnshare_DATA=sample-config.ca-es.cfg sample-config.es-ca.cfg sample-config.br-fr.cfg sample-config.en-es.cfg sample-config.es-en.cfg newstest2010head40.en newstest2010head40.es

pythonlibdir=$(libdir)/python
pythonlib_DATA= \
               beamSearchLib.py ruleLearningLib.py tsort.py addPosAndRestrictionsStr.py spreadBilphrases.py generateMultipleATsFromBilphrases.py chooseATs.py filterAlignmentTemplates.py addStandardBoxDescToOnlyLexical.py beamSearch.py computeSupersetsOfKeySegments.py maximiseScore.py  addGeneralisedLeftSide.py uniqSum.py removeExplicitEmptuTagsFromPatternTLandRest.py addDebugInfoToTransferRules.py filterBilphrasesMatchingAT.py removeDebugInfoFromTransfer.py addWordInforToReport.py summarizeReport.py addDebugInfoToTransferRules-debug.py collapseSourcetarget.py extractPhrases.py seq.py generatePostTransferXML.py

ruLearn-%: ruLearn-%.in
	sed "s!__LIBDIR__!@libdir@!g"< $< | sed "s!__PYTHON__!$(PYTHON)!g" | sed "s!__PYTHONLIBDIR__!@libdir@/python!g" | sed "s!__DATADIR__!@datadir@/ruLearn!g" | sed "s!__BASH__!$(BASH)!g;" | sed "s!__JAVA__!$(JAVA)!g;" > $@
