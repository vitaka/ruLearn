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

origline=sys.stdin.readline()
while origline:
	numRule=int(origline.strip())
	origline=sys.stdin.readline()
	target=origline.strip().decode('utf-8')[7:]
	origline=sys.stdin.readline()
	source=origline.strip().decode('utf-8')[7:]
	print str(numRule)+" | "+source.encode('utf-8')+" | "+target.encode('utf-8')
	origline=sys.stdin.readline()
