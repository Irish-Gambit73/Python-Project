from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode, CollisionTube, CollisionCapsule

def __init__(self):
    self.cTrav = CollisionTraverser()
    self.pusher = CollisionHandlerPusher()
    self.colliderNode = CollisionNode("Models/Guts.glb")
    self.colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))
    self.collider = self.tempActor.attachNewNode(colliderNode)
    self.collider.show()

    self.base.pusher.addCollider(self.collider, self.tempActor)
    self.base.cTrav.addCollider(self.collider, self.pusher)
    self.pusher.setHorizontal(True)

    self.wallSolid = CollisionCapsule(-8.0, 0, 0, 8.0, 0, 0, 0.2)
    self.wallNode = CollisionNode("Models/Brick_wall.glb")
    self.wallNode.addSolid(wallSolid)
    self.wall = render.attachNewNode(wallNode)
    self.wall.setY(8.0)

    self.wallSolid = CollisionCapsule(-8.0, 0, 0, 8.0, 0, 0, 0.2)
    self.wallNode = CollisionNode("Models/Brick_wall.glb")
    self.wallNode.addSolid(wallSolid)
    self.wall = render.attachNewNode(wallNode)
    self.wall.setY(-8.0)

    self.wallSolid = CollisionCapsule(0, -8.0, 0, 0, 8.0, 0, 0.2)
    self.wallNode = CollisionNode("Models/Brick_wall.glb")
    self.wallNode.addSolid(wallSolid)
    self.wall = render.attachNewNode(wallNode)
    self.wall.setX(8.0)

    self.wallSolid = CollisionCapsule(0, -8.0, 0, 0, 8.0, 0, 0.2)
    self.wallNode = CollisionNode("Models/Brick_wall.glb")
    self.wallNode.addSolid(wallSolid)
    self.wall = render.attachNewNode(wallNode)
    self.wall.setX(-8.0)

