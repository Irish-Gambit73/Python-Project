__author__ = "Me"

from direct.actor.Actor import Actor 
from direct.task import Task
from player import Player

class Player():
    def __init__(self, charId, charNr):
        self.charId = charId 
        charPath = "characters/character{}/".format(charNr)
        self.character = Actor(
            charPath + "char", {
                "Idle":charPath + "idle",
                "walk":charPath + "walk"
                }) 


def __init__(self, render, startPos): 
    self.character.setH(90)
    self.character.reparentTo(render)
    self.character.hide()
    self.character.setPos(startPos) 
    self.character.show() 
    self.player = Player(0, 1) 
    self.player.start((0, 8, -0.5))
    

