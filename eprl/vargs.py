# vargs.py
# author: borysn
# license: MIT
import argparse
from eprl import util, resolver
from eprl.util import status
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
def noOptionsSpecified(args):
    return args.backup    == False and \
           args.clear     == False and \
           args.export    == False and \
           args.importing == False and \
           args.itemNums  == None  and \
           args.items     == None  and \
           args.list      == False

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

# resolveAmbiguousItem
# resolve ambigous item
#
# @param args    script arguments
# @param pstr    packages string from AmbiguousPackageName exception
# @param item    item in question
def resolveAmbiguousItem(args, pstr, item, dbapi):
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
    return packages[index]

# isInvalidItem
# check if the package name can be matched
#
# @param item    item name the user entered
# @return        true if package can be matched, false otherwise
def isInvalidItem(item):
    # get porttree dbapi
    dbapi = portage.dbapi.porttree.portdbapi()
    # check for matches
    if dbapi.match(item) == []:
        # error
        print('{}: invalid dependency "{}", cannot add to resume list'.format(status.ERROR, item))
        # cannot match this item
        return True
    # item was succesfully matched
    return False


# invalidItems
# check for invalid items
#
# @param args    command line arguments
# @return        true if any items specified are invalid, false otherwise
def invalidItems(args):
    # get porttree dbapi
    dbapi = portage.dbapi.porttree.portdbapi()
    # init return
    itemsAreInvalid = False
    # store ambiguous packages for user resolution
    ambiguousPackages = []
    # check if items were given
    if args.items != None:
        # iterate items
        for item in args.items:
            try:
                # check if item is valid
                if isInvalidItem(item):
                    # set result and break
                    itemsAreInvalid = True
                    break
            except portage.exception.AmbiguousPackageName as err:
                # get packages
                pstr = err.__str__()
                # store resolution info
                ambiguousPackages.append({'item':item, 'pstr':pstr})
            except:
                util.errorAndExit('failed to validate your listed dependencies')
    # check for any ambiguous packages
    if not itemsAreInvalid and not ambiguousPackages == []:
        # iterate packages
        for p in ambiguousPackages:
            # get item index
            index = args.items.index(p['item'])
            # have user resolve ambiguous package
            args.items[index] = resolveAmbiguousItem(args, p['pstr'], p['item'], dbapi)
    # return result
    return itemsAreInvalid

# getArgParser
# get parser for command line options and arguments
def getArgParser():
    # get argument parser
    parser = argparse.ArgumentParser()
    # list portage resume items
    parser.add_argument('-l', '--list', action='store_true', help='list portage resume items')
    # clear portage resume list
    parser.add_argument('-c', '--clear', action='store_true', help='clear portage resume list')
    # remove portage resume item(s)
    parser.add_argument('-r', '--remove', action='store', dest='itemNums', type=int, nargs="+", help='remove portage resume item(s)') 
    # add portage resume item(s)
    parser.add_argument('-a', '--add', action='store', dest='items', type=str, nargs='+', help='add resume item(s) to a resume list')
    # export portage resume list
    parser.add_argument('-e', '--export', action='store_true', help='export portage resume list')
    # import portage resume list
    parser.add_argument('-i', '--import', action='store_true', help='import portage resume list', dest='importing')
    # backup flag to target backup resume list
    parser.add_argument('-b', '--backup', action='store_true', help='perform operations on backup resume list')
    # version
    parser.add_argument('-v', '--version', action='version', version='eprl version {}'.format(util.getEprlVersion()))

    # parse arguments and return
    return parser

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
