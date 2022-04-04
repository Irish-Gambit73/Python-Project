from direct.showbase.ShowBase import ShowBase 
from panda3d.core import loadPrcFileData 


configVars = """
win-size 1280 720
show-frame-rate-meter 1
"""
loadPrcFileData("", configVars)


class Guts_Rage(ShowBase):
    def __init__ (self):
        super().__init__() 

             #just for now
        self.set_background_color(0, 0, 1, 0) 
        self.cam.setPos(0, -30, 5)

        self.player = self.loader.loadModel("Models/alliedflanker.egg")
        self.player.reparentTo(self.render)

        # F1 for key_map 
        self.accept("arrow_left", update_key_map, ["left", True])
        self.accept("arrow_left-up", update_key_map, ["left", False])
        self.accept("arrow_right", update_key_map, ["right, True"])
        self.accept("arrow_right-up", update_key_map, ["right", False]) 

        # F2 for update/pass
        self.taskMgr.add(self.update, "update")




# F1
key_map = {
            "left": False,
            "right": False,
        }

def update_key_map(control_name, state):
    key_map[control_name] = state

# F2
def update(self, task):
    print("F2_updated")
    return task.cont





        


Guts_Rage = Guts_Rage()
Guts_Rage.run()