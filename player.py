import pygame


class Player:

    def __init__(self, imagem):
        self.imagem = imagem

        self.x = 100
        self.y = 370

        self.largura = 60
        self.altura = 60

        self.velocidade = 5
        self.vel_y = 0
        self.gravidade = 0.7
        self.forca_pulo = -15

        self.no_chao = True
        self.tempo_pulo = 0

    def pular(self, teclas):

        if teclas[pygame.K_SPACE] and self.no_chao:
            self.vel_y = self.forca_pulo
            self.no_chao = False
            self.tempo_pulo = 0

        if teclas[pygame.K_SPACE] and not self.no_chao:
            if self.tempo_pulo < 10:
                self.vel_y -= 0.5
                self.tempo_pulo += 1

    def atualizar(self, teclas):

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.velocidade

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.velocidade

        if self.x < 0:
            self.x = 0

        self.pular(teclas)

        self.vel_y += self.gravidade
        self.y += self.vel_y

        if self.y >= 370:
            self.y = 370
            self.vel_y = 0
            self.no_chao = True

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

    def rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )