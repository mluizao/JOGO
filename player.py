import pygame


class Player:

    def __init__(self, imagem):

        self.imagem = imagem

        self.x = 100
        self.y = 300

        self.vel_y = 0

        self.gravidade = 0.7

        self.no_chao = True

        self.tempo_pulo = 0

    def pular(self, teclas):

        if teclas[pygame.K_SPACE] and self.no_chao:

            self.vel_y = -15
            self.no_chao = False
            self.tempo_pulo = 0

        if teclas[pygame.K_SPACE] and not self.no_chao:

            if self.tempo_pulo < 10:

                self.vel_y -= 0.5
                self.tempo_pulo += 1

    def atualizar(self):

        self.vel_y += self.gravidade
        self.y += self.vel_y

        self.no_chao = False

        if self.y >= 380:

            self.y = 380
            self.vel_y = 0
            self.no_chao = True

    def desenhar(self, tela):

        tela.blit(self.imagem, (self.x, self.y))

    def rect(self):

        return pygame.Rect(self.x, self.y, 60, 60)