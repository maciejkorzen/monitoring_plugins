#!/usr/bin/python2

##### DESCRIPTION ###########################################################
# Wrapper for check_time_mkorzen. To be used with Check_MK agent as local
# type of check.
# Invokes check_time_mkorzen and converts it's output to format compatible
# with Check_MK agent's local check.
#
##### USAGE #################################################################
# Place this script somewhere on server monitored by Check_MK.
# Don't forget to adjust path to check_time_mkorzen.sh.
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

import sys
import os
import argparse
import traceback
import string
from subprocess import Popen, PIPE

def main():
    """
    return values:
    0:  all got well
    1:  connection is slow
    2:  no connection at all (or really slow)
    3:  something really bad happend

    """
    parser = argparse.ArgumentParser(description = "check_time_mkorzen")
    parser.add_argument("-n",
        required = True,
        help = "check name",
        dest = "name",
        metavar = "<string>")
    args = parser.parse_args()

    try:
        checkresult = Popen(["timeout", "18", "/fix_me/path/a/b/c/check_time_mkorzen.sh"],
            stdout = PIPE, stderr = PIPE)
    except OSError:
        sys.stdout.write("3 %s - check binary program not found! (error 1)" % (args.name))
        sys.exit(3)
    except:
        sys.stdout.write("3 %s - UNKNOWN error " % (args.name))
        sys.stdout.write(''.join(traceback.format_exc()).replace('\n', ' '))
        sys.exit(3)

    exit_code = os.waitpid(checkresult.pid, 0)
    output = checkresult.communicate()
    if exit_code[1] == 0:
        output2 = output[0].split('\n')[0]
        outdata1 = output2.split('|')[0].strip()
        perfdata = output2.split('|')[1].strip().replace(' ', '|')
        sys.stdout.write("0 %s %s %s\n" % (args.name, perfdata, outdata1))
        sys.exit(0)

    sys.stdout.write("3 %s - UNKNOWN error " % (args.name))
    sys.stdout.write(''.join(output[0]).replace('\n', ' '))
    sys.exit(3)

if __name__ == '__main__':
    main()
