#! /bin/bash

CURDIR=`dirname $0`

APERTIUMLIBS="$1"


APERTIUMPATH=`echo "$APERTIUMLIBS" | tr ' ' '\n' | grep -- '-L' | cut -f 1 | sed 's:^-L::' | sed -r 's:lib/?$::' | sed 's:$:/bin:' `
SEP="/"
if [ "$APERTIUMPATH" == ""  ]; then
	SEP=""
fi


$APERTIUMPATH${SEP}apertium-preprocess-transfer $CURDIR/test.rules.xml $CURDIR/test.rules.bin >/dev/null
$APERTIUMPATH${SEP}lt-comp lr $CURDIR/apertium-es-ca.es-ca.dix $CURDIR/apertium-es-ca.es-ca.bin >/dev/null

echo '^el<det><def><f><sg>$ ^casa<n><f><sg>$ ^azul<adj><mf><sg>$ ^.<sent>$' | $APERTIUMPATH${SEP}apertium-transfer $CURDIR/test.rules.xml $CURDIR/test.rules.bin $CURDIR/apertium-es-ca.es-ca.bin > $CURDIR/output
#$APERTIUMPATH/apertium-transfer $CURDIR/test.rules.xml $CURDIR/test.rules.bin $CURDIR/apertium-es-ca.es-ca.bin < $CURDIR/input2  > $CURDIR/output2


DIFF=`diff $CURDIR/output $CURDIR/reference`
#DIFF2=`diff $CURDIR/output2 $CURDIR/reference2`
DIFF2=""

if [ "$DIFF" == "" -a "$DIFF2" == "" ]; then
  echo "True"
else
  echo "False "
  echo "$DIFF"
  echo "$DIFF2"
fi


