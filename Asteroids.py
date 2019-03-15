import pygame
import sys
import random

background = (0, 0, 0)
entity_color = (255, 255, 255)

tick = 60

player_lives = 3
player_score = 0

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
        self.speed = 6
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

    def MoveKeyDown(self, key):
        """Responds to a key-down event and moves accordingly"""
        if (key == pygame.K_UP):
            self.y_change += -self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += self.y_dist

    def Fire(self, key):
        """Fires a projectile"""
        if (key == pygame.K_SPACE):
            bullet = Bullet(self.rect.x, self.rect.y, self.bullet.get_width(), self.bullet.get_height(), self.bullet)
            all_sprites_list.add(bullet)

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
        self.speed = 6
        self.sprite = sprite
        self.player_lives = 3

    def update(self):
        global player_lives
        self.rect.x -= self.speed
        screen.blit(self.sprite, (self.rect.x, self.rect.y))
        width = 0 - self.sprite.get_width()
        if self.rect.x < width:
            all_sprites_list.remove(self)
        for bullet in all_sprites_list:
            if isinstance(bullet, Bullet):
                if self.rect.colliderect(bullet.rect):
                    all_sprites_list.remove(self)
                    all_sprites_list.remove(bullet)
        if self.rect.colliderect(player.rect):
            player_lives -= 1
            if player_lives == 0:
                pygame.quit()
                sys.exit()
            else:
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


pygame.init()

enemysprite = pygame.image.load('covenantship.png')
ship = pygame.image.load('ship.png')
laser = pygame.image.load('laser.png')
backgroundimage = pygame.image.load('halospace2.png')


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

pygame.mixer.music.load('Halo.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.time.set_timer(pygame.USEREVENT +1, enemy_spawn_rate)
while True:
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
            player.MoveKeyUp(event.key)
        elif event.type == pygame.USEREVENT + 1:
            ey = random.randint(0, window_height-enemysprite.get_height())
            enemy = Enemy(window_width + 200, ey, enemysprite.get_width(), enemysprite.get_height(), enemysprite)
            all_sprites_list.add(enemy)

    all_sprites_list.update()


    pygame.display.flip()

    clock.tick(tick)