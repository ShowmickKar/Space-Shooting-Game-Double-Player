import pygame
import os
from spaceship import Spaceship

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 30)
big_font = pygame.font.SysFont("Comic Sans MS", 70)


WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooting Game")

BACKGROUND = pygame.transform.scale(
    pygame.image.load("./Assets/Background.png"), (WIDTH, HEIGHT)
)

BORDER = ((WIDTH // 2) - 5, 0, 10, HEIGHT)
SPACESHIP_SIZE = 65

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

BULLET_SIZE = 50, 40
bullet_1_img = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load("Assets/Bullet-1.png"), BULLET_SIZE),
    270,
)
bullet_2_img = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load("Assets/Bullet-2.png"), BULLET_SIZE),
    90,
)

FPS = 60
INITIAL_HEALTH = 10
VELOCITY = 7
MAX_BULLETS = 3
BULLET_VELOCITY = 15


def draw(window, left_spaceship, right_spaceship):
    window.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(window, (0, 0, 0), BORDER)
    health_player_1 = myfont.render(
        f"HEALTH: {left_spaceship.getHealth()}", False, (255, 255, 255)
    )
    health_player_2 = myfont.render(
        f"HEALTH: {right_spaceship.getHealth()}", False, (255, 255, 255)
    )
    window.blit(health_player_1, (0, 0))
    window.blit(health_player_2, (WIDTH - 120, 0))
    left_spaceship.draw(window)
    right_spaceship.draw(window)
    pygame.display.update()


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

    while run:
        clock.tick(FPS)
        draw(window, left_spaceship, right_spaceship)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    left_spaceship.shoot()
                if event.key == pygame.K_RCTRL:
                    right_spaceship.shoot()
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
