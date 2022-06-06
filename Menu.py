from direct.showbase.ShowBase import ShowBase
from panda3d.core import CardMaker, NodePath, loadPrcFileData
from panda3d.core import *
import sys


configVars = """
win-size 1920 1080
show-frame-rate-meter 0
"""

loadPrcFileData("", configVars)

class mymenu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.accept("escape", sys.exit)
        #Text, Gui, buttons go here 
        #if button click, run class Platformer etc.



menu = mymenu()
menu.run()