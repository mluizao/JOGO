import pygame
import cv2
import numpy as np


def converter_mouse(pos, janela, largura, altura):

    largura_janela, altura_janela = janela.get_size()

    escala_x = largura_janela / largura
    escala_y = altura_janela / altura

    escala = min(escala_x, escala_y)

    nova_largura = int(largura * escala)
    nova_altura = int(altura * escala)

    offset_x = (largura_janela - nova_largura) // 2
    offset_y = (altura_janela - nova_altura) // 2

    mouse_x = (pos[0] - offset_x) / escala
    mouse_y = (pos[1] - offset_y) / escala

    return mouse_x, mouse_y


def mostrar_tela(
    tela,
    janela,
    largura,
    altura,
    preto
):

    largura_janela, altura_janela = janela.get_size()

    escala_x = largura_janela / largura
    escala_y = altura_janela / altura

    escala = min(escala_x, escala_y)

    nova_largura = int(largura * escala)
    nova_altura = int(altura * escala)

    tela_redimensionada = pygame.transform.scale(
        tela,
        (nova_largura, nova_altura)
    )

    janela.fill(preto)

    pos_x = (largura_janela - nova_largura) // 2
    pos_y = (altura_janela - nova_altura) // 2

    janela.blit(
        tela_redimensionada,
        (pos_x, pos_y)
    )


def alternar_tela_cheia(
    janela,
    tela_cheia,
    largura,
    altura
):

    tela_cheia = not tela_cheia

    if tela_cheia:

        janela = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN
        )

    else:

        janela = pygame.display.set_mode(
            (largura, altura),
            pygame.RESIZABLE
        )

    return janela, tela_cheia


class RankingCortina:

    def __init__(self):

        self.largura = 800
        self.altura = 500

        self.fonte = pygame.font.SysFont(
            None,
            32
        )

        self.fonte_grande = pygame.font.SysFont(
            None,
            55
        )

        try:

            self.fonte_nomes = pygame.font.Font(
                "assets/imagens/BerkshireSwash-Regular.ttf",
                34
            )

        except Exception as erro:

            print(
                "ERRO AO CARREGAR FONTE:",
                erro
            )

            self.fonte_nomes = pygame.font.SysFont(
                "serif",
                34,
                bold=True
            )

        self.video = None
        self.video_terminou = False
        self.frame_atual = None

        self.podio = None
        self.fundo_resto = None

        self.mostrar_resto = False

        self.botao_resto = pygame.Rect(
            320,
            435,
            160,
            40
        )

        self.botao_voltar = pygame.Rect(
            180,
            435,
            180,
            40
        )

        self.botao_inicio = pygame.Rect(
            490,
            435,
            180,
            40
        )

        self.carregar_imagens()
        self.carregar_video()


    def carregar_imagens(self):

        try:

            self.podio = pygame.image.load(
                "assets/imagens/podio.png"
            ).convert_alpha()

            self.podio = pygame.transform.scale(
                self.podio,
                (800, 500)
            )

        except Exception as erro:

            print(
                "ERRO AO CARREGAR PODIO:",
                erro
            )

            self.podio = pygame.Surface(
                (800, 500)
            )

            self.podio.fill(
                (120, 20, 20)
            )


        try:

            self.fundo_resto = pygame.image.load(
                "assets/imagens/fundo_resto.png"
            ).convert()

            self.fundo_resto = pygame.transform.scale(
                self.fundo_resto,
                (800, 500)
            )

        except Exception as erro:

            print(
                "ERRO AO CARREGAR FUNDO RESTO:",
                erro
            )

            self.fundo_resto = pygame.Surface(
                (800, 500)
            )

            self.fundo_resto.fill(
                (255, 180, 220)
            )


    def carregar_video(self):

        try:

            self.video = cv2.VideoCapture(
                "assets/imagens/cortina.mp4"
            )

            if not self.video.isOpened():

                self.video = cv2.VideoCapture(
                    "cortina.mp4"
                )

            if not self.video.isOpened():

                print(
                    "ERRO: cortina.mp4 não foi encontrado."
                )

                self.video = None

        except Exception as erro:

            print(
                "ERRO AO CARREGAR CORTINA:",
                erro
            )

            self.video = None


    def iniciar(self):

        self.mostrar_resto = False
        self.video_terminou = False
        self.frame_atual = None

        if self.video is not None:

            self.video.set(
                cv2.CAP_PROP_POS_FRAMES,
                0
            )


    def atualizar(self):

        if self.video is None:

            self.video_terminou = True
            return

        if self.video_terminou:

            return

        sucesso, frame = self.video.read()

        if not sucesso:

            self.video_terminou = True
            self.frame_atual = None

            return

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame = cv2.resize(
            frame,
            (800, 500)
        )

        self.frame_atual = pygame.surfarray.make_surface(
            frame.swapaxes(0, 1)
        )


    def desenhar_nomes(
        self,
        tela,
        ranking
    ):

        rosa = (255, 105, 180)
        sombra = (255, 255, 255)

        if len(ranking) > 0:

            nome, pontos = ranking[0]

            texto = self.fonte_nomes.render(
                nome,
                True,
                rosa
            )

            texto_sombra = self.fonte_nomes.render(
                nome,
                True,
                sombra
            )

            posicao = texto.get_rect(
                center=(400, 180)
            )

            tela.blit(
                texto_sombra,
                (
                    posicao.x + 2,
                    posicao.y + 2
                )
            )

            tela.blit(
                texto,
                posicao
            )


        if len(ranking) > 1:

            nome, pontos = ranking[1]

            texto = self.fonte_nomes.render(
                nome,
                True,
                rosa
            )

            texto_sombra = self.fonte_nomes.render(
                nome,
                True,
                sombra
            )

            posicao = texto.get_rect(
                center=(260, 220)
            )

            tela.blit(
                texto_sombra,
                (
                    posicao.x + 2,
                    posicao.y + 2
                )
            )

            tela.blit(
                texto,
                posicao
            )


        if len(ranking) > 2:

            nome, pontos = ranking[2]

            texto = self.fonte_nomes.render(
                nome,
                True,
                rosa
            )

            texto_sombra = self.fonte_nomes.render(
                nome,
                True,
                sombra
            )

            posicao = texto.get_rect(
                center=(540, 220)
            )

            tela.blit(
                texto_sombra,
                (
                    posicao.x + 2,
                    posicao.y + 2
                )
            )

            tela.blit(
                texto,
                posicao
            )


    def remover_verde(
        self,
        frame
    ):

        pixels = pygame.surfarray.array3d(
            frame
        )

        pixels = pixels.swapaxes(
            0,
            1
        )

        r = pixels[:, :, 0].astype(
            np.int16
        )

        g = pixels[:, :, 1].astype(
            np.int16
        )

        b = pixels[:, :, 2].astype(
            np.int16
        )

        mascara_verde = (
            (g > 80)
            &
            (g > r * 1.20)
            &
            (g > b * 1.10)
        )

        alpha = np.where(
            mascara_verde,
            0,
            255
        ).astype(
            np.uint8
        )

        pixels_rgba = np.dstack(
            (
                pixels,
                alpha
            )
        )

        superficie = pygame.image.frombuffer(
            pixels_rgba.tobytes(),
            (800, 500),
            "RGBA"
        ).convert_alpha()

        return superficie


    def desenhar_podio(
        self,
        tela,
        ranking
    ):

        tela.blit(
            self.podio,
            (0, 0)
        )

        # Título RANKING rosa com borda rosa escuro

        titulo = self.fonte_grande.render(
            "RANKING",
            True,
            (255, 105, 180)
        )

        titulo_rect = titulo.get_rect(
            center=(400, 55)
        )

        borda = self.fonte_grande.render(
            "RANKING",
            True,
            (140, 10, 80)
        )

        for dx, dy in [
            (-3, 0),
            (3, 0),
            (0, -3),
            (0, 3)
        ]:

            tela.blit(
                borda,
                (
                    titulo_rect.x + dx,
                    titulo_rect.y + dy
                )
            )

        tela.blit(
            titulo,
            titulo_rect
        )

        self.desenhar_nomes(
            tela,
            ranking
        )


    def desenhar_resto(
        self,
        tela,
        ranking
    ):

        tela.blit(
            self.fundo_resto,
            (0, 0)
        )

        # Título RANKING rosa com borda rosa escuro

        titulo = self.fonte_grande.render(
            "RANKING",
            True,
            (255, 105, 180)
        )

        titulo_rect = titulo.get_rect(
            center=(400, 55)
        )

        borda = self.fonte_grande.render(
            "RANKING",
            True,
            (140, 10, 80)
        )

        for dx, dy in [
            (-3, 0),
            (3, 0),
            (0, -3),
            (0, 3)
        ]:

            tela.blit(
                borda,
                (
                    titulo_rect.x + dx,
                    titulo_rect.y + dy
                )
            )

        tela.blit(
            titulo,
            titulo_rect
        )

        y = 120

        for i, (nome, pontos) in enumerate(
            ranking
        ):

            texto = self.fonte.render(
                f"{i + 1}. {nome} - {pontos}",
                True,
                (140, 10, 80)
            )

            tela.blit(
                texto,
                (250, y)
            )

            y += 35

            if y > 350:

                break


        mouse = pygame.mouse.get_pos()


        if self.botao_voltar.collidepoint(mouse):

            cor_voltar = (
                255,
                105,
                180
            )

        else:

            cor_voltar = (
                255,
                255,
                255
            )


        pygame.draw.rect(
            tela,
            cor_voltar,
            self.botao_voltar,
            border_radius=10
        )


        texto_voltar = self.fonte.render(
            "VOLTAR",
            True,
            (0, 0, 0)
        )

        tela.blit(
            texto_voltar,
            texto_voltar.get_rect(
                center=self.botao_voltar.center
            )
        )


        if self.botao_inicio.collidepoint(mouse):

            cor_inicio = (
                255,
                105,
                180
            )

        else:

            cor_inicio = (
                255,
                255,
                255
            )


        pygame.draw.rect(
            tela,
            cor_inicio,
            self.botao_inicio,
            border_radius=10
        )


        texto_inicio = self.fonte.render(
            "TELA INICIAL",
            True,
            (0, 0, 0)
        )

        tela.blit(
            texto_inicio,
            texto_inicio.get_rect(
                center=self.botao_inicio.center
            )
        )


    def desenhar(
        self,
        tela,
        ranking
    ):

        if self.mostrar_resto:

            self.desenhar_resto(
                tela,
                ranking
            )

            return


        self.desenhar_podio(
            tela,
            ranking
        )


        if (
            self.frame_atual is not None
            and not self.video_terminou
        ):

            cortina = self.remover_verde(
                self.frame_atual
            )

            tela.blit(
                cortina,
                (0, 0)
            )


        if self.video_terminou:

            if len(ranking) > 3:

                mouse = pygame.mouse.get_pos()

                if self.botao_resto.collidepoint(mouse):

                    cor = (
                        255,
                        105,
                        180
                    )

                else:

                    cor = (
                        255,
                        255,
                        255
                    )

                pygame.draw.rect(
                    tela,
                    cor,
                    self.botao_resto,
                    border_radius=10
                )

                texto = self.fonte.render(
                    "O RESTO",
                    True,
                    (0, 0, 0)
                )

                tela.blit(
                    texto,
                    texto.get_rect(
                        center=self.botao_resto.center
                    )
                )


    def clicar(
        self,
        pos
    ):

        if self.mostrar_resto:

            if self.botao_voltar.collidepoint(pos):

                self.mostrar_resto = False

                return "ranking"


            if self.botao_inicio.collidepoint(pos):

                self.mostrar_resto = False

                return "menu"


        else:

            if (
                self.video_terminou
                and self.botao_resto.collidepoint(pos)
            ):

                self.mostrar_resto = True

                return "ranking"


        return None