from pygame import *
from random import randint

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)

mixer.init()
#mixer.music.loud('space.ogg')
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = "galaxy.jpg"
img_bullet = "bullet.png"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_ast = "asteroid.png"
img_hp = "health.png"
score = 0
goal = 13
lost = 0
max_lost = 3


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

        
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, hp):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.hp = hp

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x = self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x = self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y +=  self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


class Asteroid(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, direction):
        super().__init__(player_image,player_x, player_y, size_x, size_y, player_speed)
        self.direction = direction
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height or self.rect.x > win_width or self.rect.x < 0:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            self.direction = randint(0, 1)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10, 5)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Asteroid(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1, 5), randint(0, 1))
    asteroids.add(asteroid)

bonus_hp = GameSprite('algoritmikahp.png', randint(80, win_width - 80), randint(80, win_height - 120), 30, 30, 0)

bullets = sprite.Group()

finish = False

run = True
while run:
    for e in event.get():
        if e .type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key ==K_SPACE:
                fire.sound.play()
                ship.fire()
    if not finish:
        window.blit(background, (0, 0))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        bonus_hp.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c  in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80),  -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if sprite.spritecollide(ship, asteroids, True):
            if ship.hp > 3:
                asteroid = Asteroid(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1, 5), randint(0, 1))
                asteroids.add(asteroid)
                shipl.hp -= 3
            else:
                finish = True
                window.blit(lose, (200, 200))

        if sprite.spritecollide(bonus_hp, bullets, True):
            ship.hp += 1
            bonus_hp.rect.x = randint(80, win_width - 80)
            bonus_hp.rect.y = randint(80, win_width - 120)



        if sprite.spritecollide(ship, monsters, True):
            if ship.hp > 1:
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(monster)
                ship.hp -= 1
            else:
                finish = True
                window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Счёт:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        hp_score = font2.render("Количество жизней:" + str(ship.hp), 1, (255, 255, 255))
        window.blit(hp_score, (10, 80))

        display.update()



    time.delay(50)







