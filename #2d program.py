from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from direct.task import Task, TaskManagerGlobal

configVars = """
win-size 1280 720
show-frame-rate-meter 1
"""
loadPrcFileData("", configVars)

# Window Display
class ShowBase(ShowBase):
    def __init__(self):
        super().__init__()

        self.floor = self.loader.loadModel("Models/floor")
        self.floor.reparentTo(self.render)

        # just for now
        self.set_background_color(0, 0, 1, 0)


# For Player(s)
class Player():
    def __init__(self):

        # Loading Models
        self.player = self.loader.loadModel("Models/player")
        self.player.reparentTo(self.render)
        self.player = Player(0, 1)
        self.player.show()
        # Constants
        self.Speed = 4.0
        self.Weight = -0.05
        self.Vertical = 1.2
        self.Friction = -0.12
        # Button Associations
        self.leftButton = KeyboardButton.asciiKey(b"a")
        self.rightButton = KeyboardButton.asciiKey(b"d")

        def moveTask(self, task):
            speed = 0.0
            isDown = base.mouseWatcherNode.isButtonDown
            if isDown(self.leftButton):
                speed += self.walkSpeed
            if isDown(self.rightButton):
                speed -= self.walkSpeed
            yDelta = speed * globalClock.get
            self.character.setY(self.character, yDelta)
            return task.cont 

            #FSM animations


base = ShowBase()
base.run()
