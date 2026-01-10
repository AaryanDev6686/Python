import pygame, random, json, os, math

# ================= SETTINGS =================
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MEGA SINGLE FILE RPG")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 22)

TILE = 40
FPS = 60

# Colors
WHITE=(255,255,255); BLACK=(0,0,0); RED=(255,0,0)
GREEN=(0,255,0); BLUE=(0,0,255); GRAY=(120,120,120)
YELLOW=(255,255,0)

# ================= CONTROLLER =================
if pygame.joystick.get_count():
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    joystick = None

# ================= MAP =================
MAP = [
"11111111111111111111",
"10000000000000000001",
"10000111100001110001",
"10000000000000000001",
"10000011100001110001",
"10000000000000000001",
"11111111111111111111"
]

WORLD_W = len(MAP[0]) * TILE
WORLD_H = len(MAP) * TILE

# ================= PLAYER =================
player = pygame.Rect(200, 200, 30, 30)
speed = 5
hp = 100
max_hp = 100
xp = 0
level = 1
damage = 10

# ================= INVENTORY =================
inventory = {"Potion": 2}

# ================= NPC =================
npc = pygame.Rect(300, 200, 30, 30)
dialogue = ["Welcome hero!", "Enemies hunt in squads.", "Defeat them all!"]
dlg_index = 0
show_dlg = False

# ================= ENEMIES (SQUADS) =================
enemies = []
for i in range(6):
    enemies.append({
        "rect": pygame.Rect(500+i*40, 400, 30, 30),
        "hp": 40
    })

# ================= BULLETS =================
bullets = []

# ================= SAVE / LOAD =================
def save_game():
    data = {"hp": hp, "xp": xp, "lvl": level, "inv": inventory}
    with open("save.json","w") as f:
        json.dump(data,f)

def load_game():
    global hp, xp, level, inventory
    if os.path.exists("save.json"):
        with open("save.json") as f:
            d=json.load(f)
            hp=d["hp"]; xp=d["xp"]; level=d["lvl"]; inventory=d["inv"]

load_game()

# ================= FUNCTIONS =================
def draw_text(t,x,y,c=WHITE):
    screen.blit(FONT.render(t,1,c),(x,y))

def get_input():
    dx=dy=0
    k=pygame.key.get_pressed()
    if k[pygame.K_w]: dy=-1
    if k[pygame.K_s]: dy=1
    if k[pygame.K_a]: dx=-1
    if k[pygame.K_d]: dx=1

    if joystick:
        dx=joystick.get_axis(0)
        dy=joystick.get_axis(1)
    return dx,dy

# ================= GAME LOOP =================
paused=False
running=True
while running:
    clock.tick(FPS)
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            save_game(); running=False
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_p: paused=not paused
            if e.key==pygame.K_SPACE:
                bullets.append(pygame.Rect(player.centerx,player.centery,6,6))
            if e.key==pygame.K_e and player.colliderect(npc):
                show_dlg=True; dlg_index=(dlg_index+1)%len(dialogue)
            if e.key==pygame.K_h and inventory.get("Potion",0)>0:
                hp=min(max_hp,hp+30); inventory["Potion"]-=1

    if paused:
        screen.fill(BLACK)
        draw_text("PAUSED",WIDTH//2-40,HEIGHT//2)
        pygame.display.update(); continue

    # Movement
    dx,dy=get_input()
    player.x+=dx*speed; player.y+=dy*speed
    player.clamp_ip(pygame.Rect(0,0,WORLD_W,WORLD_H))

    camx=player.x-WIDTH//2
    camy=player.y-HEIGHT//2

    # Bullets
    for b in bullets[:]:
        b.y-=10
        if b.y<0: bullets.remove(b)

    # Enemy Squad AI
    for i,en in enumerate(enemies[:]):
        dist=math.hypot(player.x-en["rect"].x,player.y-en["rect"].y)
        if dist<300:
            angle=math.atan2(player.y-en["rect"].y,player.x-en["rect"].x)
            en["rect"].x+=math.cos(angle)
            en["rect"].y+=math.sin(angle)

        if en["rect"].colliderect(player):
            hp-=1

        for b in bullets[:]:
            if en["rect"].colliderect(b):
                en["hp"]-=damage; bullets.remove(b)

        if en["hp"]<=0:
            enemies.remove(en); xp+=10

    # Level up
    if xp>=level*50:
        level+=1; damage+=5; max_hp+=20; hp=max_hp

    # Death
    if hp<=0:
        screen.fill(BLACK)
        draw_text("YOU DIED",WIDTH//2-40,HEIGHT//2,RED)
        pygame.display.update()
        pygame.time.delay(3000)
        break

    # ================= DRAW =================
    screen.fill(GRAY)

    # Map
    for y,row in enumerate(MAP):
        for x,t in enumerate(row):
            if t=="1":
                pygame.draw.rect(screen,BLACK,
                (x*TILE-camx,y*TILE-camy,TILE,TILE))

    # NPC
    pygame.draw.rect(screen,GREEN,(npc.x-camx,npc.y-camy,30,30))

    # Enemies
    for en in enemies:
        pygame.draw.rect(screen,RED,
        (en["rect"].x-camx,en["rect"].y-camy,30,30))

    # Player
    pygame.draw.rect(screen,BLUE,
    (player.x-camx,player.y-camy,30,30))

    # Bullets
    for b in bullets:
        pygame.draw.rect(screen,YELLOW,
        (b.x-camx,b.y-camy,6,6))

    # UI
    draw_text(f"HP: {hp}",10,10)
    draw_text(f"XP: {xp}",10,30)
    draw_text(f"Level: {level}",10,50)
    draw_text(f"Potions: {inventory.get('Potion',0)}",10,70)

    if show_dlg:
        pygame.draw.rect(screen,BLACK,(200,450,500,100))
        draw_text(dialogue[dlg_index],220,480)

    pygame.display.update()

pygame.quit()
