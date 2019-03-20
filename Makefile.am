

SUBDIRS = phrase-extraction rule-generalisation giza-pp/mkcls-v2 giza-pp/GIZA++-v2
DIST_SUBDIRS = phrase-extraction rule-generalisation

pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = ruLearn-$(GENERIC_RELEASE).pc

bin_SCRIPTS= ruLearn

ruLearn: ruLearn.in
	bash -c "APERTIUMPREFIX=`echo '$(APERTIUM_LIBS)' | tr ' ' '\n' | grep -- '-L' | sed 's:^-L::' | sed -r 's:lib/?$$::'`; cat $< | sed 's:__LIBDIR__:@libdir@:g' | sed 's:__PYTHON__:$(PYTHON):g' | sed 's:__PYTHONLIBDIR__:@libdir@/python:g' | sed \"s:__APERTIUMPREFIX__:\$$APERTIUMPREFIX:g\" | sed 's!__BASH__!$(BASH)!g;'  > $@"
