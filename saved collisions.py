        #P1 model collisions (UNFINISHED)
        self.GutsCSphere = CollisionSphere(0, 0, 0, 0.001)
        self.GutsCNode = CollisionNode('Guts')
        self.GutsCNode.addSolid(self.GutsCSphere)
        self.GutsCNode.setFromCollideMask(BitMask32.bit(0))
        self.GutsCNode.setIntoCollideMask(BitMask32.allOff())
        self.GutsCTask = self.Guts.attachNewNode(self.GutsCNode)

        self.cTrav = CollisionTraverser()
        self.GutsCGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.GutsCTask, self.GutsCGroundHandler)
        taskMgr.add(self.traverseTask, "tsk_traverse")

    def traverseTask(self, task=None):
        self.collTrav.traverse(self.render)
        self.GutsCGroundHandler.sortEntries()
        for i in range(self.ballModelGroundHandler.getNumEntries()):
            entry = self.ballModelGroundHandler.getEntry(i)
        if task: return task.cont 
        
        #P2 Model Collisions
        self.CascaCSphere = CollisionSphere(0, 0, 0, 0.001)
        self.CascaCNode = CollisionNode('box.egg')
        self.CascaCNode.addSolid(self.CascaCSphere)
        self.CascaCNode.setFromCollideMask(BitMask32.bit(0))
        self.CascaCNode.setIntoCollideMask(BitMask32.allOff())
        self.CascaCTask = self.Casca.attachNewNode(self.CascaCNode)
        self.Casca.setCollideMask(BitMask32.bit(0))

        #Bottom (Ground) collision 
        bottom = CollisionLine(0, -1, 0, 0, -1, 0)