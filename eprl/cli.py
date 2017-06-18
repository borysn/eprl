#!/bin/env python3
#
# eprl.py
# author: borysn | oxenfree
# license: MIT
#
# edit portage resume list
#     $ eprl -h
import sys
from eprl import eprl, resolver, util, dbstore, vargs
# catch portage python module import error
# probably a result of not running as root
# continue script and attempt to error out
# at root privilege check
try:
    import portage
except ImportError:
    print('hmm, can\'t find portage python module, that\'s not good...')

# runScript
# run script as a function of args
#
# @param args       args should be validated before passed in
def runScript(args, db):
    # list all portage emerge items
    if args.list == True:
        eprl.listPortageResumeItems(db)
    # clear resume list
    elif args.clear == True:
        eprl.clearPortageResumeList(db)
    # export resume list
    elif args.export == True:
        eprl.exportPortageResumeList(db)
    # import resume list
    elif args.importing == True:
        eprl.importPortageResumeList(db)
    # remove portage resume item(s)
    elif args.itemNums != None:
        eprl.removePortageResumeItems(args.itemNums, db)
    # add portage resume item(s)
    elif args.items != None:
        # resolve dependencies
        resolvedItems = resolver.resolveItems(args.items)
        # add to portage resume list
        eprl.addPortageResumeItems(resolvedItems, db)

# main
# root privilege check, parse & validate args, get mtimedb store, run script
def main():
    # check for correct privileges
    if util.userDoesNotHaveRootPrivileges():
        util.errorAndExit('eprl.py requires root privileges, try running with sudo')
    # get args
    parser = vargs.getArgParser()
    # check that we have options
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    # parse args
    args = parser.parse_args()
    # init db store for portage mtimedb
    try:
        db = dbstore.DBstore(args.backup)
    except:
        util.errorAndExit('could not init dbstore')
    # validate args, exit if invalid
    if vargs.argsAreNotValid(args, db):
        data = tcolor.CTXT(tcolor.BLUE, '-h')
        util.errorAndExit('what to do, what to do...try {}'.format(data))
    # execute script
    runScript(args, db)
    # exit success
    sys.exit(0)

# exec main
if __name__ == '__main__':
    main()
