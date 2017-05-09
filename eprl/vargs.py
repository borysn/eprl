# vargs.py
# author: borysn
# license: MIT
import argparse
import util, resolver
from util import status
try:
    import portage
except:
    pass

# cantRemoveItem
# validate if an item cant be removed from the resume point
#
# @param itemNum    portage resume item number for removal
# @return           True if item cant be removed, False otherwise
def cantRemoveItem(itemNum, db):
    # get current resume list
    resumeList = db.getResumeList();
    # check if itemNum is in range
    if resumeList != None and itemNum in range(len(resumeList)):
        return False
    return True

# noOptionsSpecified
# validate if no options were specified
#
# @param  args    command line arguments
# @return         true if no options were specified, false otherwise
def noOptionsSpecified(args): True if args.list == False and args.itemNums == None and args.items == None else False

# invalidItemNums
# check for invalid item numbers
#
# @param args    command line arguments
# @return        true if any of the specified item nums are invalid, false otherwise
def invalidItemNums(args, db):
    # init return
    itemNumsAreInvalid = False
    # check if itemNums were specified
    if (args.itemNums != None):
        # iterate item numbers
        for itemNum in args.itemNums:
            # check if itemNum is available for removal
            if cantRemoveItem(itemNum, db):
                # error
                print('{}: invalid item number "{}", cannot remove'.format(status.ERROR, itemNum))
                # itemNum not available for removal, arg not valid
                itemNumsAreInvalid = True
                break
    return itemNumsAreInvalid

# invalidItems
# check for invalid items
#
# TODO remove duplicates
#
# @param args    command line arguments
# @return        true if any items specified are invalid, false otherwise
def invalidItems(args):
    # init return
    itemsAreInvalid = False
    # check if items were given
    if args.items != None:
        # iterate items
        for item in args.items:
            # init porttree dbapi
            dbapi = portage.dbapi.porttree.portdbapi()
            # try to find matches
            try:
                # find any matches for a given item
                matches = dbapi.match(item)
                # no matches
                if len(matches) == 0:
                    # error
                    print('{}: invalid dependency "{}", cannot add to resume list'.format(status.ERROR, item))
                    # cannot match this item, arg not valid
                    itemsAreInvalid = True
                    break
            except portage.exception.AmbiguousPackageName as err:
                # package name too ambiguous, resolve by user
                # get packages
                pstr = err.__str__()
                # convert to list
                packages = pstr.translate(dict.fromkeys(map(ord, u"[],\'"))).split(' ')
                # have user resolve dependency discrepency
                index = resolver.userResolveItem(item, packages)
                # attempt to match resolved package
                # it can be masked, so a match would result in an empty list
                matches = dbapi.match(packages[index])
                if len(matches) == 0:
                    util.errorAndExit('looks like the "{}" package is masked'.format(packages[index]), False)
                # save result in args
                args.items[args.items.index(item)] = packages[index]
            except:
                util.errorAndExit('something went wrong when attempting to validate your listed dependencies')
    # return result
    return itemsAreInvalid

# parseArgs
# parse command line options and arguments
def parseArgs():
    # get argument parser
    parser = argparse.ArgumentParser()
    # list portage resume items
    parser.add_argument('-l', '--list', action='store_true', help='list portage resume items')
    # remove portage resume item(s)
    parser.add_argument('-r', '--remove', action='store', dest='itemNums', type=int, nargs="+", help='remove portage resume item(s)') 
    # add portage resume item(s)
    parser.add_argument('-a', '--add', action='store', dest='items', type=str, nargs='+', help='add resume item(s) to a resume list')
    # which list to remove from
    parser.add_argument('-b', '--backup', action='store_true', help='perform operations on backup list')
    # version
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.2')

    # parse arguments and return
    return parser.parse_args()

# argsAreNotValid
# validate commandline options and arguments
#
# note: argparse will handle most of the args error checking
#
# @param args    script arguments
# @return        True if args are valid, False otherwise
def argsAreNotValid(args, db):
    # validate args
    if noOptionsSpecified(args) or invalidItemNums(args, db) or invalidItems(args):
        # some args could not be valifated
        return True
    # everythings ok!
    return False
