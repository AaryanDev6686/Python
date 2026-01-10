from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    DirectionalLight,
    AmbientLight,
    KeyboardButton,
    ClockObject,
    WindowProperties
)
from direct.task import Task


class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.eye_height = 1.7

        # ================= WINDOW / MOUSE =================
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)

        self.center_x = self.win.getXSize() // 2
        self.center_y = self.win.getYSize() // 2
        self.win.movePointer(0, self.center_x, self.center_y)

        self.heading = 0
        self.pitch = 0
        self.sensitivity = 0.1

        # ================= LIGHTING =================
        dlight = DirectionalLight("dlight")
        dlight.setColor((1, 1, 1, 1))
        dlight_np = self.render.attachNewNode(dlight)
        dlight_np.setHpr(0, -60, 0)
        self.render.setLight(dlight_np)

        alight = AmbientLight("alight")
        alight.setColor((0.4, 0.4, 0.4, 1))
        alight_np = self.render.attachNewNode(alight)
        self.render.setLight(alight_np)

        # ================= GROUND =================
        self.ground = self.loader.loadModel("models/environment")
        self.ground.reparentTo(self.render)
        self.ground.setScale(0.25)
        self.ground.setPos(-8, 42, 0)

        # ================= PLAYER =================
        self.player = self.loader.loadModel("models/panda")
        self.player.reparentTo(self.render)
        self.player.setScale(0.005)
        self.player.setPos(0, 0, 0)

        # Camera attached to player (FPS)
        self.camera.reparentTo(self.player)
        self.camera.setPos(0, 0, self.eye_height)
       


        # ================= MOVEMENT =================
        self.speed = 5000

        # ================= JUMP / GRAVITY =================
        self.velocity_z = 0
        self.gravity = -30
        self.jump_strength = 12
        self.ground_z = 0

        self.taskMgr.add(self.update, "update")

    def update(self, task):
        dt = ClockObject.getGlobalClock().getDt()

        # ================= FPS MOUSE LOOK =================
        if self.win.hasPointer(0):
            md = self.win.getPointer(0)

            dx = md.getX() - self.center_x
            dy = md.getY() - self.center_y

            self.heading -= dx * self.sensitivity
            self.pitch -= dy * self.sensitivity
            self.pitch = max(-80, min(80, self.pitch))

            self.player.setH(self.heading)
            self.camera.setP(self.pitch)

            self.win.movePointer(0, self.center_x, self.center_y)

        # ================= MOVEMENT =================
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.ascii_key('w')):
            self.player.setY(self.player, self.speed * dt)

        if self.mouseWatcherNode.isButtonDown(KeyboardButton.ascii_key('s')):
            self.player.setY(self.player, -self.speed * dt)

        if self.mouseWatcherNode.isButtonDown(KeyboardButton.ascii_key('a')):
            self.player.setX(self.player, -self.speed * dt)

        if self.mouseWatcherNode.isButtonDown(KeyboardButton.ascii_key('d')):
            self.player.setX(self.player, self.speed * dt)

        # ================= JUMP =================
        if (
            self.mouseWatcherNode.isButtonDown(KeyboardButton.space())
            and self.player.getZ() <= self.ground_z + 0.01
        ):
            self.velocity_z = self.jump_strength

        # ================= GRAVITY =================
        self.velocity_z += self.gravity * dt
        new_z = self.player.getZ() + self.velocity_z * dt

        if new_z < self.ground_z:
            new_z = self.ground_z
            self.velocity_z = 0

        self.player.setZ(new_z)

        return Task.cont


# ================= START GAME =================
game = MyGame()
game.run()
