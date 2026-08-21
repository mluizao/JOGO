import pygame


class Bloco:

    def __init__(self, imagem, x, y):
        self.imagem = imagem
        self.x = x
        self.y = y
        self.largura = 60
        self.altura = 20

    def mover(self, velocidade):
        self.x -= velocidade

    def desenhar(self, tela):
        tela.blit(
            self.imagem,
            (self.x, self.y)
        )

    def rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

    def saiu_da_tela(self):
        return self.x <= -60