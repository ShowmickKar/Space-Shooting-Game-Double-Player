import pygame


class Bullet:
    def __init__(self, position, size, direction, velocity, img, WIDTH, HEIGHT):
        self.__position = pygame.Rect(position[0], position[1], size[0], size[1])
        self.__size = size
        self.__direction = direction
        self.__velocity = velocity
        self.__img = img
        self.window_width = WIDTH
        self.window_height = HEIGHT

    def getPosition(self):
        return self.__position

    def move(self):
        self.__position.x += self.__velocity * self.__direction
        if self.__direction == 1 and self.__position.x >= self.window_width:
            return False
        if self.__direction == -1 and self.__position.x <= 0:
            return False

    def draw(self, window):
        window.blit(self.__img, (self.__position.x, self.__position.y))