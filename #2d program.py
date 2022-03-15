from direct.showbase.ShowBase import ShowBase 





class Guts_Rage(ShowBase):
    def __init__ (self):
        super().__init__() 

        self.disableMouse()
        
        print(self.render)
        print(self.camera)
        print(self.cam)


        


Guts_Rage = Guts_Rage()
Guts_Rage.run()