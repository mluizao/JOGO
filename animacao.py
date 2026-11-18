
import os
import glob
import pygame
import math


class AnimacaoPlayer:

    def __init__(self):

        self.tempo = 0.0
        self.indice = 0
        self.estado = "parado"

        self.escala_x = 1.0
        self.escala_y = 1.0

        self.no_chao = True
        self.vel_y = 0.0

        self.velocidade_animacao = 0.12
        self.contador = 0

        self.animacoes = {}

        self.direcao = 1

        self.carregar_sprites()

    # =====================================================
    # CARREGAR AS SPRITES
    # =====================================================

    def carregar_sprites(self):

        pasta_projeto = os.path.dirname(
            os.path.abspath(__file__)
        )

        pasta_player = os.path.join(
            pasta_projeto,
            "assets",
            "imagens",
            "player"
        )

        nomes = [
            "parado",
            "correndo",
            "pulando",
            "caindo",
            "teia",
            "dano"
        ]

        for nome in nomes:

            pasta_animacao = os.path.join(
                pasta_player,
                nome
            )

            arquivos = glob.glob(
                os.path.join(pasta_animacao, "*.png")
            )

            arquivos.sort(
                key=lambda caminho: int(
                    os.path.splitext(
                        os.path.basename(caminho)
                    )[0].split("_")[-1]
                )
            )

            quadros = []

            for arquivo in arquivos:

                imagem = pygame.image.load(
                    arquivo
                ).convert_alpha()

                quadros.append(imagem)

            if quadros:

                self.animacoes[nome] = quadros

                print(
                    f"Animação {nome}: "
                    f"{len(quadros)} sprites carregadas."
                )

            else:

                print(
                    f"ATENÇÃO: nenhuma sprite encontrada em {pasta_animacao}"
                )

        if "parado" not in self.animacoes:

            raise FileNotFoundError(
                "Não encontrei as sprites da pasta "
                "assets/imagens/player/parado"
            )

    # =====================================================
    # ESCOLHER ANIMAÇÃO
    # =====================================================

    def definir_estado(self, novo_estado):

        if novo_estado not in self.animacoes:
            return

        if self.estado != novo_estado:

            self.estado = novo_estado
            self.indice = 0
            self.contador = 0

    # =====================================================
    # POUSAR
    # =====================================================

    def pousar(self, vel_impacto):

        forca = min(
            max(vel_impacto, 0) / 15,
            1.0
        )

        if forca < 0.15:
            return

        self.escala_x = 1.0 + 0.20 * forca
        self.escala_y = 1.0 - 0.20 * forca

    # =====================================================
    # ATUALIZAR ANIMAÇÃO
    # =====================================================

    def atualizar(
        self,
        no_chao,
        vel_y,
        velocidade_mundo,
        movendo=False,
        atacando=False,
        recebendo_dano=False
    ):

        self.no_chao = no_chao
        self.vel_y = vel_y

        # Prioridade das animações.
        if recebendo_dano:

            novo_estado = "dano"

        elif atacando:

            novo_estado = "teia"

        elif not no_chao:

            if vel_y < 0:
                novo_estado = "pulando"
            else:
                novo_estado = "caindo"

        elif movendo:

            novo_estado = "correndo"

        else:

            novo_estado = "parado"

        self.definir_estado(novo_estado)

        # Velocidade de cada animação.
        if self.estado == "parado":
            velocidade = 0.16

        elif self.estado == "correndo":
            velocidade = 0.14

        elif self.estado == "teia":
            velocidade = 0.13

        elif self.estado == "dano":
            velocidade = 0.15

        else:
            velocidade = 0.12

        self.contador += velocidade

        if self.contador >= 1:

            self.indice += 1
            self.contador = 0

            quadros = self.animacoes.get(
                self.estado,
                []
            )

            if quadros:

                if self.estado in ("dano", "teia"):

                    if self.indice >= len(quadros):
                        self.indice = len(quadros) - 1

                else:

                    self.indice %= len(quadros)

        # Recuperar a escala depois do pouso.
        alvo_x = 1.0
        alvo_y = 1.0

        self.escala_x += (
            alvo_x - self.escala_x
        ) * 0.25

        self.escala_y += (
            alvo_y - self.escala_y
        ) * 0.25

    # =====================================================
    # DESENHAR PERSONAGEM
    # =====================================================

    def desenhar(
        self,
        tela,
        imagem=None,
        x=0,
        y=0,
        tamanho=60,
        ajuste_pes=0,
        direcao=1
    ):

        quadros = self.animacoes.get(
            self.estado,
            self.animacoes.get("parado", [])
        )

        if not quadros:
            return

        indice = min(
            self.indice,
            len(quadros) - 1
        )

        imagem_atual = quadros[indice]

        # Virar o personagem conforme a direção.
        if direcao == -1:

            imagem_atual = pygame.transform.flip(
                imagem_atual,
                True,
                False
            )

        # Mantém a proporção da sprite.
        largura_original = imagem_atual.get_width()
        altura_original = imagem_atual.get_height()

        proporcao = largura_original / altura_original

        altura = int(tamanho * 1.25)
        largura = int(altura * proporcao)

        largura = max(1, int(largura * self.escala_x))
        altura = max(1, int(altura * self.escala_y))

        imagem_atual = pygame.transform.scale(
            imagem_atual,
            (largura, altura)
        )

        # Pequeno movimento de respiração quando parado.
        bob = 0

        if self.estado == "parado":

            bob = math.sin(
                pygame.time.get_ticks() * 0.004
            ) * 1.5

        # Posicionar mantendo os pés no mesmo lugar.
        pos_x = x + tamanho / 2 - largura / 2

        pos_y = (
            y + tamanho + ajuste_pes
            - altura
            + bob
        )

        tela.blit(
            imagem_atual,
            (int(pos_x), int(pos_y))
        )
