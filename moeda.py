import pygame


class Moeda:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 30
        self.altura = 30
        self.coletada = False

    def mover(self, velocidade):
        self.x -= velocidade

    def desenhar(self, tela):
        centro_x = int(self.x + 15)
        centro_y = int(self.y + 15)

        pygame.draw.circle(
            tela,
            (255, 215, 0),
            (centro_x, centro_y),
            15
        )

        pygame.draw.circle(
            tela,
            (255, 255, 255),
            (centro_x - 5, centro_y - 5),
            4
        )

    def rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

    def coletar(self):
        self.coletada = True

    def saiu_da_tela(self):
        return self.x <= -30