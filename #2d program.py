from turtle import isdown
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, AmbientLight, DirectionalLight
from direct.task import Task, TaskManagerGlobal
import simplepbr
import Player.py


class game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        configVars = """
        win-size 1280 720
        show-frame-rate-meter 1
        """
        loadPrcFileData("", configVars)

        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection((-5, -5, -5))
        directionalLight.setColor((1, 1, 1, 1))
        directionalLight.setSpecularColor((1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))



    

        
















game = ShowBase()
game.run()
