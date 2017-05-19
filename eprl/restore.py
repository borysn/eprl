# restore.py
# author: borysn
# license: MIT
import os, datetime, re, pickle

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

    # export
    # export portage resume list
    #
    # @param data    portage mtimedb resume list data to be exported
    def export(self, data):
        # file name datetime str
        file = re.sub(r'[^\w]', '', str(datetime.datetime.now()))
        # pickle data
        # write data to file
        file = open(os.path.join(self.dir, file), 'wb+')
        pickle.dump(data, file)
        # close file
        file.close()
