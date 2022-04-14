from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from direct.task import Task, TaskManagerGlobal
import simplepbr

configVars = """
win-size 1280 720
show-frame-rate-meter 1
"""
loadPrcFileData("", configVars)

# Window Display


class ShowBase(ShowBase):
    def __init__(self):
        super().__init__()

        simplepbr.init()
        self.floor = self.loader.loadModel("Models/floor")
        self.floor.reparentTo(self.render)

        self.Guts = self.loader.loadModel("Models/Guts.glb")
        self.Guts.reparentTo(self.render)
        self.Guts.setScale(0.05)
        self.Guts.setPos(0, 0, 1)

        self.set_background_color(0, 0, 1, 0) 
    def start(self):

        self.keyMap = {"left": 0, "right": 0, "forward": 0, "backward": 0}

        self.accept("escape", exit)
        self.accept("a", self.setKey, ["left", 1])
        self.accept("d", self.setKey, ["right", 1])
        self.accept("w", self.setKey, ["forward", 1])
        self.accept("s", self.setKey, ["backward", 1])
        self.accept("a-up", self.setKey, ["left", 0])
        self.accept("d-up", self.setKey, ["right", 0])
        self.accept("w-up", self.setKey, ["forward", 0])
        self.accept("s-up", self.setKey, ["backward", 0])

        taskMgr.add(self.move, "task_movement", priority=-10)
        self.request("Idle")
    def setKey(self, key, value):
        self.keyMap[key] = value

    def move(self, task):
        dt = globalClock.getDt()
        requestState = "Idle"
        if self.keyMap["left"] != 0:
            self.player.setH(self.player.getH() + 150 * dt)
            requestState = "Walk"
        if self.keyMap["right"] != 0:
            self.player.setH(self.player.getH() - 150 * dt)
            requestState = "Walk"
        if self.keyMap["forward"] != 0:
            self.player.setY(self.player, -15 * dt)
            requestState = "Walk"
        if self.keyMap["backward"] != 0:
            self.player.setY(self.player, 15 * dt)
            requestState = "Walk"
        if self.state != requestState:
            self.request(requestState)
        return task.cont


base = ShowBase()
base.run()
