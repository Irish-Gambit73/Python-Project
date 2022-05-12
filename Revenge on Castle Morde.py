from turtle import update
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, Vec3
from panda3d.core import CollisionBox, CollisionTraverser, CollisionHandlerQueue, CollisionNode, BitMask32, CollisionSegment, CollisionHandlerEvent, CollisionRay, CollisionParabola
from panda3d.core import *

configVars = """
win-size 1280 720
show-frame-rate-meter 1
"""

loadPrcFileData("", configVars)

key_map = {
    "left": False,
    "right": False,
    "attack": False,
    "left2": False,
    "right2": False,
}


def update_key_map(control_name, state):
    """ This function is called when keys are pressed or released. It updates the key_map dict."""
    key_map[control_name] = state


class Platformer(ShowBase):
    def __init__(self):
        super().__init__()
        self.set_background_color(0, 0, 0, 1)
        self.cam.setPos(0, -65, 15)

        # Guts
        self.player = self.loader.loadModel("Models/Guts.glb")
        self.player.node().setIntoCollideMask(BitMask32.bit(2))
        self.player.reparentTo(self.render)
        self.player.setScale(1)
        self.player.setHpr(90, 0, 0)
        playerhealth = 100

        # Flor
        self.floor = self.loader.loadModel("Models/floor")
        self.floor.reparentTo(self.render)

        # Godo
        self.player2 = self.loader.loadModel("Models/godo.glb")
        self.player2.reparentTo(self.render)
        self.player2.setScale(1)
        player2health = 100

        # keyboard input
        self.accept("a", update_key_map, ["left", True])
        self.accept("a-up", update_key_map, ["left", False])
        self.accept("d", update_key_map, ["right", True])
        self.accept("d-up", update_key_map, ["right", False])
        self.accept("w", self.jump)
        self.accept("space", update_key_map, ["attack", True])
        self.accept("space-up", update_key_map, ["attack", False])
        self.accept("l", update_key_map, ["left2", True])
        self.accept("l-up", update_key_map, ["left2", False])
        self.accept("'", update_key_map, ["right2", True])
        self.accept("'-up", update_key_map, ["right2", False])

        # adding the update method to the Task manager
        self.taskMgr.add(self.update, "update")

        # Movement vec's
        self.position = Vec3(0, 0, 30)
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)

        # Movement constants
        self.SPEED = 4
        self.GRAVITY = -0.05
        self.JUMP_FORCE = 1.2
        self.FRICTION = -0.12

        # Collision detection
        self.cTrav = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        # collision node for the Player
        collider_node = CollisionNode("box-coll")
        # collision geometry for the Player
        coll_box = CollisionBox((-1, -1, 0), (1, 1, 4))
        collider_node.setFromCollideMask(BitMask32.bit(1))
        collider_node.addSolid(coll_box)
        collider = self.player.attachNewNode(collider_node)
        self.cTrav.addCollider(collider, self.queue)
        collider.show()

        # Jump variables
        self.is_jumping = False
        self.is_on_floor = True
        self.jump_count = 0

        # Attack variables
        self.is_attacking = False
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

    def setEnemy(self, enemyCol):
        self.enemyCol = enemyCol

    def update(self, task):
        dt = globalClock.getDt()

        self.acceleration = Vec3(0, 0, self.GRAVITY)

        if key_map["right"]:  # if right is True
            self.acceleration.x = self.SPEED * dt
        if key_map["left"]:  # if left is True
            self.acceleration.x = -self.SPEED * dt
        if key_map["right2"]:
            self.acceleration.x = self.SPEED * dt
        if key_map["left2"]:
            self.accelration.x = self.SPEED * dt
        if key_map["attack"]:
            attackray = CollisionBox((-5, 5, 0), (1, 1, 6) )
            attackray_node = CollisionNode("attack-ray")
            attackray_node.setFromCollideMask(BitMask32.bit(0))
            attackray_node.addSolid(attackray)
            attackrayphysical = self.player.attachNewNode(attackray_node)
            self.cTrav.addCollider(attackrayphysical, self.queue)
            attackrayphysical.show()

        # calculating the position vector based on the velocity and the acceleration vectors
        self.acceleration.x += self.velocity.x * self.FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + (self.acceleration * 0.5)

        for entry in self.queue.getEntries():

            inp = entry.getIntoNodePath().getPos(self.render)

            if self.velocity.z < 0:  # prevent snapping to the top of the platforms
                if not self.is_jumping:
                    self.position.z = inp.z
                    self.velocity.z = 0  # prevent fast falling from platforms
                    self.is_on_floor = True
                else:
                    self.is_jumping = False

        self.player.setPos(self.position)

        return task.cont


game = Platformer()
game.run()
