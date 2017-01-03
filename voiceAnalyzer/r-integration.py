#!/usr/bin/env python

import subprocess

command = 'RScript'
pathToScript = './rScripts/getTweetSentiment.R'

# Variable number of args in a list
args = ['cullimoreorless']

# Build subprocess command
cmd = [command, pathToScript] + args

# check_output will run the command and store to result
x = subprocess.check_output(cmd, universal_newlines=True)

print('The maximum of the numbers is:', x)