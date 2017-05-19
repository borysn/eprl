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
from eprl.restore import RestorePRL
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
        # store item names
        items = []
        # attempt to remove resume item
        try:
            items = db.removeItems(itemNums)
        except:
            util.errorAndExit('could not remove items from resume list')
        # print success
        data = tcolor.CTXT(tcolor.PURPLE, items)
        print('{}: item(s) removed from portage resume list\n{}'.format(status.SUCCESS, data))

# addPortageResumeItems
# add item(s) to a portage resume list
#
# @param  items    list of possible item entries, just portage package names
# @param  db       portage mtimedb data store
def addPortageResumeItems(items, db):
    # get user confirmation
    if util.userConfirmed(db):
        try:
            db.addItems(items)
        except:
            util.errorAndExit('could not add items to resume list')
        # print success
        data = tcolor.CTXT(tcolor.PURPLE, items)
        print('{}: item(s) added to portage resume list\n{}'.format(status.SUCCESS, data))

# clearPortageResumeList
# remove all items from portage resume list
#
# @param args    command line arguments
def clearPortageResumeList(db):
    # get user confirmation
    if util.userConfirmed(db):
        try:
            db.clearList()
        except:
            util.errorAndExit('could not clear portage resume list')
        # print success
        print('{}: successfully cleared portage resume list'.format(status.SUCCESS))

# exportPortageResumeList
# export a portage resume list
#
# @param db    portage mtimedb
def exportPortageResumeList(db):
    try:
        # get data from dbstore
        data = db.getTargetResumeListData()
        # export data
        RestorePRL().exportData(data)
    except:
        util.errorAndExit('could not export portage resume list')
    # print success
    print('{}: {}'.format(status.SUCCESS, 'successfully exported portage resume list'))

# importPortageResumeList
# import a portage resume list
#
# @param db    portage mtimedb
def importPortageResumeList(db):
    # get user confirmation
    if util.userConfirmed(db):
        try:
            # get data
            data = RestorePRL().importData()
            # store data
            db.setTargetResumeList(data)
        except:
            util.errorAndExit('could not import portage resume list')
        # print success
        print('{}: {}'.format(status.SUCCESS, 'successfully imported portage resume list'))

# runScript
# run script as a function of args
#
# @param args       args should be validated before passed in
def runScript(args, db):
    # list all portage emerge items
    if args.list == True:
        listPortageResumeItems(db)
    # clear resume list
    elif args.clear == True:
        clearPortageResumeList(db)
    # export resume list
    elif args.export == True:
        exportPortageResumeList(db)
    # import resume list
    elif args.importing == True:
        importPortageResumeList(db)
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
        data = tcolor.CTXT(tcolor.BLUE, '-h')
        util.errorAndExit('what to do, what to do...try {}'.format(data))
    # execute script
    runScript(args, db)
    # exit success
    sys.exit(0)

# exec main
if __name__ == '__main__':
    main()
