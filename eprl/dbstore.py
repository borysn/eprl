# dbstore.py
# author: borysn
# license: MIT
from eprl import dbutil
from eprl.util import status
from eprl.colors import tcolor
try:
    import portage
    from portage.util.mtimedb import MtimeDB
    from portage.package.ebuild.config import config as portconfig
except:
    pass

# dbstore
# portage mtimedb data store
class DBstore:

    # constructor
    # create dbstore object for portage mtime db access
    #
    # @param  backup    flag indicating if 'resume_backup' list should be used instead of 'resume'
    def __init__(self, backup=False):
        # set target based upon backup flag value
        self.target = 'resume_backup' if backup else 'resume'
        # store portage mtimedb object
        self.db = MtimeDB(portage.mtimedbfile)
        # check if target exists in object
        if not self.target in self.db.keys():
            # create empty target
            self.db[self.target] = self.createEmptyTarget()

    # addEmptyTarget
    # add an empty target to the portage mtimedb loaded in memory
    def createEmptyTarget(self):
        # get default emerge opts using portage config object
        edo = portconfig().get('EMERGE_DEFAULT_OPTS').split(' ')
        # create empty target
        return {
            'mergelist': [],
            'myopts': {'--load-average': edo[1], '--jobs': edo[3]},
            'favorites': []
        }

    # getResumeList
    # return resume list
    #
    # @return    resume list stored in memory
    def getResumeList(self): 
        return self.db[self.target]['mergelist']

    # getTarget
    # get target 'resume' || 'resume_backup' if -b flag is set
    #
    # @return    string containing current resumt list target
    def getTarget(self):
        return self.target

    # getTargetResumeListData
    # get the data for the target resume list
    def getTargetResumeListData(self):
        return self.db[self.target]

    # setTargetResumeList
    # set the data for the target resume list
    #
    # @param data    resume list data
    def setTargetResumeList(self, data):
        self.db[self.target] = data
        self.db.commit()

    # addItems
    # add item to resume list
    #
    # @param  items    items to be added to the portage resume list
    def addItems(self, items):
        for item in items:
            # create item entry
            entry = ['ebuild', '/', '{}'.format(item), 'merge']
            # check for favorite
            favorite = dbutil.packageIsFavorite(item)
            if not favorite == None:
                # set favorite
                self.db[self.target]['favorites'].append(favorite)
            # add item to dict loaded in memory
            self.db[self.target]['mergelist'].append(entry)
        # write changes to disk
        self.db.commit()

    # removeItems
    # remove item from resume list by item number
    #
    # @param  itemNums    list of item numbers to be removed
    # @return             list of removed item package names
    def removeItems(self, itemNums):
        # init return
        removed = []
        # store resume list locally
        tmpList = self.db[self.target]['mergelist']
        # remove all item nums form the resume list
        # new list with removed items
        newList = []
        # iterate all item numbers building new list with ommitted items
        for i in range(len(tmpList)):
            # ommit item?
            if i in itemNums:
                removed.append(tmpList[i][2])
            else:
                # don't ommit item
                newList.append(tmpList[i])
        # save new mergelist
        self.db[self.target]['mergelist'] = newList
        # write changes to disk
        self.db.commit()
        # return list of removed item package names
        return removed

    # clearList
    # clear portage resume list
    def clearList(self):
        # clear list in memory
        self.db[self.target] = self.createEmptyTarget()
        # write changes to disk
        self.db.commit()
