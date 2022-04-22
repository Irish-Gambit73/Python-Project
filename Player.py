#player

from direct.showbase.ShowBase import ShowBase
from panda3d.core import KeyboardButton
import sys, simplepbr


class Player(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.keyMap = {
            "left": 0, "right": 0, "forward": 0, "backward": 0, "leftp2": 0, "rightp2": 0, "forwardp2": 0, "backwardp2": 0}

        simplepbr.init()
        self.Guts = self.loader.loadModel("Models/Guts.glb")
        self.Guts.reparentTo(self.render)
        self.Guts.setScale(0.05)
        self.Guts.setPos(0, 5, 1)

        self.accept("escape", sys.exit)
        self.accept("a", self.setKey, ["left", True])
        self.accept("d", self.setKey, ["right", True])
        self.accept("w", self.setKey, ["forward", True])
        self.accept("a-up", self.setKey, ["left", False])
        self.accept("d-up", self.setKey, ["right", False])
        self.accept("w-up", self.setKey, ["forward", False])
        self.accept("s", self.setKey, ["backward", True])
        self.accept("s-up", self.setKey, ["backward", False])

        self.floor = self.loader.loadModel("Models/floor")
        self.floor.reparentTo(self.render)

        self.casca = self.loader.loadModel("Models/player.egg")
        self.casca.reparentTo(self.render)
        self.casca.setScale(0.05)
        self.casca.setPos(0, 5, 1)

        self.accept("j", self.setKey, ["leftp2", True])
        self.accept("l", self.setKey, ["rightp2", True])
        self.accept("i", self.setKey, ["forwardp2", True])
        self.accept("j-up", self.setKey, ["leftp2", False])
        self.accept("l-up", self.setKey, ["rightp2", False])
        self.accept("i-up", self.setKey, ["forwardp2", False])
        self.accept("k", self.setKey, ["backwardp2", True])
        self.accept("k-up", self.setKey, ["backwardp2", False])


        taskMgr.add(self.move, "moveTask")

        self.isMoving = False
    def setKey(self, key, value):
        self.keyMap[key] = value
    def move(self, task):
        dt = globalClock.getDt()
        if self.keyMap["left"]:
            self.Guts.setH(self.Guts.getH() + 300 * dt)
        if self.keyMap["right"]:
            self.Guts.setH(self.Guts.getH() - 300 * dt)
        if self.keyMap["forward"]:
            self.Guts.setY(self.Guts, -25 * dt)
        if self.keyMap["backward"]:
            self.Guts.setY(self.Guts, 25 * dt)
        
        if self.keyMap["leftp2"]:
            self.casca.setH(self.casca.getH() + 300 * dt)
        if self.keyMap["rightp2"]:
            self.casca.setH(self.casca.getH() - 300 * dt)
        if self.keyMap["forwardp2"]:
            self.casca.setY(self.casca, -25 * dt)
        if self.keyMap["backwardp2"]:
            self.casca.setY(self.casca, 25 * dt)
        
        return task.cont



PlayerScript = Player()
PlayerScript.run()
