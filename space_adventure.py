import pygame

pygame.init()

root_width = 640
root_height = 780
root = pygame.display.set_mode((root_width, root_height))
pygame.display.set_caption('SPACE ADVENTURE')

clock = pygame.time.Clock()
bg_g = pygame.transform.scale(pygame.image.load('space/space_bg1.jpg'), (640, 780))
bg_m = pygame.transform.scale(pygame.image.load('space/space_bg2.jpg'), (640, 780))
bg_music = pygame.mixer.music.load('space/space_bg.mp3')
menu_b = pygame.transform.scale(pygame.image.load('space/menu_b.png'), (150, 70))
pygame.mixer.music.play(-1)

e_sound = pygame.mixer.Sound('space/explosion3.wav')
s_sound = pygame.mixer.Sound('space/explosion1.wav')
alert = pygame.mixer.Sound('space/1beeper.wav')
shipFire = pygame.mixer.Sound('space/missile2.wav')


class Ship:
    jet1 = pygame.transform.scale(pygame.image.load('space/ship1.png'), (70, 70))
    jet2 = pygame.transform.scale(pygame.image.load('space/ship2.png'), (70, 70))
    explosion = pygame.transform.scale(pygame.image.load('space/explosion1.png'), (100, 100))

    def __init__(self, x, y, width, height, jet):
        self.x = x
        self.y = y
        self.width = width
        self.jet = jet
        self.height = height
        self.vel = 8
        self.hitBox = (self.x, self.y, self.width, self.height)
        self.health = 7
        self.visible = True

    def draw(self, win):
        if self.visible:
            self.hitBox = (self.x, self.y, self.width, self.height)
            # pygame.draw.rect(win, (255, 0, 0), self.hitBox, 1)
            if self.jet == 1:
                win.blit(self.jet1, (self.x, self.y))
            else:
                win.blit(self.jet2, (self.x, self.y))
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y + self.height, self.width, 5))
            pygame.draw.rect(win, (0, 255, 0), (self.x, self.y + self.height, 70 - (10 * (7 - self.health)), 5))
        else:
            s_sound.play()
            win.blit(self.explosion, (self.x, self.y))

    def hit(self):
        if self.health == 2:
            alert.play()
        else:
            alert.stop()
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False

    def reset(self):
        self.x = 320
        self.y = 700
        self.health = 7
        self.visible = True

class Weapon:
    fire = pygame.transform.scale(pygame.image.load('space/missile1.png'), (10, 70))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10  # 684.999999999999943156

    def draw(self, win):
        win.blit(self.fire, (self.x, self.y))


class Enemy:
    e_ship = pygame.transform.scale(pygame.image.load('space/enemyShip1.png'), (300, 300))
    explosion = pygame.transform.scale(pygame.image.load('space/explosion1.png'), (300, 300))

    def __init__(self, x, y, end):
        self.x = x
        self.y = y
        self.path = (self.x, end)
        self.vel = 7
        self.hitBox = (self.x + 25, self.y, 265, 300)
        self.health = 10
        self.visible = True

    def draw(self, win):
        if self.visible:
            self.move()
            self.hitBox = (self.x + 25, self.y + 10, 252, 270)
            # pygame.draw.rect(win, (255, 0, 0), self.hitBox, 1)
            pygame.draw.rect(root, (255, 0, 0), (self.x, self.y + 5, 300, 5))
            pygame.draw.rect(root, (0, 255, 0), (self.x, self.y + 5, 300 - (30 * (10 - self.health)), 5))
            win.blit(self.e_ship, (self.x, self.y))
        else:
            e_sound.play()
            win.blit(self.explosion, (self.x, self.y))

    def move(self):
            if self.vel > 0:
                if self.x + self.vel + 300 < self.path[1]:
                    self.x += self.vel
                else:
                    self.vel *= -1
            else:
                if self.x + self.vel > self.path[0]:
                    self.x += self.vel
                else:
                    self.vel *= -1

    def hit(self):
        if self.health > 0.5:
            self.health -= 0.5
        else:
            self.visible = False

    def reset(self):
        self.x = 0
        self.y = 5
        self.health = 10
        self.visible = True



class EWeapon:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 20
        self.e_missile = pygame.transform.scale(pygame.image.load('space/e_missile1.png'), (self.width, self.height))

    def draw(self, win):
        win.blit(self.e_missile, (self.x, self.y))


def reset_values():
    globals()['score'] = 0
    global missiles
    global e_missiles
    global e_missilesR
    Falcon.reset()
    Thanos.reset()
    missiles.clear()
    e_missiles.clear()
    e_missilesR.clear()


def re_draw_everything():
    root.blit(bg_g, (0, 0))
    Falcon.draw(root)
    if Thanos.visible:
        if Falcon.visible:
            text = font.render('SCORE:' + str(score), 1, (255, 255, 255))
            root.blit(text, (250, 390))
        else:
            text = font1.render('GALAXY IS DESTROYED...', 1, (255, 255, 255))
            root.blit(text, (120, 390))
            text = font1.render('GAME OVER.', 1, (255, 255, 255))
            root.blit(text, (220, 420))
            text = font1.render('PRESS C TO RESTART..', 1, (255, 255, 255))
            root.blit(text, (120, 520))
    else:
        text = font1.render('YOU SAVED THE GALAXY.', 1, (255, 255, 255))
        root.blit(text, (120, 390))
        text = font1.render('WELL PLAYED...', 1, (255, 255, 255))
        root.blit(text, (220, 420))

    for missile in missiles:
        missile.draw(root)
    for e_missile in e_missiles:
        e_missile.draw(root)
    for e_missile in e_missilesR:
        e_missile.draw(root)
    Thanos.draw(root)
    pygame.display.update()


def re_draw_menu_window():
    root.blit(bg_m, (0, 0))
    text = font1.render('PRESS S TO START.', 1, (255, 255, 255))
    root.blit(text, (160, 190))
    text = font1.render('PRESS Q TO QUIT.', 1, (255, 255, 255))
    root.blit(text, (160, 240))
    pygame.display.update()


if __name__ == "__main__":
    Falcon = Ship(320, 700, 70, 70, 1)
    # Armada = Ship(320, 700, 70, 70, 2)
    Thanos = Enemy(0, 5, root_width + 10)


    missiles = []
    e_missiles = []
    e_missilesR = []

    score = 0
    font = pygame.font.SysFont('ink free', 50)
    font1 = pygame.font.SysFont('ink free', 30, True)
    shootDelay = 0
    e_missile_delay = 0
    e_missile_delayR = 0

    run = True
    runMain = False

    while run:
        clock.tick(35)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            runMain = True
        if keys[pygame.K_q]:
            run = False
        if keys[pygame.K_m]:
            runMain = False
            reset_values()

        if runMain:
            # FALCON MISSILE DEPLOY

            if shootDelay > 0:
                shootDelay += 1
            if shootDelay > 10:
                shootDelay = 0

            for missile in missiles:
                if missile.y > Thanos.hitBox[1] and missile.y < Thanos.hitBox[1] + Thanos.hitBox[3]:
                    if missile.x + 10 > Thanos.hitBox[0] and missile.x < Thanos.hitBox[0] + Thanos.hitBox[2]:
                        missiles.pop(missiles.index(missile))
                        score += 10
                        Thanos.hit()

            for missile in missiles:
                if missile.y > 0:
                    missile.y -= missile.vel
                else:
                    missiles.pop(missiles.index(missile))

            # ENEMY MISSILE DEPLOY

            if e_missile_delay > 0:
                e_missile_delay += 1
            if e_missile_delay > 20:
                e_missile_delay = 0

            if Thanos.visible:
                if Falcon.visible:
                    if e_missile_delay == 0:
                        e_missiles.append(EWeapon(round(Thanos.x + 45), round(Thanos.y + 300//2), 10, 50))
                        e_missile_delay = 1

            for e_missile in e_missiles:
                if e_missile.y < root_height:
                    e_missile.y += e_missile.vel
                else:
                    e_missiles.pop(e_missiles.index(e_missile))

            for e_missile in e_missiles:
                if e_missile.y < Falcon.hitBox[1] + Falcon.hitBox[3] and e_missile.y + e_missile.height > Falcon.hitBox[1]:
                    if e_missile.x + e_missile.width > Falcon.hitBox[0] and e_missile.x < Falcon.hitBox[0] + Falcon.hitBox[2]:
                        e_missiles.pop(e_missiles.index(e_missile))
                        score -= 10
                        Falcon.hit()

            if e_missile_delayR > 0:
                e_missile_delayR += 1
            if e_missile_delayR > 15:
                e_missile_delayR = 0

            if Thanos.visible:
                if Falcon.visible:
                    if e_missile_delayR == 0:
                        e_missilesR.append(EWeapon(round(Thanos.x + 245), round(Thanos.y + 300 // 2), 10, 50))
                        e_missile_delayR = 1

            for e_missile in e_missilesR:
                if e_missile.y < root_height:
                    e_missile.y += e_missile.vel
                else:
                    e_missilesR.pop(e_missilesR.index(e_missile))

            for e_missile in e_missilesR:
                if e_missile.y < Falcon.hitBox[1] + Falcon.hitBox[3] and e_missile.y + e_missile.height > Falcon.hitBox[1]:
                    if e_missile.x + e_missile.width > Falcon.hitBox[0] and e_missile.x < Falcon.hitBox[0] + Falcon.hitBox[2]:
                        e_missilesR.pop(e_missilesR.index(e_missile))
                        score -= 10
                        Falcon.hit()

            # KEY IN USE

            if not Falcon.visible:
                if keys[pygame.K_c]:
                    Falcon.visible = True
                    reset_values()

            if Thanos.visible:
                if Falcon.visible:
                    if keys[pygame.K_SPACE] and shootDelay == 0:
                        shipFire.play()
                        if len(missiles) < 10:
                            missiles.append(Weapon(round(Falcon.x - 5 + Falcon.width/2), Falcon.y))
                        shootDelay = 1
                    if keys[pygame.K_RIGHT] and Falcon.x < root_width - Falcon.width:
                        Falcon.x += Falcon.vel
                    if keys[pygame.K_LEFT] and Falcon.x > 0:
                        Falcon.x -= Falcon.vel

            # DRAW FUNCTION
            re_draw_everything()
        else:

            re_draw_menu_window()
    pygame.quit()
