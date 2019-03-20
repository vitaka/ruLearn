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

import sys

def descToStdDesc(d):
    bigparts=d.split("__")
    resultl=[]
    for bigpart in bigparts:
        lexcat=bigpart.split(">")[0][1:]
        resultl.append(lexcat)
    return "__".join(resultl)

for line in sys.stdin:
    line=line.rstrip("\n")
    parts=line.split("\t")
    if len(parts) == 2:
        num=parts[0]
        desc=parts[1]
        stddesc=descToStdDesc(desc)
        print "\t".join([num,desc,stddesc])
