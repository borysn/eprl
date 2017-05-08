# colors.py
# author: borysn
# license: MIT

# ANSI color codes
# thank you, lliam-mcinroy
# https://stackoverflow.com/a/22886382/2276284
class bcolors:
    HEADER  = '\033[95m'
    OKBLUE  = '\033[94m'
    OKGREEN = '\033[92m'
    WARN    = '\033[93m'
    ERROR   = '\033[91m'
    ENDC    = '\033[0m'

# tcolor
# colorify some text
class tcolor:
    PURPLE  = bcolors.HEADER
    BLUE    = bcolors.OKBLUE
    GREEN   = bcolors.OKGREEN
    YELLOW  = bcolors.WARN
    RED     = bcolors.ERROR
    CTXT    = lambda c, m: '{}{}{}'.format(c, m, bcolors.ENDC)
