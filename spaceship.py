import pygame
from bullet import Bullet


class Spaceship:
    def __init__(
        self,
        position,
        size,
        placement,
        initial_health,
        velocity,
        max_bullets,
        bullet_size,
        bullet_img,
        bullet_velocity,
        img,
        WIDTH,
        HEIGHT,
        border,
    ):

        self.__size = size
        self.__placement = placement
        self.__img = img
        self.__health = initial_health
        self.__velocity = velocity
        self.__position = pygame.Rect(position[0], position[1], size, size)
        self.__border = border
        self.__max_bullets = max_bullets
        self.bullets = []
        self.__bullet_size = bullet_size
        self.__bullet_img = bullet_img
        self.__bullet_velocity = bullet_velocity
        self.window_width = WIDTH
        self.window_height = HEIGHT

    def moveUp(self):
        if self.__position.y - self.__velocity >= 0:
            self.__position.y -= self.__velocity

    def moveDown(self):
        if self.__position.y + self.__velocity + self.__size <= self.window_height:
            self.__position.y += self.__velocity

    def moveRight(self):
        if self.__placement == "right":
            if self.__position.x + self.__velocity + self.__size <= self.window_width:
                self.__position.x += self.__velocity
        else:
            if self.__position.x + self.__velocity + self.__size <= self.__border[0]:
                self.__position.x += self.__velocity

    def moveLeft(self):
        if self.__placement == "right":
            if (
                self.__position.x - self.__velocity
                >= self.__border[0] + self.__border[2]
            ):
                self.__position.x -= self.__velocity
        else:
            if self.__position.x - self.__velocity >= 0:
                self.__position.x -= self.__velocity

    def shoot(self):
        if len(self.bullets) < self.__max_bullets:
            if self.__placement == "right":
                self.bullets.append(
                    Bullet(
                        [self.__position.x, self.__position.y + 10],
                        self.__bullet_size,
                        -1,
                        self.__bullet_velocity,
                        self.__bullet_img,
                        self.window_width,
                        self.window_height,
                    )
                )
            else:
                self.bullets.append(
                    Bullet(
                        [self.__position.x, self.__position.y + 10],
                        self.__bullet_size,
                        1,
                        self.__bullet_velocity,
                        self.__bullet_img,
                        self.window_width,
                        self.window_height,
                    )
                )

    def getPosition(self):
        return self.__position

    def getHealth(self):
        return self.__health

    def healthDecrease(self):
        self.__health -= 1

    def collision(self, opponent):
        for bullet in opponent.bullets:
            if self.__position.colliderect(bullet.getPosition()):
                opponent.bullets.remove(bullet)
                return True

    def draw(self, window):
        window.blit(self.__img, (self.__position.x, self.__position.y))
        for bullet in self.bullets:
            flag = bullet.move()
            if flag == False:
                self.bullets.remove(bullet)
            bullet.draw(window)