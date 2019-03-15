"""
    Asteroids v1.0.0
    Copyright (C) 2018  Ryan I Callahan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pygame
import sys
import random
background = (0, 0, 0)
entity_color = (255, 255, 255)

tick = 60

player_lives = 1
player_score = 0
fire_timer = True
you_lose = False
lose_sound = False
play = False
fire_rate = 500
laser = pygame.image.load('laser.png')
piercing = False
class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Paddle(Entity):
    """
    Player controlled or AI controlled, main interaction with
    the game
    """

    def __init__(self, x, y, width, height):
        super(Paddle, self).__init__(x, y, width, height)

class Bullet(Entity):


    def __init__(self, x, y, width, height, sprite):
        super(Bullet, self).__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.sprite = sprite

    def update(self):
        self.rect.x += self.speed
        screen.blit(self.sprite, (self.rect.x, self.rect.y))


class Player(Paddle):
    """The player controlled Paddle"""

    def __init__(self, x, y, width, height, playersprite, bulletsprite):
        super(Player, self).__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # How many pixels the Player Paddle should move on a given frame.
        self.y_change = 0
        # How many pixels the paddle should move each frame a key is pressed.
        self.y_dist = 5
        self.sprite = playersprite
        self.bullet = bulletsprite

    def changeshot(self, newshot):
        self.bullet=newshot

    def MoveKeyDown(self, key):
        """Responds to a key-down event and moves accordingly"""
        if (key == pygame.K_UP):
            self.y_change += -self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += self.y_dist

    def Fire(self, key):
        global fire_timer
        """Fires a projectile"""
        if (key == pygame.K_SPACE) and fire_timer == True:
            bullet = Bullet((self.rect.x + (self.rect.x/2)), self.rect.y + 13, self.bullet.get_width(), self.bullet.get_height(), self.bullet)
            laser_shot.play()
            all_sprites_list.remove(player)
            all_sprites_list.add(bullet)
            all_sprites_list.add(player)
            fire_timer = False

    def MoveKeyUp(self, key):
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_UP):
            self.y_change += self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += -self.y_dist

    def getRects(self):
        ptop = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, (self.rect.height/2))
        pmid = pygame.Rect(self.rect.x, (self.rect.y + (self.rect.height/3)), self.rect.width, (self.rect.height/3))
        pbottom = pygame.Rect(self.rect.x, (self.rect.y + (self.rect.height/2)), self.rect.width, (self.rect.height/2))
        return(ptop,pmid,pbottom)

    def update(self):
        """
        Moves the paddle while ensuring it stays in bounds
        """
        # Moves it relative to its current location.
        self.rect.move_ip(0, self.y_change)
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

        # If the paddle moves off the screen, put it back on.
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > window_height - self.height:
            self.rect.y = window_height - self.height
class Enemy(Entity):

    def __init__(self, x, y, width, height, sprite):
        super(Enemy, self).__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 3
        self.sprite = sprite

    def update(self):
        global player_lives
        global player_score
        global you_lose
        global lose_sound
        global piercing
        self.rect.x -= self.speed
        screen.blit(self.sprite, (self.rect.x, self.rect.y))
        width = 0 - self.sprite.get_width()
        if self.rect.x < width:
            all_sprites_list.remove(self)
            player_score -= 100
        for bullet in all_sprites_list:
            if isinstance(bullet, Bullet):
                if self.rect.colliderect(bullet.rect):
                    all_sprites_list.remove(self)
                    if piercing == False:
                        all_sprites_list.remove(bullet)
                    player_score += 100
                    enemy_explosion.play()
        if self.rect.colliderect(player.rect):
            player_lives -= 1
            if player_lives == 0:
                lose_sound = True
                you_lose = True
            else:
                all_sprites_list.remove(self)

class Rapidfire(Entity):

    def __init__(self, x, y, width, height, sprite):
        super(Rapidfire, self).__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 8
        self.sprite = sprite

    def setspeed(self):
        self.speed = 8

    def update(self):
        global piercing
        self.rect.x -= self.speed
        screen.blit(self.sprite, (self.rect.x, self.rect.y))
        width = 0 - self.sprite.get_width()
        if self.rect.x < width:
            all_sprites_list.remove(self)
        if self.rect.colliderect(player.rect):
            player.changeshot(pygame.image.load('widelaser.png'))
            self.speed = 5
            piercing = True
            pygame.time.set_timer(pygame.USEREVENT + 3, 5000)
            all_sprites_list.remove(self)



class Button:

    def __init__(self, x, y, height, width, color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


    def write(self, textcolor, script, fonttype, size):
        text = pygame.font.SysFont(fonttype, size)
        textSurfaceObj = text.render(script, True, textcolor)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (((self.width / 2) + self.x), ((self.height / 2) + self.y))
        screen.blit(textSurfaceObj, textRectObj)

    def click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos[0], mouse_pos[1])

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

enemysprite = pygame.image.load('covenantship.png')
ship = pygame.image.load('ship.png')
backgroundimage = pygame.image.load('space.png')
titleimage = pygame.image.load('title.png')
powerupsprite = pygame.image.load('widesprite.png')

enemy_explosion = pygame.mixer.Sound('explosion.wav')
enemy_explosion.set_volume(5)

laser_shot = pygame.mixer.Sound('grifle01.wav')
laser_shot.set_volume(5)


window_width = 700
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Asteroid")

clock = pygame.time.Clock()

scoreboard = Button(0,0,400,700, (0,0,0))
player = Player(20, window_height / 2, ship.get_width(), ship.get_height(), ship, laser)

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)
enemy_spawn_rate = 4000
powerup_spawn_rate = 15000

pygame.mixer.music.load('Halo.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.time.set_timer(pygame.USEREVENT +1, enemy_spawn_rate)
pygame.time.set_timer(pygame.USEREVENT +4, powerup_spawn_rate)
pygame.time.set_timer(pygame.USEREVENT +2, fire_rate)

while True:
    if play == True:
        if you_lose == True:

            if lose_sound == True:
                pygame.mixer.music.load('lose.mp3')
                pygame.mixer.music.play(-1, 0.0)
                lose_sound = False

            all_sprites_list.remove(player)
            enemy_spawn_rate = 100000000000000000000


            try:
                with open("scores.txt", "r") as high_scores:
                    current_scores = high_scores.read().split("\n")
            except FileNotFoundError:
                with open("scores.txt", "w") as high_scores:
                    high_scores.write("0\n0\n0\n0\n0\n0\n0\n0\n0\n0")
                with open("scores.txt", "r") as high_scores:
                    current_scores = high_scores.read().split("\n")
            for score in range(len(current_scores)):
                if int(player_score) >= int(current_scores[score]):
                    player_score, current_scores[score] = str(current_scores[score]), str(player_score)
                    break
            with open("scores.txt", "w") as high_scores:
                high_scores.write("\n".join([str(score) for score in current_scores]))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()



            string = ("High Scores " + " ".join(current_scores) + " press Escape to quit")

            scoreboard.draw()
            scoreboard.write((255, 255, 255), string, 'Arial', 15)

        if you_lose == False:
            # Event processing here
            screen.blit(backgroundimage, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    player.MoveKeyDown(event.key)
                    player.Fire(event.key)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    player.MoveKeyUp(event.key)
                elif event.type == pygame.USEREVENT + 2:
                    fire_timer = True
                elif event.type == pygame.USEREVENT + 3:
                    player.changeshot(pygame.image.load('laser.png'))
                    piercing = False
                elif event.type == pygame.USEREVENT + 1:
                    ey = random.randint(0, window_height-enemysprite.get_height())
                    enemy = Enemy(window_width + enemysprite.get_width(), ey, enemysprite.get_width(), enemysprite.get_height(), enemysprite)
                    all_sprites_list.add(enemy)
                    if not enemy_spawn_rate <= 300:
                        enemy_spawn_rate -= 100
                        pygame.time.set_timer(pygame.USEREVENT + 1, enemy_spawn_rate)
                elif event.type == pygame.USEREVENT + 4:
                    py = random.randint(0, window_height-powerupsprite.get_height())
                    powerup = Rapidfire(window_width + powerupsprite.get_width(), py, powerupsprite.get_width(), powerupsprite.get_height(), powerupsprite)
                    all_sprites_list.add(powerup)

            score_string = ("Lives: "+ str(player_lives) + "    Score: " + str(player_score))
            score = pygame.font.SysFont('arial', 40)
            score1SurfaceObj = score.render(score_string, True, (0,0,204))
            score1RectObj = score1SurfaceObj.get_rect()
            score1RectObj.center = (350, 50)
            screen.blit(score1SurfaceObj, score1RectObj)


            all_sprites_list.update()
    if play == False:
        screen.blit(titleimage, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    play = True

    pygame.display.flip()

    clock.tick(tick)