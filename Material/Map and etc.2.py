from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain


class mygame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.world = self.loader.loadModel("world.bam")
        self.world.reparentTo(self.render)
        # Player model below:
        self.player = self.loader.loadModel("alliedflanker.egg")
        self.player.setPos(20, 20, 65)
        self.player.setH(100)
        self.player.reparentTo(self.render)
        self.taskMgr.add(self.updateTask, "update")
        self.keyboardSetup()
        self.speed = 0.0
        self.maxspeed = 100.0
        self.player.setScale(.2, .2, .2)

        self.maxdistance = 400
        self.camLens.setFar(self.maxdistance)
        self.camLens.setFov(71)
        # Keymappings below:

        def keyboardSetup(self):
            self.keyMap = {"left": 0, "right": 0, "jump": 0, }
            self.accept("escape", sys.exit)
            self.accept("a", self.setKey, ["left", 1])
            self.accept("a-up", self.setKey, ["left", 0])
            self.accept("d", self.setKey, ["right", 1])
            self.accept("d-up", self.setKey, ["right", 0])
            self.accept("space", self.setKey, ["jump", 1])
            self.accept("space-up", self.setKey, ["jump", 0])
            base.disableMouse()  # just for now

        def setKey(self, key, value):
            self.keyMap[key] = value

        def updateTask(self, task):
            self.updatePlayer()
            self.updateCamera()
            return Task.cont
        def updatePlayer(self):
            scalefactor = (globalClock.getDt()*self.speed)
            jumpinessfactor = scalefactor * 0.5
            speedfactor = scalefactor * 2.9
            if (self.keyMap["jump"]!=0 and self.speed > 0.00):
                self.player.setZ(self.player.getZ()+jumpinessfactor)
                self.player.setR

            


guts_rage = mygame()
guts_rage.run()
