# dbstore.py
# author: borysn
# license: MIT
import os, re

# constants
worldFile = '/var/lib/portage/world'
stripVersion = lambda x: re.split('-\d.', x)[0]

# isInWorldFile
# see if the world file has a match for the given dependency string
#
# @param depstr    depedency with version stripped
# return           true if depstr is found in the world file
def isInWorldFile(depstr):
    # open world file
    f = open(worldFile, 'r')
    # get file contents
    content = f.read()
    # close file
    f.close()
    # return match or not
    return depstr in content

# packageIsFavorite
# check if the given dependency is found in the world file
#
# @param dep    portdbapi matched dependency name
# return        string containing dependency with version truncated if package is a favorite, None otherwise
def packageIsFavorite(dep):
    # get dependency string without version
    depstr = stripVersion(dep)
    # test
    if isInWorldFile(depstr):
        return depstr
    # return test for match
    return None
