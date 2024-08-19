import pygame
from random import randint
from numpy import random

class Player(pygame.sprite.Sprite):
    """This is a class to handle all the player variables and methods"""

    def __init__(self):
        super().__init__()  # Initializes the parent class __init__ method

        amogus_walk_1 = pygame.image.load(
            'graphics/player/amogus1.png').convert_alpha()

        amogus_walk_2 = pygame.image.load(
            'graphics/player/amogus2.png').convert_alpha()

        amogus_walk_3 = pygame.image.load(
            'graphics/player/amogus3.png').convert_alpha()

        amogus_walk_4 = pygame.image.load(
            'graphics/player/amogus4.png').convert_alpha()

        amogus_walk_5 = pygame.image.load(
            'graphics/player/amogus5.png').convert_alpha()

        amogus_walk_6 = pygame.image.load(
            'graphics/player/amogus6.png').convert_alpha()

        self.amogus_walk = [ amogus_walk_1, amogus_walk_2, amogus_walk_3, amogus_walk_4, amogus_walk_5, amogus_walk_6 ]
        self.amogus_index = 0  # The number used to select between the sprites
        self.amogus_jump = pygame.image.load('graphics/player/amogus_jump.png')

        self.image = self.amogus_walk[self.amogus_index]
        self.rect = self.image.get_rect(midbottom=(80, 400))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('sound/jump.wav')
        self.down_sound = pygame.mixer.Sound('sound/swoosh.wav')
        self.play_sound_once = True

        increment_this = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 400:
            self.gravity = -20
            self.jump_sound.play()

        if keys[pygame.K_DOWN] and self.rect.bottom < 300:
            self.gravity = +20

            if self.play_sound_once:
                self.down_sound.play()
                self.play_sound_once = False

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 400:
            self.rect.bottom = 400

        if self.rect.bottom == 400:
            self.play_sound_once = True

    def animation(self):
        if self.rect.bottom < 400:
            self.image = self.amogus_jump
        else:
            self.amogus_index += 0.1  # Determines the speed of the animation
            if self.amogus_index >= len(self.amogus_walk):
                self.amogus_index = 0
            self.image = self.amogus_walk[int(self.amogus_index)]

    def update(self):  # Much cleaner than calling each method manually
        self.player_input()
        self.apply_gravity()
        self.animation()
        print(self.rect.bottom)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png')
            fly_2 = pygame.image.load('graphics/fly/fly2.png')
            self.frames = [fly_1, fly_2]
            self.animation_speed = 0.3
            y_pos = 300

        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png')
            snail_2 = pygame.image.load('graphics/snail/snail2.png')
            self.frames = [snail_1, snail_2]
            self.animation_speed = 0.1
            y_pos = 400

        self.animation_index = 0

        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(
            randint(900, 1400), y_pos))

    def animation(self):
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation()
        self.destroy()
        self.rect.x -= 5


def collisions():
    if pygame.sprite.spritecollide(player.sprite, enemy, False):
        enemy.empty()
        return False
    else:
        return True


def display_score():
    """For continiously displaying the score of the game"""
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'{current_time}', False, '#f0f0f0')
    score_rect = score_surf.get_rect(center=(WIDTH/2, 50))

    pygame.draw.rect(screen, '#cc5e1f', score_rect)
    pygame.draw.rect(screen, '#cc5e1f', score_rect, 10)
    screen.blit(score_surf, score_rect)
    return current_time  # Returning it to be able to display as score later on


# Must be executed first.
pygame.init()

# Initial Variables.
WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_active = False
controls_pressed = False

pygame.display.set_caption("Scrongo Run")
font = pygame.font.Font('fonts/Pixeboy.ttf', 50)

clock = pygame.time.Clock()
start_time = 0
score = 0

# Where I create my things.

# Background
sky_surf = pygame.image.load('graphics/sky.png').convert()
sun_surf = pygame.image.load('graphics/sun.png').convert_alpha()
sun_rect = sun_surf.get_rect(midtop=(50, 20))

clouds_surf = pygame.image.load('graphics/clouds.png').convert_alpha()
clouds_rect = clouds_surf.get_rect(midtop=(400, 50))

ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()

controls_surf = font.render("Controls to be added soon", False, (0, 0, 0))
controls_rect = controls_surf.get_rect(center=(WIDTH/2, 100))

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())  # Player Group

enemy = pygame.sprite.Group()

# Intro/Gameover screen
# Reminder : Order matters
char_stand_surf = pygame.image.load('graphics/player/amogus1.png')
char_stand_surf = pygame.transform.rotozoom(char_stand_surf, 10, 2)
char_stand_rect = char_stand_surf.get_rect(center=(WIDTH/2, HEIGHT/2+20))

game_title = font.render("Amogus Run", False, (255, 255, 255))
game_title_rect = game_title.get_rect(center=(WIDTH/2, 50))

game_message = font.render("Press space to start", False, (255, 255, 255))
game_message_rect = game_message.get_rect(center=(WIDTH/2, 400))

# Timers
# +1 is to avoid conflict with pygame reserved events
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)

# Main loop.
running = True
while running:
    # Event loop.
    for event in pygame.event.get():

        # Makes the window quitable.
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if game_active:
            # Quits the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_active = False

            # User events
            if event.type == enemy_timer:
                # Will pick randomly between fly and snail using choice method
                enemy.add(Enemy(random.choice(['fly', 'snail'], p=[0.3, 0.7])))

        else:
            # Game restart logic
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

                if event.key == pygame.K_F1:
                    if controls_pressed is False:
                        controls_pressed = True
                    else:
                        controls_pressed = False

    if game_active:
        # Fills the screen with an RGB or Hex value, should be on top.
        screen.fill('#ea64d3')

        # Background
        screen.blit(sky_surf, (0, 0))
        screen.blit(sun_surf, sun_rect)
        screen.blit(clouds_surf, clouds_rect)
        screen.blit(ground_surf, (0, 370))

        # Player
        player.update()
        player.draw(screen)

        # Enemy
        enemy.update()
        enemy.draw(screen)

        # Collision
        game_active = collisions()  # If it returns False game stops

        # Text
        score = display_score()

    else:
        score_message = font.render(f'Score: {score}', False, (255, 255, 255))
        score_message_rect = score_message.get_rect(center=(WIDTH/2, 120))

        screen.fill('#f0b1ac')
        screen.blit(char_stand_surf, char_stand_rect)
        screen.blit(game_title, game_title_rect)
        screen.blit(game_message, game_message_rect)
        screen.blit(score_message, score_message_rect)

        enemy.empty()

        if controls_pressed is True:
            pygame.draw.rect(screen, (255, 255, 255), controls_rect)
            screen.blit(controls_surf, controls_rect)

    pygame.display.update()
    clock.tick(60)
