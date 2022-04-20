#player

from direct.showbase.ShowBase import ShowBase
from panda3d.core import KeyboardButton
import sys


class Player(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.keyMap = {
            "left": 0, "right": 0, "forward": 0}

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
        return task.cont


PlayerScript = Player()
PlayerScript.run()
