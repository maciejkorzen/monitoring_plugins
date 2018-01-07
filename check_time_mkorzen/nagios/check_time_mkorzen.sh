#!/bin/bash

##### DESCRIPTION ###########################################################
# Wrapper for check_time_mkorzen to run it with custom (server specific)
# version of Python 3.
#
##### USAGE #################################################################
# Run this script.
#
##### LICENSE ###############################################################
# Copyright 2017 Maciej Korzen
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
##### AUTHOR ################################################################
# Maciej Korzen
# maciek@korzen.org, mkorzen@gmail.com
# http://www.korzen.org/

path1="NONE"
for j in python3 python3.4 python3.5 python3.6; do
	if which "${j}" >/dev/null 2>&1; then
		path1="${j}"
	fi
done
if [ "${path1}" = "NONE" ]; then
	# Modify following line according to your environment.
	for i in /usr/local/pyenv1/shims/python3 /usr/local/pyenv2/shims/python3; do
		if [ -e "$i" ]; then
			path1="${i}"
		fi
	done
fi
if [ "${path1}" = "NONE" ]; then
	echo "Can't find Python 3 binary!"
	exit 2
fi
exec "${path1}" "$(dirname $0)/check_time_mkorzen"
