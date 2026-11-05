import pygame
import random

from player import Player
from obstaculo import Obstaculo
from bloco import Bloco
from moeda import Moeda


class Jogo:

    def __init__(self, player_img, obstaculo_img, bloco_img):
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

        self.camera_x = 0
        self.proximo_obstaculo = 700

        self.game_over = False

    def reiniciar(self):
        self.player = Player(self.player_img)

        self.obstaculos = []
        self.blocos = []
        self.moedas = []

        self.moedas_coletadas = 0
        self.pontos = 0

        self.fundo_x = 0
        self.camera_x = 0
        self.proximo_obstaculo = 700

        self.game_over = False

    def atualizar_player(self, teclas):
        self.player.atualizar(teclas)

        # A câmera acompanha o personagem quando ele
        # chega perto do lado direito da tela.
        if self.player.x > 500:
            deslocamento = self.player.x - 500
            self.player.x = 500
            self.camera_x += deslocamento

            for obstaculo in self.obstaculos:
                obstaculo.x -= deslocamento

            for bloco in self.blocos:
                bloco.x -= deslocamento

            for moeda in self.moedas:
                moeda.x -= deslocamento

    def mover_fundo(self):
        self.fundo_x = 0

    def calcular_velocidade(self):
        return self.velocidade_base + (self.pontos / 1000) * 0.5

    def criar_obstaculo(self):
        if self.camera_x + 800 >= self.proximo_obstaculo:
            self.obstaculos.append(
                Obstaculo(
                    self.obstaculo_img,
                    800,
                    405
                )
            )
            self.proximo_obstaculo += random.randint(350, 500)

    def criar_blocos(self):
        # Mantido desativado durante o teste do movimento.
        pass

    def criar_moedas(self):
        if len(self.moedas) < 3:
            for i in range(3 - len(self.moedas)):
                x = 850 + i * 70
                y = random.choice([250, 290, 320])
                self.moedas.append(Moeda(x, y))

    def mover_objetos(self):
        # Os objetos só se deslocam quando a câmera avança.
        # Não há movimento automático do cenário.
        pass

    def remover_objetos(self):
        self.obstaculos = [
            obj for obj in self.obstaculos
            if obj.x > -150
        ]

        self.blocos = [
            obj for obj in self.blocos
            if obj.x > -150
        ]

        self.moedas = [
            obj for obj in self.moedas
            if obj.x > -100 and not obj.coletada
        ]

    def verificar_moedas(self):
        player_rect = self.player.rect()

        for moeda in self.moedas:
            if player_rect.colliderect(moeda.rect()):
                moeda.coletar()
                self.moedas_coletadas += 1
                self.pontos += 25

    def verificar_obstaculos(self):
        player_rect = self.player.rect()

        for obstaculo in self.obstaculos:
            if player_rect.colliderect(obstaculo.rect()):
                self.game_over = True
                return

    def verificar_blocos(self, player_y_anterior):
        player_rect = self.player.rect()

        for bloco in self.blocos:
            bloco_rect = bloco.rect()

            if player_rect.colliderect(bloco_rect):
                if (
                    self.player.vel_y > 0
                    and player_y_anterior + self.player.altura
                    <= bloco_rect.top + 15
                ):
                    self.player.y = bloco_rect.top - self.player.altura
                    self.player.vel_y = 0
                    self.player.no_chao = True

    def atualizar(self, teclas):
        if self.game_over:
            return

        player_y_anterior = self.player.y

        self.atualizar_player(teclas)

        self.criar_obstaculo()
        self.criar_moedas()

        self.remover_objetos()
        self.verificar_moedas()
        self.verificar_obstaculos()

        if self.game_over:
            return

        self.verificar_blocos(player_y_anterior)

        # Se cair para fora da tela, perde.
        if self.player.y > 500:
            self.game_over = True
            return

        self.pontos += 1

    def desenhar_fundo(self, tela, fundo_img):
        tela.blit(fundo_img, (0, 0))

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
            f"Pontos: {self.pontos}   Moedas: {self.moedas_coletadas}",
            True,
            (255, 255, 255)
        )
        tela.blit(texto, (10, 10))

    def desenhar(self, tela, fundo_img, fonte):
        self.desenhar_fundo(tela, fundo_img)
        self.desenhar_objetos(tela)
        self.desenhar_pontuacao(tela, fonte)