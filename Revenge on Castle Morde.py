from turtle import delay, update
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, Vec3
from panda3d.core import CollisionBox, CollisionTraverser, CollisionHandlerQueue, CollisionNode, BitMask32, CollisionHandler
from panda3d.core import *
from direct.task import Task
from time import time
import time

configVars = """
win-size 1280 720
show-frame-rate-meter 1
"""

loadPrcFileData("", configVars)

key_map = {
    "left": False,
    "right": False,
    "left2": False,
    "right2": False,
}


def update_key_map(control_name, state):
    key_map[control_name] = state


class Platformer(ShowBase):
    def __init__(self):
        super().__init__()
        self.set_background_color(0, 0, 15, 0)
        self.cam.setPos(0, -65, 15)

        # Guts
        self.player = self.loader.loadModel("Models/guts21.glb")
        self.player.node().setIntoCollideMask(BitMask32.bit(2))
        self.player.reparentTo(self.render)
        self.player.setScale(1)
        self.player.setHpr(80, 0, 0)
        self.playerhealth = 100

        # Flor
        self.floor = self.loader.loadModel("Models/floor")
        self.floor.reparentTo(self.render)

        # Godo
        self.player2 = self.loader.loadModel("Models/Godo.glb")
        self.player2.reparentTo(self.render)
        self.player2.setScale(1)
        self.player2.node().setIntoCollideMask(BitMask32.bit(2))
        self.player2.setHpr(-80, 0, 0)
        self.player2health = 100

        # keyboard input
        self.accept("a", update_key_map, ["left", True])
        self.accept("a-up", update_key_map, ["left", False])
        self.accept("d", update_key_map, ["right", True])
        self.accept("d-up", update_key_map, ["right", False])
        self.accept("w", self.jump)
        self.accept("space", self.attack)
        self.accept("l", update_key_map, ["left2", True])
        self.accept("l-up", update_key_map, ["left2", False])
        self.accept("'", update_key_map, ["right2", True])
        self.accept("'-up", update_key_map, ["right2", False])
        self.accept("p", self.jump2)

        # adding the update method to the Task manager
        self.taskMgr.add(self.update, "update")

        # Movement vec's for player1 and player2
        self.position = Vec3(0, 0, 30)
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)

        self.position2 = Vec3(0, 0, 40)
        self.velocity2 = Vec3(0, 0, 0)
        self.acceleration2 = Vec3(0, 0, 0)

        # Movement constants
        self.islookingleft = False
        self.islookingright = False
        self.islookingleft2 = False
        self.islookingright2 = False
        
        self.SPEED = 4
        self.GRAVITY = -0.05
        self.JUMP_FORCE = 1.2
        self.FRICTION = -0.12

        self.SPEED2 = 4
        self.GRAVITY2 = -0.05
        self.JUMP_FORCE2 = 1.2
        self.FRICTION2 = -0.12

        # Collision detection
        self.cTrav = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        collider_node = CollisionNode("p1-coll")
        coll_box = CollisionBox((-1, -1, 0), (1, 1, 6.5))
        collider_node.setFromCollideMask(BitMask32.bit(1))
        collider_node.addSolid(coll_box)
        collider = self.player.attachNewNode(collider_node)
        self.cTrav.addCollider(collider, self.queue)
        collider.show()

        self.queue2 = CollisionHandlerQueue()
        collider_nodep2 = CollisionNode("p2-coll")
        coll_box2 = CollisionBox((-1, -1, 0), (1, 1, 6))
        collider_nodep2.setFromCollideMask(BitMask32.bit(1))
        collider_nodep2.addSolid(coll_box2)
        collider2 = self.player2.attachNewNode(collider_nodep2)
        self.cTrav.addCollider(collider2, self.queue2)
        collider2.show()

        # Jump variables
        self.is_jumping = False
        self.is_on_floor = True
        self.jump_count = 0

        self.is_jumping2 = False
        self.is_on_floor2 = True
        self.jump_count2 = 0

        # Attack variables
        self.is_attacking = False
        self.is_attacking2 = False
        self.is_attacking3 = False
        self.attack_count = 0
        self.is_not_attacking = True

    def jump(self):
        if self.is_on_floor:
            self.is_jumping = True
            self.is_on_floor = False
            self.velocity.z = self.JUMP_FORCE
            self.jump_count += 1
            if self.jump_count == 2:
                self.is_jumping = False
                self.is_on_floor = True
                self.jump_count = 0

    def jump2(self):
        if self.is_on_floor2:
            self.is_jumping2 = True
            self.is_on_floor2 = False
            self.velocity2.z = self.JUMP_FORCE2
            self.jump_count2 += 1
            if self.jump_count2 == 2:
                self.is_jumping2 = False
                self.is_on_floor2 = True
                self.jump_count2 = 0

    def attack(self, task):
        self.is_attacking = True
        




    def setEnemy(self, enemyCol):
        self.enemyCol = enemyCol

    def update(self, task):
        dt = globalClock.getDt()

        self.acceleration = Vec3(0, 0, self.GRAVITY)
        self.acceleration2 = Vec3(0, 0, self.GRAVITY2)

        if key_map["right"]:  # if right is True
            self.acceleration.x = self.SPEED * dt
            self.islookingright = True
        if key_map["left"]:  # if left is True
            self.acceleration.x = -self.SPEED * dt
            self.islookingleft = True
        if key_map["right2"]:
            self.acceleration2.x = self.SPEED2 * dt
            self.islookingright2 = True
        if key_map["left2"]:
            self.acceleration2.x = -self.SPEED2 * dt
            self.islookingleft2 = True

        # calculating the position vector based on the velocity and the acceleration vectors
        self.acceleration.x += self.velocity.x * self.FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + (self.acceleration * 0.5)

        self.acceleration2.x += self.velocity2.x * self.FRICTION2
        self.velocity2 += self.acceleration2
        self.position2 += self.velocity2 + (self.acceleration2 * 0.5)


        for entry in self.queue.getEntries():

            inp = entry.getIntoNodePath().getPos(self.render)

            if self.velocity.z < 0:  # prevent snapping to the top of the platforms
                if not self.is_jumping:
                    self.position.z = inp.z
                    self.velocity.z = 0  # prevent fast falling from platforms
                    self.is_on_floor = True
                else:
                    self.is_jumping = False

        for entry in self.queue2.getEntries():

            inp2 = entry.getIntoNodePath().getPos(self.render)

            if self.velocity2.z < 0:  # prevent snapping to the top of the platforms
                if not self.is_jumping2:
                    self.position2.z = inp2.z
                    self.velocity2.z = 0  # prevent fast falling from platforms
                    self.is_on_floor2 = True
                else:
                    self.is_jumping2 = False

        self.player.setPos(self.position)
        self.player2.setPos(self.position2)

        self.cam.setX(self.position.x)

        return task.cont


game = Platformer()
game.run()
