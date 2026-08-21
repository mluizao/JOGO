import pygame
import random

from player import Player
from obstaculo import Obstaculo
from bloco import Bloco
from moeda import Moeda


class Jogo:

    def __init__(
        self,
        player_img,
        obstaculo_img,
        bloco_img
    ):
        self.player_img = player_img
        self.obstaculo_img = obstaculo_img
        self.bloco_img = bloco_img

        self.player = Player(player_img)

        self.obstaculos = []
        self.blocos = []
        self.moedas = []

        self.moedas_coletadas = 0
        self.pontos = 0

        self.fundo_x = 0
        self.velocidade_base = 6

        self.game_over = False

    def reiniciar(self):

        self.player = Player(self.player_img)

        self.obstaculos = []
        self.blocos = []
        self.moedas = []

        self.moedas_coletadas = 0
        self.pontos = 0

        self.fundo_x = 0

        self.game_over = False

    def atualizar_player(self, teclas):

        self.player.pular(teclas)
        self.player.atualizar()

    def mover_fundo(self):

        self.fundo_x -= 2

        if self.fundo_x <= -800:
            self.fundo_x = 0

    def calcular_velocidade(self):

        return (
            self.velocidade_base
            + (self.pontos / 1000) * 0.5
        )

    def criar_obstaculo(self):

        if (
            len(self.obstaculos) == 0
            or self.obstaculos[-1].x < 450
        ):

            self.obstaculos.append(
                Obstaculo(
                    self.obstaculo_img,
                    800,
                    405
                )
            )

    def criar_blocos(self):

        if len(self.blocos) != 0:
            return

        if (
            len(self.obstaculos) > 0
            and self.obstaculos[-1].x < 500
        ):

            if random.randint(0, 100) < 25:

                quantidade = random.randint(3, 5)

                for i in range(quantidade):

                    x = 800 + (i * 65)
                    y = 395 - (i * 30)

                    self.blocos.append(
                        Bloco(
                            self.bloco_img,
                            x,
                            y
                        )
                    )

    def criar_moedas(self):

        if (
            len(self.moedas) != 0
            and self.moedas[-1].x >= 550
        ):
            return

        quantidade_moedas = random.randint(2, 3)

        alturas = [
            280,
            230,
            180
        ]

        for i in range(quantidade_moedas):

            x = 850 + (i * 60)

            tentativas = 0
            moeda_criada = False

            while (
                tentativas < 20
                and not moeda_criada
            ):

                y = random.choice(alturas)

                moeda = Moeda(x, y)

                pode_criar = True

                for obstaculo in self.obstaculos:

                    obstaculo_rect = pygame.Rect(
                        obstaculo.x - 100,
                        obstaculo.y - 50,
                        150,
                        100
                    )

                    if moeda.rect().colliderect(
                        obstaculo_rect
                    ):
                        pode_criar = False
                        break

                if pode_criar:

                    for bloco in self.blocos:

                        bloco_rect = pygame.Rect(
                            bloco.x - 20,
                            bloco.y - 20,
                            100,
                            60
                        )

                        if moeda.rect().colliderect(
                            bloco_rect
                        ):
                            pode_criar = False
                            break

                if pode_criar:

                    self.moedas.append(moeda)
                    moeda_criada = True

                tentativas += 1

    def mover_objetos(self):

        velocidade = self.calcular_velocidade()

        for obstaculo in self.obstaculos:
            obstaculo.mover(velocidade)

        for bloco in self.blocos:
            bloco.mover(velocidade)

        for moeda in self.moedas:
            moeda.mover(velocidade)

    def remover_objetos(self):

        self.obstaculos = [
            obstaculo
            for obstaculo in self.obstaculos
            if not obstaculo.saiu_da_tela()
        ]

        self.blocos = [
            bloco
            for bloco in self.blocos
            if not bloco.saiu_da_tela()
        ]

        self.moedas = [
            moeda
            for moeda in self.moedas
            if not moeda.saiu_da_tela()
            and not moeda.coletada
        ]

    def verificar_moedas(self):

        player_rect = self.player.rect()

        for moeda in self.moedas:

            if player_rect.colliderect(
                moeda.rect()
            ):

                moeda.coletar()

                self.moedas_coletadas += 1
                self.pontos += 25

                break

    def verificar_obstaculos(self):

        player_rect = self.player.rect()

        for obstaculo in self.obstaculos:

            if player_rect.colliderect(
                obstaculo.rect()
            ):

                self.game_over = True

                return

    def verificar_blocos(self, player_y_anterior):

        player_rect = self.player.rect()

        for bloco in self.blocos:

            bloco_rect = bloco.rect()

            if player_rect.colliderect(
                bloco_rect
            ):

                if (
                    self.player.vel_y > 0
                    and player_y_anterior + 60
                    <= bloco_rect.top + 15
                ):

                    self.player.y = (
                        bloco_rect.top - 60
                    )

                    self.player.vel_y = 0
                    self.player.no_chao = True

    def atualizar(self, teclas):

        if self.game_over:
            return

        player_y_anterior = self.player.y

        self.mover_fundo()

        self.atualizar_player(teclas)

        self.criar_obstaculo()

        self.criar_blocos()

        self.criar_moedas()

        self.mover_objetos()

        self.remover_objetos()

        self.verificar_moedas()

        self.verificar_obstaculos()

        if self.game_over:
            return

        self.verificar_blocos(
            player_y_anterior
        )

        self.pontos += 1

    def desenhar_fundo(self, tela, fundo_img):

        tela.blit(
            fundo_img,
            (self.fundo_x, 0)
        )

        tela.blit(
            fundo_img,
            (self.fundo_x + 800, 0)
        )

    def desenhar_objetos(self, tela):

        self.player.desenhar(tela)

        for obstaculo in self.obstaculos:
            obstaculo.desenhar(tela)

        for bloco in self.blocos:
            bloco.desenhar(tela)

        for moeda in self.moedas:
            moeda.desenhar(tela)

    def desenhar_pontuacao(self, tela, fonte):

        texto = fonte.render(
            f"Pontos: {self.pontos}   "
            f"Moedas: {self.moedas_coletadas}",
            True,
            (255, 255, 255)
        )

        tela.blit(
            texto,
            (10, 10)
        )

    def desenhar(
        self,
        tela,
        fundo_img,
        fonte
    ):

        self.desenhar_fundo(
            tela,
            fundo_img
        )

        self.desenhar_objetos(
            tela
        )

        self.desenhar_pontuacao(
            tela,
            fonte
        )