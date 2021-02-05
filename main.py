import pygame
import os
from spaceship import Spaceship
from pygame import mixer

pygame.init()
pygame.font.init()
mixer.init()
myfont = pygame.font.SysFont("Comic Sans MS", 25)
big_font = pygame.font.SysFont("Comic Sans MS", 70)

# Loads background music
BACKGROUND_MUSIC = mixer.Sound("Assets/04.JUMP IN THE FIRE.wav")
BACKGROUND_MUSIC.play(-1)

# Defines window size
WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooting Game")

BACKGROUND = pygame.transform.scale(
    pygame.image.load("./Assets/Background.png"), (WIDTH, HEIGHT)
)

BORDER = ((WIDTH // 2) - 5, 0, 10, HEIGHT)
SPACESHIP_SIZE = 65

# Loads, resizes and rotates spaceship images
spaceship_1 = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load("Assets/spaceship-1.png"), (SPACESHIP_SIZE, SPACESHIP_SIZE)
    ),
    270,
)

spaceship_2 = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load("Assets/spaceship-2.png"), (SPACESHIP_SIZE, SPACESHIP_SIZE)
    ),
    90,
)

# Defines Bullet Dimentions
BULLET_SIZE = 50, 40

# Loads, resizes and rotates bullet images
bullet_1_img = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load("Assets/Bullet-1.png"), BULLET_SIZE),
    270,
)
bullet_2_img = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load("Assets/Bullet-2.png"), BULLET_SIZE),
    90,
)

FPS = 60  # Game speed
INITIAL_HEALTH = 10
VELOCITY = 7  # Player/ Spaceship speed
MAX_BULLETS = 3  # Maximum number of bullets a player can shoot at a time
BULLET_VELOCITY = 15  # Bullet velocity


""" Main draw function that renders images, background and updates the display """


def draw(window, left_spaceship, right_spaceship):
    window.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(window, (0, 0, 0), BORDER)

    # Loads and displays the remaining health of each player
    health_player_1 = myfont.render(
        f"HEALTH: {left_spaceship.getHealth()}", False, (255, 255, 255)
    )
    health_player_2 = myfont.render(
        f"HEALTH: {right_spaceship.getHealth()}", False, (255, 255, 255)
    )
    window.blit(health_player_1, (0, 0))
    window.blit(health_player_2, (BORDER[0] + 10, 0))

    # Renders images of the spaceships
    left_spaceship.draw(window)
    right_spaceship.draw(window)
    pygame.display.update()


# Displays winning messege and restarts the game
def reset(window, winner):
    pygame.time.delay(500)
    game_over = big_font.render("WINS!", False, (255, 255, 0))
    pygame.display.update()
    if winner == 1:
        window.blit(game_over, (WIDTH // 2 - 320, HEIGHT // 2 - 50))
    else:
        window.blit(game_over, (WIDTH - (WIDTH // 2 - 180), HEIGHT // 2 - 50))
    pygame.display.update()
    pygame.time.delay(1000)
    main(window)


# Main game function that takes player inputs and handles all the game logic
def main(window):
    clock = pygame.time.Clock()
    run = True
    left_spaceship = Spaceship(
        [100, 100],
        SPACESHIP_SIZE,
        "left",
        INITIAL_HEALTH,
        VELOCITY,
        MAX_BULLETS,
        BULLET_SIZE,
        bullet_1_img,
        BULLET_VELOCITY,
        spaceship_1,
        WIDTH,
        HEIGHT,
        BORDER,
    )
    right_spaceship = Spaceship(
        [WIDTH - 100, HEIGHT - 100],
        SPACESHIP_SIZE,
        "right",
        INITIAL_HEALTH,
        VELOCITY,
        MAX_BULLETS,
        BULLET_SIZE,
        bullet_2_img,
        BULLET_VELOCITY,
        spaceship_2,
        WIDTH,
        HEIGHT,
        BORDER,
    )

    # Main game loop
    while run:
        clock.tick(FPS)
        draw(window, left_spaceship, right_spaceship)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # Handles bullet shot
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    left_spaceship.shoot()
                if event.key == pygame.K_RCTRL:
                    right_spaceship.shoot()

        # Takes player input and handles spaceship movement
        navigation_key = pygame.key.get_pressed()
        if navigation_key[pygame.K_w]:
            left_spaceship.moveUp()
        if navigation_key[pygame.K_s]:
            left_spaceship.moveDown()
        if navigation_key[pygame.K_d]:
            left_spaceship.moveRight()
        if navigation_key[pygame.K_a]:
            left_spaceship.moveLeft()

        if navigation_key[pygame.K_UP]:
            right_spaceship.moveUp()
        if navigation_key[pygame.K_DOWN]:
            right_spaceship.moveDown()
        if navigation_key[pygame.K_RIGHT]:
            right_spaceship.moveRight()
        if navigation_key[pygame.K_LEFT]:
            right_spaceship.moveLeft()

        # Detects collision
        if left_spaceship.collision(right_spaceship):
            pygame.mixer.music.load("Assets/Collision.wav")
            pygame.mixer.music.play()
            left_spaceship.healthDecrease()
        if right_spaceship.collision(left_spaceship):
            pygame.mixer.music.load("Assets/Collision.wav")
            pygame.mixer.music.play()
            right_spaceship.healthDecrease()
        if left_spaceship.getHealth() <= 0:
            reset(window, 2)
        if right_spaceship.getHealth() <= 0:
            reset(window, 1)

    pygame.quit()


if __name__ == "__main__":
    main(window)