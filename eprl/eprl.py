#!/bin/env python3
# eprl.py
# author: borysn | oxenfree
# license: MIT
#
# edit portage resume list
#
# usage: eprl.py [-h] [-l] [-r ITEMNUMS [ITEMNUMS ...]] [-a ITEMS [ITEMS ...]] [-b] [-v]
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -l, --list            list portage resume items
#   -r ITEMNUMS [ITEMNUMS ...], --remove ITEMNUMS [ITEMNUMS ...]
#                         remove portage resume items
#   -a ITEMS [ITEMS ...], --add ITEMS [ITEMS ...]
#                         add resume item(s) to a resume list
#   -b, --backup          perform operations on backup list
#   -v, --version         show program's version number and exit
import sys
import util, vargs, dbstore, resolver
from colors import tcolor, bcolors
from util import status

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
        # print resume items
        printResumeList(db.getResumeList(), db.getTarget())
        # listing portage resume items was successful
        print('\n{}: fetch portage resume/resume_backup lists'.format(status.SUCCESS))

# removePortageResumeItem
# remove a portage resume item
#
# @param itemNum    valid portage resume item to be removed
def removePortageResumeItems(itemNums, db):
    # confirm delete
    # TODO resolve itemNums for proper input
    if util.userConfirmed(itemNums):
        # attempt to remove resume item
        db.removeItems(itemNums)
        print('{}: item "{}" removed from portage resume list'.format(status.SUCCESS, tcolor.CTXT(tcolor.PURPLE, itemNums)))

# addPortageResumeItems
# add item(s) to a portage resume list
#
# @param  items    list of possible item entries, just portage package names
# @param  db       portage mtimedb data store
def addPortageResumeItems(items, db):
    db.addItems(items)
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
    db = dbstore.DBstore(args.backup)
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
