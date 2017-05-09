# resolve.py
# author: borysn
# license: MIT
import portage
import util

# printMatches
# print matches to console
#
# @param matches    matches to be printed
def printMatches(matches):
    for i in range(len(matches)):
        print('{}: {}'.format(i, matches[i]))

# askUserWhichMatch
# ask user which match they'd like to use
#
# @param matches    m
# @return           index of user choice
def askUserWhichMatch(matches):
    # init return
    index = -1
    msg = '{}: {}'.format(status.WARN, 'which item would you like to use? ')
    while True:
        # print matches
        printMatches(matches)
        # get user input
        index = input(msg)
        if index in range(len(matches)):
            break
    return index

# userResolveItem
# attempt to resolve a single item through user input
#
# @param item       item the user initially entered
# @param matches    matches returned for given item
# @return           string containing a single match resolved through user input
def userResolveItem(item, matches):
    print('{} dependency \'{}\' has multiple matches'.format(status.WARN, item))
    return askUserWhichMatch(matches)

# resolveItems
# resolve all items through user input
#
# @param items      list of items the user initially entered
# @param matches    possibly matches for given item
# @return           list containing user resolved matches
def resolveItems(items):
    # init return
    resolvedItems = []
    # get porttree dbapi object
    dbapi = portage.dbapi.porttree.dbapi()
    # iterate items finding matches and resolving
    for item in items:
        # find matches
        matches = dbapi.match(item)
        # no matches
        if len(matches) == 0:
            # if args were validateted correctly,
            # there should never be a 0 match here
            util.errorAndExit('check dependency names, something\'s wrong')
        elif len(matches) == 1:
            # store match
            resolvedItems.append(matches[0])
        elif len(matches) > 1:
            # user resolve matches and store
            resolvedItems.append(userResolveItem(item, matches))

    # return result
    return resolvedItems
