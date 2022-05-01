import pygame
import random
import os, time
os.system("start 1.0.0.exe")

GameTime = time.time()
FPS = 60
WIDTH = 500
HIGNT = 600
#顏色
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

#初始化
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HIGNT))
pygame.display.set_caption('A game of killing insects')
clock = pygame.time.Clock()

#載入圖片
background_imp = pygame.image.load(os.path.join("imp", "background.png")).convert()
player_imp = pygame.image.load(os.path.join("imp", "player.png")).convert()
player_mini_imp = pygame.transform.scale(player_imp, (30, 30))
player_mini_imp.set_colorkey(WHITE)
bug_imp = pygame.image.load(os.path.join("imp", "bug.png")).convert()
bug_mini_imp = pygame.transform.scale(bug_imp, (30, 30))
bug_mini_imp.set_colorkey(WHITE)
pygame.display.set_icon(bug_mini_imp)
bullet_imp = pygame.image.load(os.path.join("imp", "bullet.png")).convert()
rock_imgs = []
for i in range(3):
    rock_imgs.append(pygame.image.load(os.path.join("imp", f"rock{i}.png")).convert())
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(8):
    expl_imp = pygame.image.load(os.path.join("imp", f"expl{i}.png")).convert()
    expl_imp.set_colorkey(WHITE)
    expl_anim["lg"].append(pygame.transform.scale(expl_imp, (75, 75)))
    expl_anim["sm"].append(pygame.transform.scale(expl_imp, (30, 30)))
    player_expl_imp = (pygame.image.load(os.path.join("imp", f"player{i}.png")).convert())
    player_expl_imp.set_colorkey(WHITE)
    expl_anim["player"].append(player_expl_imp)
power_imps = {}
power_imps['shield'] = pygame.image.load(os.path.join("imp", "shield.png")).convert()
power_imps['gun'] = pygame.image.load(os.path.join("imp", "gun.png")).convert()

#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.wav"))
expl_sound = [
    pygame.mixer.Sound(os.path.join("sound", "Expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "Expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound", "background.wav"))
pygame.mixer.music.set_volume(0.9)


font_name = pygame.font.match_font("arial")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect =text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/200)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, imp, x, y):
    for i in range(lives):
        imp_rect = imp.get_rect()
        imp_rect.x = x + 30*i
        imp_rect.y = y
        surf.blit(imp, imp_rect)

def draw_init():
    screen.blit(background_imp, (0,0))
    draw_text(screen, 'Kill the insects!', 64, WIDTH/2, HIGNT/4)
    draw_text(screen, '←→Control the space key to fire bullets', 22, WIDTH/2, HIGNT/2)
    draw_text(screen, 'Start with any key', 18, WIDTH/2, HIGNT*3/4)
    pygame.display.update()
    winting = True
    while winting:
        clock.tick(FPS)
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                winting = False
                return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_imp, (57, 58))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 28
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HIGNT - 10
        self.speedx = 8
        self.health =200
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HIGNT - 10

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HIGNT+500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(WHITE)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *0.7 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 8)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HIGNT or self.rect.left > WIDTH or self.rect.right < 0:#重製石頭
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-180, -100)
            self.speedy = random.randrange(2, 8)
            self.speedx = random.randrange(-3, 3)  

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.image = pygame.transform.scale(bullet_imp, (20, 25))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill() 

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 40
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imps[self.type]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HIGNT:
            self.kill() 


all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)
score = 0
pygame.mixer.music.play(-1)

# 遊戲迴圈
show_init = True
running = True
while running:
    print(FPS)
    scoretime = time.time() - GameTime
    FPS += scoretime/100000
    if FPS>100:
        FPS = 100
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            r = Rock()
            all_sprites.add(r)
            rocks.add(r)
        score = 0
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    #更新遊戲
    all_sprites.update()
    #石頭與子彈碰撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(expl_sound).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
#石頭與飛船碰撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0:
            daeth_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(daeth_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 200
            player.hide()

    #寶物與飛船碰撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 40
            if player.health > 200:
                player.health = 200
            shield_sound.play()
        elif hit.type == 'gun':
            player.gunup()
            gun_sound.play()

    if player.lives == 0 and not(daeth_expl.alive()):
        show_init = True

    #畫面顯示
    screen.fill(BLACK)
    screen.blit(background_imp, (0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 22, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 10)
    draw_lives(screen, player.lives, player_mini_imp, WIDTH - 100, 15)
    pygame.display.update()

pygame.quit()