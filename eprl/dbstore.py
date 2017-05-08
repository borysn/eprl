# dbstore.py
# author: borysn
# license: MIT
import util
from util import status
from colors import tcolor
# catch portage python module import error
# probably a result of not running as root
# continue script and attempt to error out
# at root privilege check
try:
    import portage
    from portage.util.mtimedb import MtimeDB
except ImportError:
    print('hmm, can\'t find portage python module, that\'s not good...')


# dbstore
# portage mtimedb data store
class DBstore:

    # constructor
    # create dbstore object for portage mtime db access
    #
    # @param  backup    flag indicating if 'resume_backup' list should be used instead of 'resume'
    def __init__(self, backup):
        # get resume items
        self.target     = 'resume_backup' if backup else 'resume'
        # attempt to get portage mtimedb
        self.db = MtimeDB(portage.mtimedbfile)
        try:
            self.resumeList = portage.mtimedb[self.target]['mergelist']
        except:
            # listing portage resume items was unsuccessful
            util.errorAndExit('cannot fetch portage resume list')

    # getResumeList
    # return resume list
    #
    # @return    resume list stored in memory
    def getResumeList(self): 
        return self.resumeList

    # getTarget
    # get target 'resume' || 'resume_backup' if -b flag is set
    #
    # @return    string containing current resumt list target
    def getTarget(self):
        return self.target

    # addItems
    # add item to resume list
    #
    # @param  items    items to be added to the portage resume list
    def addItems(self, items):
        try:
            for item in items:
                # log
                print('{}: attempting to add {}'.format(status.INFO, tcolor.CTXT(tcolor.PURPLE, item)))
                # create item entry
                entry = ['ebuild', '/', '{}'.format(item), 'merge']
                # add item to dict loaded in memory
                self.db[self.target]['mergelist'].append(entry)
            # write changes to disk
            self.db.commit()
        except:
            util.errorAndExit('could not add items to portage mtimedb')

    # removeItems
    # remove item from resume list by item number
    #
    # @param  itemNums    list of item numbers to be removed
    def removeItems(self, itemNums):
        # store resume list locally
        list = self.db[self.target]['mergelist']
        # remove all item nums form the resume list
        try:
            # new list with removed items
            tmp = []
            # iterate all item numbers building new list with ommitted items
            for i in range(len(list)):
                # ommit item?
                if i in itemNums:
                    # log
                    print('{}: attempting to remove {}'.format(status.INFO, tcolor.CTXT(tcolor.PURPLE, list[i][2])))
                else:
                    # don't ommit item
                    tmp.append(list[i])
            # save new mergelist
            self.db[self.target]['mergelist'] = tmp
            # write changes to disk
            self.db.commit()
        except:
            util.errorAndExit('could not remove item portage mtimedb')
