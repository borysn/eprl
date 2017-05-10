# util.py
# author: borysn
# license: MIT
import os, sys
from eprl.colors import bcolors

# errorAndExit
# display error msg and exit
#
# @param msg    msg to be displayed
def errorAndExit(msg, sysflag=True):
    excInfo = sys.exc_info()
    if excInfo[0] != None and sysflag:
        print(sys.exc_info())
    print('{}: {}'.format(status.ERROR, msg))
    sys.exit(2)

# confirm
# have user confirm given a confirm msg
#
# @param itemNum    item to be deleted
# @param db         portage mtimedb data store
# @param data       what is being confirmed?
# @return           true if user confirmed (said y), false if user did not confirm (said n)
def userConfirmed(data):
    # TODO data
    # init return
    confirmed = False
    msg = '{}: {}'.format(status.WARN, 'are you sure? (y/n) ')
    while True:
        answer = input(msg)
        answer = answer.upper()
        if answer == 'Y':
            confirmed = True
            break;
        elif answer == 'N':
            break;
    return confirmed

# userDoesNotHaveRootPrivileges
# check if user does not have root privileges
#
# @return    true if user does not have root privileges, false otherwise
def userDoesNotHaveRootPrivileges(): return True if os.getuid() != 0 else False

# getEprlVersion
# get the current version of eprl
def getEprlVersion():
    return '0.7'

# status
# status log msg prefixes (with colors)
class status:
    ERROR   = '{}ERROR{}'.format(bcolors.ERROR, bcolors.ENDC)
    WARN    = '{}WARNING{}'.format(bcolors.WARN, bcolors.ENDC)
    INFO    = '{}INFO{}'.format(bcolors.OKBLUE, bcolors.ENDC)
    SUCCESS = '{}SUCCESS{}'.format(bcolors.OKGREEN, bcolors.ENDC)
