import pygame
import random

from player import Player
from ranking import *

pygame.init()

# ===== CONFIG =====
LARGURA = 800
ALTURA = 500

tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption(
       "jump:spider-man "
)

clock = pygame.time.Clock()

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

fonte = pygame.font.SysFont(None, 36)
fonte_grande = pygame.font.SysFont(None, 60)

# ===== IMAGENS =====
try:

    player_img = pygame.image.load(
        "assets/imagens/player.png"
    )

    player_img = pygame.transform.scale(
        player_img,
        (60, 60)
    )

    obstaculo_img = pygame.image.load(
        "assets/imagens/obstaculo.png"
    )

    obstaculo_img = pygame.transform.scale(
        obstaculo_img,
        (50, 50)
    )

    fundo_img = pygame.image.load(
        "assets/imagens/fundo.png"
    )

    fundo_img = pygame.transform.scale(
        fundo_img,
        (800, 500)
    )

    bloco_img = pygame.image.load(
        "assets/imagens/bloco.png"
    )

    bloco_img = pygame.transform.scale(
        bloco_img,
        (60, 20)
    )

except:

    player_img = pygame.Surface((60, 60))
    player_img.fill((255, 0, 0))

    obstaculo_img = pygame.Surface((50, 50))
    obstaculo_img.fill((0, 0, 0))

    fundo_img = pygame.Surface((800, 500))
    fundo_img.fill((200, 200, 200))

    bloco_img = pygame.Surface((60, 20))
    bloco_img.fill((255, 255, 255))

# ===== PLAYER =====
player = Player(player_img)

# ===== VARIÁVEIS =====
obstaculos = []
blocos = []

pontos = 0

fundo_x = 0

estado = "menu"

mostrar_ranking = False

nome_jogador = ""

rodando = True

# ===== TEXTO =====
def desenhar_texto(texto, fonte, cor, x, y):

    img = fonte.render(texto, True, cor)

    tela.blit(img, (x, y))


# ===== RESET =====
def resetar_jogo():

    global player
    global obstaculos
    global blocos
    global pontos
    global fundo_x

    player = Player(player_img)

    obstaculos = []

    blocos = []

    pontos = 0

    fundo_x = 0


# ===== LOOP =====
while rodando:

    clock.tick(60)

    # ================= MENU =================
    if estado == "menu":

        tela.fill(BRANCO)

        desenhar_texto(
            "jump: spider-man",
            fonte_grande,
            PRETO,
            80,
            80
        )

        desenhar_texto(
            "Digite seu nome:",
            fonte,
            PRETO,
            260,
            170
        )

        desenhar_texto(
            nome_jogador,
            fonte,
            PRETO,
            260,
            210
        )

        desenhar_texto(
            "ENTER = Jogar",
            fonte,
            PRETO,
            280,
            270
        )

        desenhar_texto(
            "R = Ver Ranking",
            fonte,
            PRETO,
            260,
            320
        )

        if mostrar_ranking:

            ranking = carregar_ranking()

            y = 370

            desenhar_texto(
                "TOP 5",
                fonte,
                PRETO,
                340,
                y
            )

            y += 40

            for i, dado in enumerate(ranking):

                nome = dado[0]
                score = dado[1]

                desenhar_texto(
                    f"{i+1}° - {nome}: {score}",
                    fonte,
                    PRETO,
                    250,
                    y
                )

                y += 35

        pygame.display.update()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                rodando = False

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:

                    if nome_jogador != "":

                        resetar_jogo()

                        estado = "jogo"

                elif evento.key == pygame.K_r:

                    mostrar_ranking = not mostrar_ranking

                elif evento.key == pygame.K_BACKSPACE:

                    nome_jogador = nome_jogador[:-1]

                else:

                    if len(nome_jogador) < 10:

                        nome_jogador += evento.unicode

    # ================= JOGO =================
    elif estado == "jogo":

        fundo_x -= 2

        if fundo_x <= -800:

            fundo_x = 0

        tela.blit(fundo_img, (fundo_x, 0))

        tela.blit(fundo_img, (fundo_x + 800, 0))

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                rodando = False

        teclas = pygame.key.get_pressed()

        player.pular(teclas)

        player_y_anterior = player.y

        player.atualizar()

        # ===== OBSTÁCULOS =====
        if len(obstaculos) == 0 or obstaculos[-1][0] < 450:

            obstaculos.append([800, 390])

        # ===== BLOCOS =====
        if len(blocos) == 0:

            if len(obstaculos) > 0:

                if obstaculos[-1][0] < 500:

                    if random.randint(0, 100) < 25:

                        quantidade = random.randint(3, 5)

                        for i in range(quantidade):

                            x = 800 + (i * 65)

                            y = 380 - (i * 30)

                            blocos.append([x, y])

        velocidade = 6 + (pontos / 1000) * 0.5

        for obs in obstaculos:

            obs[0] -= velocidade

        for bloco in blocos:

            bloco[0] -= velocidade

        obstaculos = [
            o for o in obstaculos if o[0] > -50
        ]

        blocos = [
            b for b in blocos if b[0] > -60
        ]

        player_rect = player.rect()

        # ===== COLISÃO =====
        for obs in obstaculos:

            obs_rect = pygame.Rect(
                obs[0],
                obs[1],
                50,
                50
            )

            if player_rect.colliderect(obs_rect):

                salvar_ranking(
                    nome_jogador,
                    pontos
                )

                estado = "gameover"

        # ===== BLOCOS =====
        for bloco in blocos:

            bloco_rect = pygame.Rect(
                bloco[0],
                bloco[1],
                60,
                20
            )

            if player_rect.colliderect(bloco_rect):

                if (
                    player.vel_y > 0
                    and player_y_anterior + 60
                    <= bloco_rect.top + 15
                ):

                    player.y = bloco_rect.top - 60

                    player.vel_y = 0

                    player.no_chao = True

        pontos += 1

        texto = fonte.render(
            f"Pontos: {pontos}",
            True,
            PRETO
        )

        player.desenhar(tela)

        for obs in obstaculos:

            tela.blit(
                obstaculo_img,
                (obs[0], obs[1])
            )

        for bloco in blocos:

            tela.blit(
                bloco_img,
                (bloco[0], bloco[1])
            )

        tela.blit(texto, (10, 10))

        pygame.display.update()

    # ================= GAME OVER =================
    elif estado == "gameover":

        tela.fill(BRANCO)

        desenhar_texto(
            "GAME OVER",
            fonte_grande,
            PRETO,
            220,
            120
        )

        desenhar_texto(
            f"PONTOS: {pontos}",
            fonte,
            PRETO,
            300,
            220
        )

        desenhar_texto(
            "ENTER = Menu",
            fonte,
            PRETO,
            280,
            300
        )

        pygame.display.update()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                rodando = False

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:

                    estado = "menu"

pygame.quit()