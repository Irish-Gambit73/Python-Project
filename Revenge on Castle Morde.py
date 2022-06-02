from cgi import test
from turtle import delay, update
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, Vec3
from panda3d.core import CollisionBox, CollisionTraverser, CollisionHandlerQueue, CollisionNode, BitMask32, WindowProperties, ConfigPageManager, ConfigVariableInt, ConfigVariableBool, ConfigVariableString, AntialiasAttrib, CollisionHandlerPusher, CollisionSegment
from panda3d.core import *
from direct.task import Task
from time import time
import time, os, math, sys

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
    "space": False,
}

def update_key_map(control_name, state):
    key_map[control_name] = state


class Platformer(ShowBase):
    def __init__(self):
        super().__init__()
        self.set_background_color(0.5, 0.5, 1.5)
        self.cam.setPos(0, -65, 15)
        self.camLens.setFov(50)
        self.camLens.setNear(0.8)
        self.render.setAntialias(AntialiasAttrib.MAuto)
        render.setShaderAuto()

        particles = ConfigVariableBool("particles-enabled", True).getValue()
        if particles:
            self.enableParticles()

        # Guts
        self.player = self.loader.loadModel("Models/guts21.glb")
        self.player.node().setIntoCollideMask(BitMask32.bit(2))
        self.player.reparentTo(self.render)
        self.player.setScale(1)
        self.player.setHpr(90, 0, 0)
        self.playerhealth = 100
        self.alive = True
        # Flor
        self.floor = self.loader.loadModel("Models/floor")
        self.floor.reparentTo(self.render)

        # Godo
        self.player2 = self.loader.loadModel("Models/Godot.glb")
        self.player2.reparentTo(self.render)
        self.player2.setScale(1)
        self.player2.node().setIntoCollideMask(BitMask32.bit(2))
        self.player2.setHpr(90, 0, 0)
        self.player2health = 100
        self.alive2 = True

        # Enemy1
        self.enemy1 = self.loader.loadModel("Models/enemy1.glb")
        self.enemy1.reparentTo(self.render)
        self.enemy1.setScale(1)
        self.enemy1.setHpr(-90, 0, 0)
        self.enemy1health = 50
        self.enemyisalive = True
        enemy1startpos = Vec3(-10, 0, 0)
        self.enemy1.setPos(enemy1startpos)
        self.enemy1attackdistance = 1.5


        # keyboard input
        self.accept("a", update_key_map, ["left", True])
        self.accept("a-up", update_key_map, ["left", False])
        self.accept("d", update_key_map, ["right", True])
        self.accept("d-up", update_key_map, ["right", False])
        self.accept("w", self.jump)
        self.accept("space", self.attack)
        self.accept("escape", sys.exit)
        self.accept("m", self.debugme)
        self.accept("l", update_key_map, ["left2", True])
        self.accept("l-up", update_key_map, ["left2", False])
        self.accept("'", update_key_map, ["right2", True])
        self.accept("'-up", update_key_map, ["right2", False])
        self.accept("p", self.jump2)

        # taskMgr
        self.taskMgr.add(self.update, "update")



        # Lighting
        light = Spotlight('light')
        light_np = self.render.attachNewNode(light)
        light_np.set_pos(50, 50, 25)
        light_np.look_at(0, 1, 0)
        light.setShadowCaster(True)
        light.getLens().setNearFar(1, 100)
        self.render.setLight(light_np)

        plight = PointLight("plight")
        plight.setColor((1, 1, 1, 1))
        plnp = render.attachNewNode(plight)
        plnp.setPos(0, 65, 15)
        render.setLight(plnp)

        alight = AmbientLight("alight")
        alight.setColor((0.08, 0.08, 0.08, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)

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
        
        self.SPEED = 5
        self.GRAVITY = -0.05
        self.JUMP_FORCE = 1.1
        self.FRICTION = -0.14

        self.SPEED2 = 5
        self.GRAVITY2 = -0.05
        self.JUMP_FORCE2 = 1.1
        self.FRICTION2 = -0.14

        # Collision detection
        self.cTrav = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        collider_node = CollisionNode("p1coll")
        coll_box = CollisionBox((-1, -1, 0), (1, 1, 6.5))
        collider_node.setFromCollideMask(BitMask32.bit(1))
        collider_node.addSolid(coll_box)
        collider = self.player.attachNewNode(collider_node)
        base.pusher = CollisionHandlerPusher()
        base.pusher.addCollider(collider, self.player)
        base.cTrav.addCollider(collider, self.queue)
        # Attack Ray
        attackray = CollisionSegment(0, -6.8, 5, 0, 0, 5)
        attackray_node = CollisionNode("attackcol")
        collider_node.addSolid(attackray)
        attackray_node.setFromCollideMask(BitMask32.bit(0))
        attackraycollider = self.player.attachNewNode(collider_node)
        attackraycollider.show()


        self.queue2 = CollisionHandlerQueue()
        collider_nodep2 = CollisionNode("p2coll")
        coll_box2 = CollisionBox((-1, -1, 0), (1, 1, 6))
        collider_nodep2.setFromCollideMask(BitMask32.bit(1))
        collider_nodep2.addSolid(coll_box2)
        collider2 = self.player2.attachNewNode(collider_nodep2)
        base.pusher2 = CollisionHandlerPusher()
        base.pusher2.addCollider(collider2, self.player)
        base.cTrav.addCollider(collider2, self.queue2)

        self.queue3 = CollisionHandlerQueue()
        collider_nodee1 = CollisionNode("e1coll")
        coll_boxe1 = CollisionBox((-1.5, -1.5, 0), (1, 2, 8))
        collider_nodee1.setFromCollideMask(BitMask32.bit(1))
        collider_nodee1.addSolid(coll_boxe1)
        collidere1 = self.enemy1.attachNewNode(collider_nodee1)

        self.cTrav.addCollider(collidere1, self.queue3)



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
        self.attackcombo = 0.0

        # Collision actions
        self.pusher.add_in_pattern("%in-into-%in")

        self.accept("p1coll-into-p2coll", self.jump)


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

    def alterhealth(self):
        pass

    def taketime(task):
        self.delayTime +=1
        return task.cont

    def debugme(self):
        self.cTrav.showCollisions(self.render)



    def setEnemy(self, enemyCol):
        self.enemyCol = enemyCol

    def update(self, task):
        dt = globalClock.getDt()

        self.acceleration = Vec3(0, 0, self.GRAVITY)
        self.acceleration2 = Vec3(0, 0, self.GRAVITY2)

        if key_map["right"]:  # if right is True
            self.acceleration.x = self.SPEED * dt
            self.islookingright = True
            self.player.setHpr(90, 0, 0)
        if key_map["left"]:  # if left is True
            self.acceleration.x = -self.SPEED * dt
            self.islookingleft = True
            self.player.setHpr(-90, 0, 0)
        if key_map["right2"]:
            self.acceleration2.x = self.SPEED2 * dt
            self.islookingright2 = True
            self.player2.setHpr(90, 0, 0)
        if key_map["left2"]:
            self.acceleration2.x = -self.SPEED2 * dt
            self.islookingleft2 = True
            self.player2.setHpr(-90, 0, 0)
        if key_map["space"] and task.time > self.attackcombo:
            self.attack(task.time)
            self.attackcombo = task.time + 0.6
        key_map["space"] = 0

        # Calculating the position vector based on the velocity and the acceleration vectors
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
