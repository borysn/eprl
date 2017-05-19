# resolve.py
# author: borysn
# license: MIT
from eprl import util
from eprl.util import status
try:
    import portage
except:
    pass

# userResolveItem
# attempt to resolve a single item through user input
#
# @param item       item the user initially entered
# @param matches    matches returned for given item
# @return           string containing a single match resolved through user input
def userResolveItem(item, matches):
    print('{} dependency \'{}\' has multiple matches'.format(status.WARN, item))
    return util.askUserWhichItem(matches)

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
    dbapi = portage.dbapi.porttree.portdbapi()
    # iterate items finding matches and resolving
    for item in items:
        # find matches
        matches = dbapi.match(item)
        # no matches
        if len(matches) == 0:
            # if args were validated correctly,
            # there should never be a 0 match here
            util.errorAndExit('check dependency names, something\'s wrong')
        elif len(matches) == 1:
            # store match
            resolvedItems.append(matches[0])
        elif len(matches) > 1:
            # user resolve matches and store
            resolvedItems.append(matches[userResolveItem(item, matches)])
    # return result
    return resolvedItems
