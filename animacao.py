
import math
import pygame


class AnimacaoPlayer:

    def __init__(self):
        self.tempo = 0.0
        self.escala_x = 1.0
        self.escala_y = 1.0
        self.no_chao = True
        self.vel_y = 0.0

    def pousar(self, vel_impacto):
        forca = min(max(vel_impacto, 0) / 15, 1.0)

        if forca < 0.15:
            return

        self.escala_x = 1.0 + 0.30 * forca
        self.escala_y = 1.0 - 0.30 * forca

    def atualizar(self, no_chao, vel_y, velocidade_mundo):
        self.no_chao = no_chao
        self.vel_y = vel_y

        if no_chao:
            self.tempo += 0.18 + velocidade_mundo * 0.05
            alvo_x, alvo_y = 1.0, 1.0
        else:
            esticar = min(abs(vel_y) / 25, 0.25)
            alvo_x = 1.0 - esticar * 0.6
            alvo_y = 1.0 + esticar

        self.escala_x += (alvo_x - self.escala_x) * 0.25
        self.escala_y += (alvo_y - self.escala_y) * 0.25

    def desenhar(
        self,
        tela,
        imagem,
        x,
        y,
        tamanho=60,
        ajuste_pes=0,
        direcao=1
    ):

        # Vira a imagem conforme a direção do jogador.
        imagem = pygame.transform.flip(
            imagem,
            direcao == -1,
            False
        )

        largura = max(1, int(imagem.get_width() * self.escala_x))
        altura = max(1, int(imagem.get_height() * self.escala_y))

        img = pygame.transform.scale(
            imagem,
            (largura, altura)
        )

        if self.no_chao:
            onda = math.sin(self.tempo)
            bob = -abs(onda) * 4

            # A inclinação acompanha a direção do movimento.
            angulo = (-5 + onda * 3) * direcao

        else:
            bob = 0
            angulo = max(
                -10,
                min(10, -self.vel_y * 0.5)
            ) * direcao

        img = pygame.transform.rotate(img, angulo)

        # Mantém o ponto de apoio nos pés.
        rad = math.radians(angulo)

        pivo_x = x + tamanho / 2
        pivo_y = y + tamanho + bob + ajuste_pes

        centro = (
            pivo_x - (altura / 2) * math.sin(rad),
            pivo_y - (altura / 2) * math.cos(rad)
        )

        tela.blit(
            img,
            img.get_rect(center=centro)
        )
