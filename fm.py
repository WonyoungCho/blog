## Title : Find Me
## Find some fname1's words in fname2


#! /usr/bin/env python3

import subprocess
import sys

fname1=sys.argv[1]
column=sys.argv[2]
fname2=sys.argv[3]

cmd='awk \'{print $'+column+'}\' '+fname1+'|while read line;do grep $line '+fname2+';done|column -ts $\'\\t\''
subprocess.run(cmd,shell=True)
