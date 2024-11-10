import os
import xml.etree.ElementTree as ET
from xml.dom import minidom


class ProjectInfo:
    def __init__(self):
        self.name = ""
        self.path = ""
        return

    def setFullPath(self, fullpath):
        self.path = fullpath
        _, name = os.path.split(fullpath)
        self.name = name

    def setRelativePath(self, relativePath):
        self.directory = os.getcwd()
        self.path = os.path.join(self.directory, relativePath)
        _, name = os.path.split(self.path)
        self.name = name


global currentProjectInfo
currentProjectInfo = ProjectInfo()

global lastChose
lastChose = None
