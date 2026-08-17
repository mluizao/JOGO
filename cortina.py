import cv2
import pygame
import numpy as np


class VideoCortina:

    def __init__(self, caminho):
        self.video = cv2.VideoCapture(caminho)

        self.fps = self.video.get(cv2.CAP_PROP_FPS)

        if self.fps <= 0:
            self.fps = 30

        self.ultimo_frame = pygame.time.get_ticks()

        self.finalizado = False

    def atualizar(self):

        if self.finalizado:
            return None

        agora = pygame.time.get_ticks()

        intervalo = 1000 / self.fps

        if agora - self.ultimo_frame < intervalo:
            return None

        self.ultimo_frame = agora

        sucesso, frame = self.video.read()

        if not sucesso:
            self.finalizado = True
            self.video.release()
            return None

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detecta o verde
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        limite_inferior = np.array([35, 60, 40])
        limite_superior = np.array([90, 255, 255])

        mascara = cv2.inRange(
            hsv,
            limite_inferior,
            limite_superior
        )

        # Inverte a máscara
        mascara = cv2.bitwise_not(mascara)

        # Cria canal de transparência
        frame_rgba = np.dstack((frame, mascara))

        altura, largura = frame.shape[:2]

        superficie = pygame.image.frombuffer(
            frame_rgba.tobytes(),
            (largura, altura),
            "RGBA"
        ).convert_alpha()

        return superficie

    def reiniciar(self):

        self.video.release()

        self.video = cv2.VideoCapture(
            "assets/imagens/cortina.mp4"
        )

        self.finalizado = False
        self.ultimo_frame = pygame.time.get_ticks()