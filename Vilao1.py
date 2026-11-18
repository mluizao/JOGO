
import os
import pygame
import math


class Vilao1:

    def __init__(self, pasta_imagens, x=850, y=160):

        self.pasta = os.path.join(
            pasta_imagens,
            "vilao"
        )

        self.x = float(x)
        self.y = float(y)

        self.largura = 85
        self.altura = 85

        self.vida_maxima = 100
        self.vida = 100

        self.velocidade = 2.0

        self.ativo = True
        self.estado = "voando"

        self.animacoes = {
            "voando": self.carregar_frames("voando"),
            "ataque": self.carregar_frames("ataque"),
            "papel": self.carregar_frames("papel"),
            "atingido": self.carregar_frames("atingido")
        }

        self.frame = 0
        self.contador_animacao = 0
        self.velocidade_animacao = 7

        self.tempo_ataque = 0
        self.intervalo_ataque = 110

        self.tempo_invulneravel = 0

        self.papeis = []

        self.tempo_derrota = 0

    # ==========================================
    # CARREGAR ANIMAÇÕES
    # ==========================================

    def carregar_frames(self, pasta):

        caminho = os.path.join(
            self.pasta,
            pasta
        )

        imagens = []

        if not os.path.isdir(caminho):
            print("Pasta não encontrada:", caminho)
            return imagens

        arquivos = sorted(
            arquivo
            for arquivo in os.listdir(caminho)
            if arquivo.lower().endswith(".png")
        )

        for arquivo in arquivos:

            imagem = pygame.image.load(
                os.path.join(caminho, arquivo)
            ).convert_alpha()

            imagem = pygame.transform.smoothscale(
                imagem,
                (self.largura, self.altura)
            )

            imagens.append(imagem)

        if not imagens:
            print("Nenhuma imagem encontrada em:", caminho)

        return imagens

    # ==========================================
    # COLISÃO
    # ==========================================

    def rect(self):

        return pygame.Rect(
            int(self.x + 10),
            int(self.y + 10),
            self.largura - 20,
            self.altura - 20
        )

    # ==========================================
    # RECEBER DANO DA TEIA
    # ==========================================

    def receber_dano(self, dano):

        if not self.ativo:
            return False

        if self.estado == "atingido":
            return False

        if self.tempo_invulneravel > 0:
            return False

        self.vida -= dano

        self.tempo_invulneravel = 20

        if self.vida <= 0:

            self.vida = 0
            self.estado = "atingido"
            self.frame = 0
            self.contador_animacao = 0
            self.tempo_derrota = 0

            self.papeis.clear()

            return True

        return False

    # ==========================================
    # LANÇAR PAPEL NA DIREÇÃO DO JOGADOR
    # ==========================================

    def lancar_papel(self, jogador_x, jogador_y):

        origem_x = self.x
        origem_y = self.y + 40

        destino_x = jogador_x + 30
        destino_y = jogador_y + 30

        dx = destino_x - origem_x
        dy = destino_y - origem_y

        distancia = max(
            math.hypot(dx, dy),
            1
        )

        velocidade_papel = 6

        vx = (dx / distancia) * velocidade_papel
        vy = (dy / distancia) * velocidade_papel

        self.papeis.append({
            "x": origem_x,
            "y": origem_y,
            "vx": vx,
            "vy": vy
        })

    # ==========================================
    # ATUALIZAR
    # ==========================================

    def atualizar(
        self,
        velocidade_cenario,
        deslocamento_camera,
        jogador_x,
        jogador_y
    ):

        if not self.ativo:
            return

        if self.tempo_invulneravel > 0:
            self.tempo_invulneravel -= 1

        # --------------------------------------
        # SE ESTIVER DERROTADO
        # --------------------------------------

        if self.estado == "atingido":

            self.contador_animacao += 1
            self.tempo_derrota += 1

            if self.contador_animacao >= self.velocidade_animacao:

                self.contador_animacao = 0
                self.frame += 1

            if self.tempo_derrota >= 70:
                self.ativo = False

            return

        # --------------------------------------
        # APROXIMAÇÃO DO JOGADOR
        # --------------------------------------

        # Acompanha o deslocamento da cidade.
        self.x -= (
            velocidade_cenario
            + deslocamento_camera
        )

        # Mantém o vilão diante do jogador.
        distancia_desejada = jogador_x + 155

        if self.x > distancia_desejada:

            self.x -= min(
                self.velocidade,
                self.x - distancia_desejada
            )

        elif self.x < distancia_desejada:

            self.x += min(
                1.2,
                distancia_desejada - self.x
            )

        # Acompanha a altura do personagem.
        altura_desejada = jogador_y - 35

        altura_desejada = max(
            65,
            min(altura_desejada, 250)
        )

        if self.y < altura_desejada:
            self.y += 1.2

        elif self.y > altura_desejada:
            self.y -= 1.2

        # --------------------------------------
        # ANIMAÇÃO
        # --------------------------------------

        self.contador_animacao += 1

        if self.contador_animacao >= self.velocidade_animacao:

            self.contador_animacao = 0

            imagens = self.animacoes[self.estado]

            if imagens:

                self.frame += 1

                if self.estado == "ataque":

                    if self.frame >= len(imagens):

                        self.estado = "voando"
                        self.frame = 0

                else:

                    self.frame %= len(imagens)

        # --------------------------------------
        # ATAQUE
        # --------------------------------------

        self.tempo_ataque += 1

        if (
            self.tempo_ataque >= self.intervalo_ataque
            and self.x > jogador_x + 65
        ):

            self.lancar_papel(
                jogador_x,
                jogador_y
            )

            self.tempo_ataque = 0

            if self.animacoes["ataque"]:

                self.estado = "ataque"
                self.frame = 0

        # --------------------------------------
        # MOVIMENTAR PAPÉIS
        # --------------------------------------

        for papel in self.papeis:

            papel["x"] += papel["vx"]
            papel["y"] += papel["vy"]

        self.papeis = [
            papel
            for papel in self.papeis
            if (
                -40 < papel["x"] < 840
                and -40 < papel["y"] < 540
            )
        ]

    # ==========================================
    # DESENHAR
    # ==========================================

    def desenhar(self, tela):

        if not self.ativo:
            return

        imagens = self.animacoes.get(
            self.estado,
            []
        )

        if imagens:

            indice = min(
                self.frame,
                len(imagens) - 1
            )

            imagem = imagens[indice]

            imagem = pygame.transform.flip(
                imagem,
                True,
                False
            )

            # Pisca quando recebe dano.
            if (
                self.tempo_invulneravel > 0
                and self.tempo_invulneravel % 4 < 2
            ):
                imagem = imagem.copy()
                imagem.set_alpha(100)

            tela.blit(
                imagem,
                (int(self.x), int(self.y))
            )

        else:

            pygame.draw.rect(
                tela,
                (130, 20, 150),
                (
                    int(self.x),
                    int(self.y),
                    self.largura,
                    self.altura
                )
            )

        # --------------------------------------
        # DESENHAR PAPÉIS
        # --------------------------------------

        imagens_papel = self.animacoes["papel"]

        for papel in self.papeis:

            if imagens_papel:

                indice = (
                    pygame.time.get_ticks() // 100
                ) % len(imagens_papel)

                imagem = pygame.transform.smoothscale(
                    imagens_papel[indice],
                    (30, 22)
                )

                tela.blit(
                    imagem,
                    (
                        int(papel["x"]),
                        int(papel["y"])
                    )
                )

            else:

                pygame.draw.rect(
                    tela,
                    (245, 245, 220),
                    (
                        int(papel["x"]),
                        int(papel["y"]),
                        25,
                        15
                    )
                )
