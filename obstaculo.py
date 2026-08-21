import pygame


class Obstaculo:

    def __init__(self, imagem, x, y):
        self.imagem = imagem
        self.x = x
        self.y = y
        self.largura = 50
        self.altura = 50

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
        return self.x <= -50