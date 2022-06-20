from multiprocessing.connection import wait
from turtle import delay, update
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, Vec3, Fog
from panda3d.core import CollisionBox, CollisionTraverser, CollisionHandlerQueue, CollisionHandlerEvent, CollisionNode, CollisionSphere, CollisionCapsule, BitMask32, WindowProperties, ConfigPageManager, ConfigVariableInt, ConfigVariableBool, ConfigVariableString, AntialiasAttrib, CollisionHandlerPusher, CollisionSegment
from panda3d.core import *
from panda3d.ai import *
from direct.interval.IntervalGlobal import *

from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from direct.task import Task
from time import time
import time, os, math, sys


# Welcome TO my game! The objective of the game is to catch the AI that has the sole goal of running from the player(s) until the timer runs out. 
# To catch the AI, players must use movement to close the distance and attack to eliminate the AI within the time limit
# After catching the AI, players will face increasingly difficult Ai to catch, as the AI will have increasing speed, numbers, shorter time constraints, and
# the arena will be a much more hostile place.

configVars = """
win-size 1280 720
show-frame-rate-meter 1
cursor-hidden false
"""

loadPrcFileData("", configVars)

key_map = {
    "left": False,
    "right": False,
    "left2": False,
    "right2": False,
    "space": False,
    "uparrow": False,
}

def update_key_map(control_name, state):
    key_map[control_name] = state

class RevengeOnCastleMorde(ShowBase):
    def __init__(self):
        super().__init__()
        self.set_background_color(0.5, 0.5, 1.5)
        self.cam.setPos(-5, -65, 15)
        self.camLens.setFov(50)
        self.camLens.setNear(0.8)
        self.render.setAntialias(AntialiasAttrib.MAuto)
        self.render.setShaderAuto()
        #self.disableMouse()

        self.round = 0
        self.roundadder = 1

        particles = ConfigVariableBool("particles-enabled", True).getValue()
        if particles:
            self.enableParticles()

        # Guts
        self.player = self.loader.loadModel("Models/guts21.glb")
        self.player.node().setIntoCollideMask(BitMask32.bit(2))
        self.player.reparentTo(self.render)
        self.player.setScale(1)
        self.player.show()
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
        self.enemy1attackdistance = 1.5

        # Enemy2
        self.enemy2 = self.loader.loadModel("Models/brick_wall.gltf")
        self.enemy2.reparentTo(self.render)
        self.enemy2.setScale(1)
        self.enemy2.setHpr(-90, 0, 0)
        self.enemy2health = 50
        self.enemy2isalive = True
        enemy2pos = Vec3(10, 0, 0)
        self.enemy2.setPos(enemy2pos)
        self.enemy2attackdistance = 1.5

        # First area
        self.tutorialLand = self.loader.loadModel("Models/tutorialland6.glb")
        self.tutorialLand.reparentTo(self.render)
        self.tutorialLand.setScale(1)
        self.tutorialLand.setPos(0, 0, -30)

        # keyboard input
        self.accept("a", update_key_map, ["left", True])
        self.accept("a-up", update_key_map, ["left", False])
        self.accept("d", update_key_map, ["right", True])
        self.accept("d-up", update_key_map, ["right", False])
        self.accept("w", self.jump)
        self.accept("space", update_key_map, ["space", True])
        self.accept("space-up", update_key_map,["space", False])
        self.accept("escape", sys.exit)
        self.accept("tab", self.pausemenu)
        self.accept("m", self.debugme)
        self.accept("l", update_key_map, ["left2", True])
        self.accept("l-up", update_key_map, ["left2", False])
        self.accept("'", update_key_map, ["right2", True])
        self.accept("'-up", update_key_map, ["right2", False])
        self.accept("p", self.jump2)
        self.accept("arrow_up", update_key_map, ["uparrow", True])
        self.accept("arrow_up-up", update_key_map,["uparrow", False])

        # taskMgr
        self.taskMgr.add(self.update, "update")

        # Lighting
        light = Spotlight('light')
        light_np = self.render.attachNewNode(light)
        light_np.set_pos(0, 0, 10)
        light_np.look_at(0, 0, 0)
        light_np.setColor((0, 0, 0, 0))
        light.setShadowCaster(True)
        light.getLens().setNearFar(1, 100)
        self.render.setLight(light_np)

        plight = PointLight("plight")
        plight.setColor((0, 0, 0, 0))
        plnp = self.render.attachNewNode(plight)
        plnp.look_at(0, 0, 0)
        plnp.setPos(0, 0, 10)
        self.render.setLight(plnp)

        alight = AmbientLight("alight")
        alight.setColor((0.08, 0.08, 0.08, 1))
        alnp = self.render.attachNewNode(alight)
        alnp.set_pos(0, 0, 4)
        self.render.setLight(alnp)

        expfog = Fog("scene-wide-fog")
        expfog.setColor(0, 0, 0)
        expfog.setExpDensity(0.08)
        self.render.setFog(expfog)
        

        # Movement vec's for player1 and player2
        self.position = Vec3(0, 0, 30)
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)

        self.position2 = Vec3(0, 0, 40)
        self.velocity2 = Vec3(0, 0, 0)
        self.acceleration2 = Vec3(0, 0, 0)


        self.positione1 = Vec3(-12, 0, 25)
        self.velocitye1 = Vec3(0, 0, 0)

        # Movement constants
        self.islookingleft = False
        self.islookingright = False
        self.islookingleft2 = False
        self.islookingright2 = False
        self.enemy1wontleaveZaxis = False

        self.SPEED = 5
        self.GRAVITY = -0.05
        self.JUMP_FORCE = 1.1
        self.FRICTION = -0.14

        self.SPEED2 = 5
        self.GRAVITY2 = -0.05
        self.JUMP_FORCE2 = 1.1
        self.FRICTION2 = -0.14

        self.SPEED3 = 4
        self.GRAVITY3 = -0.05

        #Collisions                                  ----------------------------------------------------------------------------
        self.collCount = 0

        # P1 Collision
        self.cTrav = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        collider_node = CollisionNode("p1coll")
        coll_box = CollisionBox((-1, -1, 0), (1, 1, 6.5))
        collider_node.setFromCollideMask(BitMask32.bit(1))
        collider_node.addSolid(coll_box)
        collider = self.player.attachNewNode(collider_node)
        self.cTrav.addCollider(collider, self.queue)
        # P1 Attack Coll. Ray
        self.queue4 = CollisionHandlerQueue()
        attackray = CollisionSegment(0, -6.8, 5, -5, 0, 5)
        attackray_node = CollisionNode("attackcol")
        attackray_node.setIntoCollideMask(BitMask32.bit(0))
        attackray_node.addSolid(attackray)
        attackraycollider = self.player.attachNewNode(attackray_node)
        self.cTrav.addCollider(attackraycollider, self.queue4)
        attackraycollider.show()

        # P2 Collision
        self.queue2 = CollisionHandlerQueue()
        collider_nodep2 = CollisionNode("p2coll")
        coll_box2 = CollisionBox((-1, -1, 0), (1, 1, 6))
        collider_nodep2.setFromCollideMask(BitMask32.bit(1))
        collider_nodep2.addSolid(coll_box2)
        collider2 = self.player2.attachNewNode(collider_nodep2)
        self.cTrav.addCollider(collider2, self.queue2)
        # P2 Attack Coll. ray
        self.queue5 = CollisionHandlerQueue()
        attackray2 = CollisionSegment(0, -6.8, 5, -5, 0, 5)
        attackray_node2 = CollisionNode("attackcol2")
        attackray_node2.setIntoCollideMask(BitMask32.bit(0))
        attackray_node2.addSolid(attackray2)
        attackraycollider2 = self.player2.attachNewNode(attackray_node2)
        self.cTrav.addCollider(attackraycollider2, self.queue5)
        attackraycollider2.show()

        # Enemy1 collision
        self.queue101 = CollisionHandlerQueue()
        collider_nodee1 = CollisionNode("e1coll")
        coll_boxe1 = CollisionCapsule(0, 0, 4, 0, 0, 4, 5)
        collider_nodee1.setFromCollideMask(BitMask32.bit(1))
        collider_nodee1.addSolid(coll_boxe1)
        collidere1 = self.enemy1.attachNewNode(collider_nodee1)
        self.cTrav.addCollider(collidere1, self.queue101)

        #Enemy2 Collision
        self.queue102 = CollisionHandlerQueue()
        collider_nodee2 = CollisionNode("e2coll")
        coll_boxe2 = CollisionBox((-3.7, -3, 0), (3.7, 3, 8))
        collider_nodee2.setFromCollideMask(BitMask32.bit(1))
        collider_nodee2.addSolid(coll_boxe2)
        collidere2 = self.enemy2.attachNewNode(collider_nodee2)
        self.cTrav.addCollider(collidere2, self.queue102)

        #                                          -------------------------------------------------------

        if self.playerhealth < 0:
            self.gamelose()
        if self.player2health < 0:
            self.gamelose()

        # Jump variables
        self.is_jumping = False
        self.is_on_floor = True
        self.jump_count = 0
        self.is_jumping2 = False
        self.is_on_floor2 = True
        self.jump_count2 = 0

        # Enemy AI
        self.AIworld = AIWorld(render)

        self.AIchar = AICharacter("enemy1", self.enemy1, 100, 0.05, 5)
        self.AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
   
        self.AIbehaviors.evade(self.player, 20, 0)
        self.AIbehaviors.obstacleAvoidance(0.3)
        self.AIworld.addObstacle(self.enemy2)

        #for Countdown
        self.countdownmovers = LerpPosInterval(self.player,
                    3,
                    (-10, 10, 0),
                    startPos=None,
                    other=None,
                    blendType='noBlend',
                    bakeInStart=1,
                    fluid=0,
                    name=None)

    def enemydeath(self):
        print("E1 HAS DIED2")
        self.round + self.roundadder
        self.enemy1.hide()
        #can do self.loader.loadModel(bloodgushing.png) and attachNode(enemy1) as a special effect

    def countdown(self):
        print("Countdown")
        self.countdownmovers.start()
        self.SPEED = 0
        self.SPEED2 = 0
        self.SPEED3 = 0
        if self.countdownmovers.finish():
            self.SPEED = 5
            self.SPEED2 = 5
            self.SPEED3 = 4

    def gamelose(self):
        print("YOUDIED")
        self.interval.start(1, 5, 1)
        #"YOU DIED" goes here
        if self.interval.finish():
            self.mainmenulaunch()
            sys.exit()
    # IF player(s) have caught escaper, setPos(startingPos) and reload everything. Countdown, new round begin load new factors data
    
    def beginround(self):
        self.round = 1
        self.player.setPos(-10, 0, 30)
        self.player2.setPos(10, 0, 30)
        self.enemy1.setPos(0, 0, 10)
        self.enemy1.show()
        if self.round == 2:
            self.round = 2
            self.player.setPos(-10, 0, 30)
            self.player2.setPos(10, 0, 30)
            self.enemy1.setPos(0, 0, 10)
            self.enemy1.show()
            if self.round == 3:
                self.player.setPos(-10, 0, 30)
                self.player2.setPos(10, 0, 30)
                self.enemy1.setPos(0, 0, 10)
                self.enemy1.show()

    def mainmenulaunch(self):
        menu = mymenu()
        menu.run()
        sys.exit

    def pausemenu(self):
        self.enableMouse
        #More buttons here

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

    def enemy1cannotleaveZaxis(self):
        enemy1wontleaveZaxis = True
        while (enemy1wontleaveZaxis == True):
            self.enemy1.getZ = 0

    def debugme(self):
        self.cTrav.showCollisions(self.render)

    def update(self, task):
        dt = globalClock.getDt()

        self.acceleration = Vec3(0, 0, self.GRAVITY)
        self.acceleration2 = Vec3(0, 0, self.GRAVITY2)
        self.acceleratione1 = Vec3(0, 0, self.GRAVITY3)

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
        if key_map["space"]:
            #slashing
            if self.queue4.getEntries():
                print("yahoo")
                self.enemy1health = (self.enemy1health - 10)
                if self.enemy1health < 0:
                    print("E1DEATH")
                    self.enemydeath()
        if key_map["uparrow"]:
            if self.queue5.getEntries():
                print("yahoo2")
                self.enemy1health = (self.enemy1health -10)
                if self.enemy1health < 0:
                    print("E!DEATH")
                    self.enemydeath()

        # Calculating the position vector based on the velocity and the acceleration vectors
        self.acceleratione1.x += self.velocitye1.x * self.FRICTION2
        self.velocitye1 += self.acceleratione1
        self.positione1 += self.velocitye1 + (self.acceleratione1 * 0.5)
        self.acceleratione1.x = self.SPEED3 * dt

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

            if self.velocity2.z < 0:
                if not self.is_jumping2:
                    self.position2.z = inp2.z
                    self.velocity2.z = 0
                    self.is_on_floor2 = True
                else:
                    self.is_jumping2 = False

        for entry in self.queue101.getEntries():

            inp3 = entry.getIntoNodePath().getPos(self.render)

            if self.velocitye1.z < 0:
                    self.positione1.z = inp3.z
                    self.velocitye1.z = 0

        self.player.setPos(self.position)
        self.player2.setPos(self.position2)
        self.enemy1.setPos(self.positione1)

        self.cam.setX(self.position.x)
        self.AIworld.update()


        return task.cont

game = RevengeOnCastleMorde()
game.run()
