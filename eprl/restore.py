# restore.py
# author: borysn
# license: MIT
import os, datetime, re, pickle
from eprl import util

# RestorePRL
# restore portage resume lists (export/import)
class RestorePRL:
    # save dir
    dir = '/var/lib/eprl'

    # constructor
    def __init__(self):
        # check save dir exists
        if not os.path.exists(self.dir):
            # create directory for storing data
            os.mkdir(self.dir)

    # exportData
    # export portage resume list
    #
    # @param data    portage mtimedb resume list data to be exported
    def exportData(self, data):
        # file name datetime str
        file = re.sub(r'[^\w]', '', str(datetime.datetime.now()))
        # write data to file
        file = open(os.path.join(self.dir, file), 'wb+')
        pickle.dump(data, file)
        # close file
        file.close()

    # importData
    # import portage resume list
    def importData(self):
        # get exported data
        exports = [os.path.join(self.dir, export) for export in os.listdir(self.dir)]
        # get user selection
        choice = util.askUserWhichItem(exports)
        # get data
        file = open(exports[choice], 'rb')
        data = pickle.load(file)
        file.close
        # return data
        return data
