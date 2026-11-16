
import os
import random
import pygame

from obstaculo import Caixa
from predios import largura_predio


def carregar_caixa():
    pasta_projeto = os.path.dirname(os.path.abspath(__file__))

    caminho = os.path.join(
        pasta_projeto,
        "assets",
        "imagens",
        "caixas",
        "caixa.png"
    )

    try:
        imagem = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.smoothscale(imagem, (50, 50))

    except (pygame.error, FileNotFoundError) as erro:
        print(f"Erro ao carregar {caminho}: {erro}")

        imagem = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.rect(imagem, (130, 75, 30), (2, 2, 46, 46))
        pygame.draw.rect(imagem, (70, 35, 15), (2, 2, 46, 46), 3)

        return imagem


def adicionar_caixa_no_predio(jogo, predio, caixa_img):
    largura = largura_predio(predio)

    largura_caixa = 50
    altura_caixa = 50

    # Não coloca caixas em prédios estreitos.
    if largura < 220:
        return

    # Nem todo prédio terá uma caixa.
    if random.random() > 0.55:
        return

    # Mantém a caixa dentro da área livre do telhado.
    inicio_x = int(predio["x"] + 100)
    fim_x = int(predio["x"] + largura - largura_caixa - 100)

    if fim_x <= inicio_x:
        return

    caixa_y = int(predio["telhado_y"] - altura_caixa)

    # Tenta encontrar uma posição livre.
    for _ in range(30):
        caixa_x = random.randint(inicio_x, fim_x)

        caixa_rect = pygame.Rect(
            caixa_x,
            caixa_y,
            largura_caixa,
            altura_caixa
        )

        # Evita caixas muito próximas do jogador.
        if caixa_x < jogo["player_x"] + 180:
            continue

        bloqueada = False

        # Verifica obstáculos e estruturas no telhado.
        for obstaculo in predio.get("obstaculos", []):
            obstaculo_rect = pygame.Rect(
                int(obstaculo["x"]),
                int(obstaculo["y"]),
                int(obstaculo["largura"]),
                int(obstaculo["altura"])
            )

            if caixa_rect.colliderect(obstaculo_rect):
                bloqueada = True
                break

        if bloqueada:
            continue

        # Evita colocar caixas muito perto de outras caixas.
        for caixa in jogo.get("caixas", []):
            outra_rect = caixa.rect()

            if caixa_rect.inflate(35, 20).colliderect(outra_rect):
                bloqueada = True
                break

        if bloqueada:
            continue

        jogo["caixas"].append(
            Caixa(caixa_img, caixa_x, caixa_y)
        )

        return
