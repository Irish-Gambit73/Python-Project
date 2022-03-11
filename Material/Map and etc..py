from direct.showbase.ShowBase import ShowBase   # the core of Panda3D
from panda3d.core import GeoMipTerrain          # Panda3D terrain library
 
class mygame(ShowBase):                    # our 'class' ('object' recipe)
    def __init__(self):                         # initialise object
        ShowBase.__init__(self)                 # initialise panda3d
        terrain = GeoMipTerrain("worldTerrain") # create a terrain
        terrain.setHeightfield("FirstMap.png") # set the height map
        terrain.setColorMap("MyMap1colour.png")   # set the colour map
        terrain.setBruteforce(True)             # level of detail
        root = terrain.getRoot()                # capture root
        root.reparentTo(render)                 # render from root
        root.setSz(60)                          # maximum height
        terrain.generate()
        root.writeBamFile('world.bam')                   # generate terrain
 
guts_rage = mygame()                 # our object 'instance'
guts_rage.run()