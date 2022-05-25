from direct.showbase.ShowBase import ShowBase
from panda3d.core import CardMaker, NodePath

class Videotest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # accept the esc button to close the application
        self.accept("escape", exit)

        #videoFile = "../../data/video/video.ogv"
        videoFile = "PandaSneezes.ogv"
        movieTexture = loader.loadTexture(videoFile)
        sound = loader.loadSfx(videoFile)

        cm = CardMaker("video-screen-card-maker")
        #cm.setFrameFullscreenQuad()
        winWidth = 1920
        winHeight = 1080
        cm.setFrame(0, winWidth, -winHeight, 0)
        cm.setUvRange(movieTexture)

        # Now place the card in the scene graph and apply the texture to it.
        screen = NodePath(cm.generate())
        #screen.reparentTo(self.rende2d)
        screen.reparentTo(self.pixel2d)
        screen.setTexture(movieTexture)

        movieTexture.synchronizeTo(sound)

        # play the video by starting the sound
        sound.play()

APP = Videotest()
APP.run()