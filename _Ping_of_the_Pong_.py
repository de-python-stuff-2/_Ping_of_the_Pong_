from pygame import *
from time import time as timer
from random import *

# Game setup
game = True
finished = False
clock = time.Clock()
FPS = 60
font.init()

# Window setup
win_width = 900
win_height = 700
window = display.set_mode((win_width, win_height + 50))
display.set_caption("_Ping_of_the_Pong_")
#EXTRA...score/points
p1_points = 0

p2_points = 0

# Load and scale background
background = transform.scale(image.load("pong.png"), (win_width, win_height + 65))
style = font.SysFont('comicsansms', 24)

# Sprite base class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.original_image = image.load(player_image).convert_alpha()
        self.image = transform.scale(self.original_image, (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Paddle (Player) class
class Player(GameSprite):
    def update_P1(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

    def update_P2(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

# Ball class with spinning effect
class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
        self.dx = 4  # x velocity
        self.dy = 4  # y velocity
        self.angle = 0  # rotation angle

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= win_height:
            self.dy *= -1
        
        if sprite.collide_rect(p1, ball) or sprite.collide_rect(p2, ball):
            self.dx *= -1
              
        

             

        # Spin effect (rotate image each frame)
        self.angle += 5
        self.image = transform.rotate(transform.scale(self.original_image, (36, 35)), self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

# Instantiate objects
p1 = Player('P1.png', 30, 200, 20, 16, 149)
p2 = Player('P2.png', win_width - 50, 200, 20, 16, 149)
ball = Ball('pong_ball.png', win_width // 2, win_height // 2, 4, 36, 35)

speed_x = 3
speed_y = 3



# Main game loop
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finished:
        window.blit(background, (0, 0))

        #text stuff
        text_p1 = style.render("Player 1 you suck! :)", 1, (0, 255, 0))
        
        text_p2 = style.render("Player 2 you suck! :)", 1, (255, 0, 0))

        

        # Update game objects
        p1.update_P1()
        p2.update_P2()
        ball.update()

        # Draw all sprites
        p1.reset()
        p2.reset()
        ball.reset()

        #Ball movement(yez)
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        


        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1

        if sprite.collide_rect(p1, ball) or sprite.collide_rect(p2, ball):
            speed_x *= -1

        if ball.rect.x < -1:
            finished = True    
            window.blit(text_p2, (150, 350))

        if ball.rect.x > win_width:
            finished = True    
            window.blit(text_p1, (550, 350))    
        
        display.update()
        clock.tick(FPS)
