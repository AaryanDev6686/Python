from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# ---------------- WINDOW ----------------
window.title = "Mini Battle Game"
window.fps_counter.enabled = True

# ---------------- SPAWN POINTS ----------------
spawn_points = [
    Vec3(0,1,0),
    Vec3(5,1,5),
    Vec3(-5,1,-5),
    Vec3(6,1,-6),
    Vec3(-6,1,6)
]

spawn = random.choice(spawn_points)

# ---------------- GROUND ----------------
ground = Entity(model='plane', scale=(20,1,20), color=color.green, collider='box')

# ---------------- WALLS ----------------
wall_data = [
    ((0,1,10),(20,3,1)), ((0,1,-10),(20,3,1)),
    ((10,1,0),(1,3,20)), ((-10,1,0),(1,3,20))
]

for pos, scale in wall_data:
    Entity(model='cube', position=pos, scale=scale, color=color.gray, collider='box')

# ---------------- PLAYER ----------------
player = FirstPersonController()
player.position = spawn
player.gravity = 0.5
player.speed = 5
player.health = 100

# Player hitbox (for damage only)
player_hitbox = Entity(
    parent=player,
    model='cube',
    scale=(1,2,1),
    position=(0,1,0),
    collider='box',
    visible=False
)

health_text = Text(text="HP: 100", position=(-0.85,0.45), scale=2)
game_over = Text(text="GAME OVER", scale=5, origin=(0,0), enabled=False)

# ---------------- ENEMY ----------------
class Enemy:
    def __init__(self, position=(0,1,0)):
        self.root = Entity(position=Vec3(*position))

        # Visual body (NO COLLISION)
        Entity(parent=self.root, model='cube', scale=(0.5,1.2,0.5), color=color.red, collider=None)
        Entity(parent=self.root, model='sphere', scale=0.5, position=(0,0.85,0), color=color.red)
        Entity(parent=self.root, model='sphere', scale=0.5, position=(0,-0.85,0), color=color.red)

        # Invisible hitbox
        self.hitbox = Entity(
            parent=self.root,
            model='cube',
            scale=(0.6,2,0.6),
            collider='box',
            visible=False
        )

        self.health = 3
        self.speed = 2.2

    def update(self):
        if game_over.enabled:
            return

        direction = (player.position - self.root.position).normalized()
        self.root.position += direction * self.speed * time.dt

        # Damage player
        if self.hitbox.intersects(player_hitbox).hit:
            player.health -= 30 * time.dt
            health_text.text = f"HP: {int(player.health)}"
            if player.health <= 0:
                game_over.enabled = True
                mouse.locked = False

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            destroy(self.root)
            if self in enemies:
                enemies.remove(self)

# ---------------- SPAWN ENEMIES (SAFE SPAWN) ----------------
enemies = []
enemy_count = 6
min_distance = 6

def get_safe_position():
    while True:
        pos = Vec3(
            random.randint(-8, 8),
            1,
            random.randint(-8, 8)
        )
        if distance(pos, player.position) >= min_distance:
            return pos

for i in range(enemy_count):
    enemies.append(Enemy(position=get_safe_position()))

    

# ---------------- BULLET ----------------
class Bullet(Entity):
    def __init__(self, position, direction):
        super().__init__(
            model='sphere',
            scale=0.2,
            color=color.yellow,
            position=position,
            collider='box'
        )
        self.direction = direction
        self.speed = 25
        destroy(self, delay=2)

    def update(self):
        self.position += self.direction * self.speed * time.dt
        for e in enemies[:]:
            if self.intersects(e.hitbox).hit:
                e.take_damage()
                destroy(self)
                break

# ---------------- INPUT ----------------
def input(key):
    if key == 'left mouse down' and not game_over.enabled:
        Bullet(
            position=player.position + Vec3(0,1,0),
            direction=player.forward
        )

# ---------------- UPDATE ----------------
def update():
    for e in enemies[:]:
        e.update()

app.run()
