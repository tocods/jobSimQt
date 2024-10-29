import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

class ProjectInfo:
    def __init__(self):
        self.directory = ""
        self.name = ""
        self.fullname = ""
        self.path = ""
        return

    def setDirAndName(self, directory, name):  # 比如 D:/fe , omnet_template
        self.directory = directory
        self.name = name
        self.fullname = directory + "/" + name
        self.path = directory + "/" + name + "/"

    def setFullname(self, fullname):  # 比如 D:/fe/omnet_template
        directory, name = os.path.split(fullname)  # 分离文件名和路径
        self.directory = directory
        self.name = name
        self.fullname = directory + "/" + name
        self.path = directory + "/" + name + "/"
        
    def setRelativePath(self, relativePath):
        self.directory = os.getcwd()
        self.name = relativePath
        self.fullname = self.directory + "\\" + relativePath
        self.path = self.directory + "\\" + relativePath + "\\"


global currentProjectInfo
currentProjectInfo = ProjectInfo()
