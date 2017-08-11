#!/usr/bin/python

# Author: Lu Ji

import os
import sys
import re

def getword(sentence): 
  "This function produces the first word of the given sentence"
  words = sentence.split()
  if (len(words)>0):
    word = words[0]
  else: 
    return None
  if (word[-1] == '\n'):
    word = word[:-1]
  if (word[0] == '$'): # if this is a variable to be expanded 
    word = os.getenv(words[1])
    if (word == None):
      os.error("getenv")
      word = "UNDEFINED"
  return word

def getargs(input):
  "This function produces command arguments from the input"
  args = []
  if input == '':
    print "Couldn't read from standard input. End of file? Exiting ..."
    sys.exit(1)
  arg = getword(input)
  
  while ( arg != None):
    if (arg == '#'):
      break
    args = args + [arg]
    input = input[len(arg)+1:]
    arg = getword(input)
  return args

def execute(argc, args):
  "This function runs the command"
  pid = os.fork()
  if (pid == -1):
    os.error("fork")
    print '  (failed to execute command)'
  elif pid == 0: # we are in child
    if (-1 == os.execvp(args[0], args)):
      os.error('execvp')
      print "   (couldn't find command)"
    sys.exit(1)
  else: # we are in parent
    os.waitpid(pid, 0) # wait until child process finishes

def shell():
  shellArgs = sys.argv
  argc = len(sys.argv)
  input = None
  if (argc >= 2):
    mystdin = file(shellArgs[1])
  else: 
    mystdin = sys.stdin
  while(1):
    print '(myshell) '
    input = mystdin.readline()[:-1]
    args = getargs(input)
    argc = len(args)
    if (argc > 0 and args[0] == 'exit'):
      sys.exit(0)
    elif (argc > 0 and args[0] == 'logout'):
      os.exit(0)
    else:
      execute(argc, args)
  return 0

shell()
