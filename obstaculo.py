
import pygame


class Caixa:
    def __init__(self, imagem, x, y):
        self.imagem = imagem
        self.x = float(x)
        self.y = float(y)
        self.largura = imagem.get_width()
        self.altura = imagem.get_height()
        self.ativa = True

    def mover(self, velocidade):
        self.x -= velocidade

    def rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.largura,
            self.altura
        )

    def desenhar(self, tela):
        if self.ativa:
            tela.blit(self.imagem, (int(self.x), int(self.y)))


class Teia:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.velocidade = 10
        self.largura = 30
        self.altura = 8

    def mover(self):
        self.x += self.velocidade

    def rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.largura,
            self.altura
        )

    def desenhar(self, tela):
        pygame.draw.line(
            tela,
            (230, 230, 255),
            (int(self.x), int(self.y + 4)),
            (int(self.x + self.largura), int(self.y + 4)),
            4
        )

    def saiu_da_tela(self):
        return self.x > 800
