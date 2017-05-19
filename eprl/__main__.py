#!/bin/env python3
#
# eprl.py
# author: borysn | oxenfree
# license: MIT
#
# edit portage resume list
#     $ eprl -h
import sys
from eprl import util, vargs, dbstore, resolver
from eprl.colors import tcolor
from eprl.util import status
# catch portage python module import error
# probably a result of not running as root
# continue script and attempt to error out
# at root privilege check
try:
    import portage
except ImportError:
    print('hmm, can\'t find portage python module, that\'s not good...')

# printResumeItems
# output resume item list to console
#
# @params items    dictionary containing 'resume' & 'resume_backup' matrices
def printResumeList(resumeList, target):
    # print collection name
    print('[{} list]'.format(tcolor.CTXT(tcolor.PURPLE, target)))
    # check list size
    if resumeList == None or len(resumeList) <= 0:
        print('\t{}: list is empty'.format(status.WARN))
    else:
        for i in range(len(resumeList)):
            print('\t{}: {}'.format(tcolor.CTXT(tcolor.BLUE, i), resumeList[i][2]))

# listPortageResumeItems
# list all ebuilds scheduled in resume & resume_backup
#
# @param db    mtimedb data store
def listPortageResumeItems(db):
    try:
        # print resume items
        printResumeList(db.getResumeList(), db.getTarget())
    except:
        util.errorAndExit('could not list resume items')
    # print success
    print('\n{}: fetch portage resume/resume_backup lists'.format(status.SUCCESS))

# removePortageResumeItem
# remove a portage resume item
#
# @param itemNum    valid portage resume item to be removed
def removePortageResumeItems(itemNums, db):
    # confirm delete
    if util.userConfirmed(itemNums):
        # attempt to remove resume item
        try:
            db.removeItems(itemNums)
        except:
            util.errorAndExit('could not remove items from resume list')
        # print success
        print('{}: item "{}" removed from portage resume list'.format(status.SUCCESS, tcolor.CTXT(tcolor.PURPLE, itemNums)))

# addPortageResumeItems
# add item(s) to a portage resume list
#
# @param  items    list of possible item entries, just portage package names
# @param  db       portage mtimedb data store
def addPortageResumeItems(items, db):
    try:
        db.addItems(items)
    except:
        util.errorAndExit('could not add items to resume list')
    # print success
    print('{}: item(s)\n{}\nadded to portage resume list'.format(status.SUCCESS, tcolor.CTXT(tcolor.PURPLE, items)))

# runScript
# run script as a function of args
#
# @param args       args should be validated before passed in
def runScript(args, db):
    # list all portage emerge items
    if args.list == True:
        listPortageResumeItems(db)
    # remove portage resume item(s)
    elif args.itemNums != None:
        removePortageResumeItems(args.itemNums, db)
    # add portage resume item(s)
    elif args.items != None:
        # resolve dependencies
        resolvedItems = resolver.resolveItems(args.items)
        # add to portage resume list
        addPortageResumeItems(resolvedItems, db)

# main
# root privilege check, parse & validate args, get mtimedb store, run script
def main():
    # check for correct privileges
    if util.userDoesNotHaveRootPrivileges():
        util.errorAndExit('eprl.py requires root privileges, try running with sudo')
    # get args
    args = vargs.parseArgs()
    # init db store for portage mtimedb
    try:
        db = dbstore.DBstore(args.backup)
    except:
        util.errorAndExit('could not init dbstore')
    # validate args, exit if invalid
    if vargs.argsAreNotValid(args, db):
        util.errorAndExit('what to do, what to do...try {}'.format(tcolor.CTXT(tcolor.BLUE, '-h')))
    # execute script
    runScript(args, db)
    # exit succes
    sys.exit(0)

# exec main
if __name__ == '__main__':
    main()
