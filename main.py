import pygame
import random

from player import Player
from ranking import *

pygame.init()

ranking = carregar_ranking()

# CONFIG

LARGURA = 800
ALTURA = 500

tela = pygame.Surface((LARGURA, ALTURA))

janela = pygame.display.set_mode(
    (LARGURA, ALTURA),
    pygame.RESIZABLE
)

pygame.display.set_caption("Jump Homem-Aranha")

clock = pygame.time.Clock()

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 215, 0)

fonte = pygame.font.SysFont(None, 36)
fonte_grande = pygame.font.SysFont(None, 60)

BOTAO_JOGAR = pygame.Rect(250, 270, 300, 50)
BOTAO_RANKING = pygame.Rect(250, 335, 300, 50)
BOTAO_SAIR = pygame.Rect(250, 400, 300, 50)

BOTAO_VOLTAR = pygame.Rect(250, 360, 300, 40)

BOTAO_JOGAR_NOVAMENTE = pygame.Rect(200, 270, 400, 50)
BOTAO_MENU_GAME_OVER = pygame.Rect(200, 330, 400, 50)

tela_cheia = False


# IMAGENS

try:

    fundo_menu = pygame.image.load(
        "assets/imagens/fundo_menu.png"
    )

    fundo_menu = pygame.transform.scale(
        fundo_menu,
        (800, 500)
    )

    game_over_img = pygame.image.load(
        "assets/imagens/game_over.png"
    ).convert()

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

    fundo_menu = pygame.Surface((800, 500))
    fundo_menu.fill((20, 20, 35))

    game_over_img = pygame.Surface((800, 500))
    game_over_img.fill((20, 20, 35))

    player_img = pygame.Surface((60, 60))
    player_img.fill((255, 0, 0))

    obstaculo_img = pygame.Surface((50, 50))
    obstaculo_img.fill((0, 0, 0))

    fundo_img = pygame.Surface((800, 500))
    fundo_img.fill((150, 150, 150))

    bloco_img = pygame.Surface((60, 20))
    bloco_img.fill((255, 255, 255))


# ESTADOS

estado = "menu"
nome_jogador = ""
estado_prev = None


# RESET

def resetar_jogo():

    return {
        "player_x": 100,
        "player_y": 395,
        "vel_y": 0,
        "gravidade": 0.7,
        "no_chao": True,
        "tempo_pulo": 0,
        "obstaculos": [],
        "blocos": [],
        "moedas": [],
        "moedas_coletadas": 0,
        "pontos": 0,
        "fundo_x": 0,
        "velocidade_base": 6
    }


jogo = resetar_jogo()


# MOUSE

def converter_mouse(pos):

    largura_janela, altura_janela = janela.get_size()

    escala_x = largura_janela / LARGURA
    escala_y = altura_janela / ALTURA

    escala = min(escala_x, escala_y)

    nova_largura = int(LARGURA * escala)
    nova_altura = int(ALTURA * escala)

    offset_x = (largura_janela - nova_largura) // 2
    offset_y = (altura_janela - nova_altura) // 2

    mouse_x = (pos[0] - offset_x) / escala
    mouse_y = (pos[1] - offset_y) / escala

    return mouse_x, mouse_y


# REDIMENSIONAMENTO

def mostrar_tela():

    largura_janela, altura_janela = janela.get_size()

    escala_x = largura_janela / LARGURA
    escala_y = altura_janela / ALTURA

    escala = min(escala_x, escala_y)

    nova_largura = int(LARGURA * escala)
    nova_altura = int(ALTURA * escala)

    tela_redimensionada = pygame.transform.scale(
        tela,
        (nova_largura, nova_altura)
    )

    janela.fill(PRETO)

    pos_x = (largura_janela - nova_largura) // 2
    pos_y = (altura_janela - nova_altura) // 2

    janela.blit(
        tela_redimensionada,
        (pos_x, pos_y)
    )


# LOOP PRINCIPAL

rodando = True

while rodando:

    clock.tick(60)

    for evento in pygame.event.get():

        # SAIR

        if evento.type == pygame.QUIT:

            rodando = False


        # REDIMENSIONAR

        if evento.type == pygame.VIDEORESIZE:

            if not tela_cheia:

                janela = pygame.display.set_mode(
                    evento.size,
                    pygame.RESIZABLE
                )


        # TECLADO

        if evento.type == pygame.KEYDOWN:

            # F11

            if evento.key == pygame.K_F11:

                tela_cheia = not tela_cheia

                if tela_cheia:

                    janela = pygame.display.set_mode(
                        (0, 0),
                        pygame.FULLSCREEN
                    )

                else:

                    janela = pygame.display.set_mode(
                        (LARGURA, ALTURA),
                        pygame.RESIZABLE
                    )


            # MENU

            if estado == "menu":

                if (
                    evento.key == pygame.K_RETURN
                    and nome_jogador.strip() != ""
                ):

                    jogo = resetar_jogo()
                    estado = "jogo"

                elif evento.key == pygame.K_BACKSPACE:

                    nome_jogador = nome_jogador[:-1]

                else:

                    if evento.unicode.isprintable():

                        nome_jogador += evento.unicode


            # GAME OVER

            elif estado == "game_over":

                if evento.key == pygame.K_RETURN:

                    jogo = resetar_jogo()
                    estado = "jogo"

                elif evento.key == pygame.K_ESCAPE:

                    estado = "menu"
                    nome_jogador = ""


        # MOUSE

        if (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
        ):

            mouse_pos = converter_mouse(evento.pos)


            # BOTÃO JOGAR

            if (
                estado == "menu"
                and BOTAO_JOGAR.collidepoint(mouse_pos)
            ):

                if nome_jogador.strip() != "":

                    jogo = resetar_jogo()
                    estado = "jogo"


            # BOTÃO RANKING

            elif (
                estado == "menu"
                and BOTAO_RANKING.collidepoint(mouse_pos)
            ):

                estado_prev = estado
                ranking = carregar_ranking()
                estado = "ranking"


            # BOTÃO SAIR

            elif (
                estado == "menu"
                and BOTAO_SAIR.collidepoint(mouse_pos)
            ):

                rodando = False


            # BOTÃO VOLTAR

            elif (
                estado == "ranking"
                and BOTAO_VOLTAR.collidepoint(mouse_pos)
            ):

                estado = estado_prev or "menu"
                estado_prev = None


            # BOTÃO JOGAR NOVAMENTE

            elif (
                estado == "game_over"
                and BOTAO_JOGAR_NOVAMENTE.collidepoint(mouse_pos)
            ):

                jogo = resetar_jogo()
                estado = "jogo"


            # BOTÃO MENU GAME OVER

            elif (
                estado == "game_over"
                and BOTAO_MENU_GAME_OVER.collidepoint(mouse_pos)
            ):

                estado = "menu"
                nome_jogador = ""


    tela.fill(BRANCO)

    mouse_pos = converter_mouse(
        pygame.mouse.get_pos()
    )


    # MENU

    if estado == "menu":

        tela.blit(
            fundo_menu,
            (0, 0)
        )


        # TITULO

        titulo = fonte_grande.render(
            "JUMP HOMEM-ARANHA",
            True,
            (220, 30, 30)
        )

        titulo_rect = titulo.get_rect(
            center=(400, 70)
        )


        # BORDA AZUL

        borda = fonte_grande.render(
            "JUMP HOMEM-ARANHA",
            True,
            (30, 70, 200)
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


        # NOME

        texto_nome = fonte.render(
            "DIGITE SEU NOME",
            True,
            (30, 70, 200)
        )

        texto_nome_rect = texto_nome.get_rect(
            center=(400, 170)
        )

        tela.blit(
            texto_nome,
            texto_nome_rect
        )


        # CAIXA DO NOME

        caixa_nome = pygame.Rect(
            200,
            195,
            400,
            50
        )

        pygame.draw.rect(
            tela,
            BRANCO,
            caixa_nome,
            border_radius=10
        )

        texto_digitado = fonte.render(
            nome_jogador if nome_jogador else "Digite aqui...",
            True,
            PRETO
        )

        texto_digitado_rect = texto_digitado.get_rect(
            center=caixa_nome.center
        )

        tela.blit(
            texto_digitado,
            texto_digitado_rect
        )


        # BOTÃO JOGAR

        if BOTAO_JOGAR.collidepoint(mouse_pos):

            cor_jogar = (50, 180, 70)

        else:

            cor_jogar = BRANCO

        pygame.draw.rect(
            tela,
            cor_jogar,
            BOTAO_JOGAR,
            border_radius=10
        )

        texto_jogar = fonte.render(
            "JOGAR",
            True,
            PRETO
        )

        texto_jogar_rect = texto_jogar.get_rect(
            center=BOTAO_JOGAR.center
        )

        tela.blit(
            texto_jogar,
            texto_jogar_rect
        )


        # BOTÃO RANKING

        if BOTAO_RANKING.collidepoint(mouse_pos):

            cor_ranking = (50, 180, 70)

        else:

            cor_ranking = BRANCO

        pygame.draw.rect(
            tela,
            cor_ranking,
            BOTAO_RANKING,
            border_radius=10
        )

        texto_ranking = fonte.render(
            "RANKING",
            True,
            PRETO
        )

        texto_ranking_rect = texto_ranking.get_rect(
            center=BOTAO_RANKING.center
        )

        tela.blit(
            texto_ranking,
            texto_ranking_rect
        )


        # BOTÃO SAIR

        if BOTAO_SAIR.collidepoint(mouse_pos):

            cor_sair = (50, 180, 70)

        else:

            cor_sair = BRANCO

        pygame.draw.rect(
            tela,
            cor_sair,
            BOTAO_SAIR,
            border_radius=10
        )

        texto_sair = fonte.render(
            "SAIR",
            True,
            PRETO
        )

        texto_sair_rect = texto_sair.get_rect(
            center=BOTAO_SAIR.center
        )

        tela.blit(
            texto_sair,
            texto_sair_rect
        )


    # RANKING

    elif estado == "ranking":

        tela.fill(BRANCO)

        titulo = fonte_grande.render(
            "RANKING",
            True,
            PRETO
        )

        tela.blit(
            titulo,
            (300, 50)
        )

        y = 140

        for i, (nome, pontos) in enumerate(ranking):

            texto = fonte.render(
                f"{i + 1}. {nome} - {pontos}",
                True,
                PRETO
            )

            tela.blit(
                texto,
                (250, y)
            )

            y += 30

        pygame.draw.rect(
            tela,
            PRETO,
            BOTAO_VOLTAR,
            2
        )

        instr = fonte.render(
            "Voltar",
            True,
            PRETO
        )

        tela.blit(
            instr,
            (
                BOTAO_VOLTAR.x + 115,
                BOTAO_VOLTAR.y + 7
            )
        )


    # JOGO

    elif estado == "jogo":

        player_y_anterior = jogo["player_y"]

        jogo["fundo_x"] -= 2

        if jogo["fundo_x"] <= -800:

            jogo["fundo_x"] = 0

        tela.blit(
            fundo_img,
            (jogo["fundo_x"], 0)
        )

        tela.blit(
            fundo_img,
            (jogo["fundo_x"] + 800, 0)
        )

        teclas = pygame.key.get_pressed()


        # PULO

        if (
            teclas[pygame.K_SPACE]
            and jogo["no_chao"]
        ):

            jogo["vel_y"] = -15
            jogo["no_chao"] = False
            jogo["tempo_pulo"] = 0

        if (
            teclas[pygame.K_SPACE]
            and not jogo["no_chao"]
        ):

            if jogo["tempo_pulo"] < 10:

                jogo["vel_y"] -= 0.5
                jogo["tempo_pulo"] += 1

        jogo["vel_y"] += jogo["gravidade"]
        jogo["player_y"] += jogo["vel_y"]
        jogo["no_chao"] = False


        # CHÃO

        if jogo["player_y"] >= 395:

            jogo["player_y"] = 395
            jogo["vel_y"] = 0
            jogo["no_chao"] = True


        # GERAR OBSTÁCULOS

        if (
            len(jogo["obstaculos"]) == 0
            or jogo["obstaculos"][-1][0] < 450
        ):

            jogo["obstaculos"].append(
                [800, 405]
            )


        # GERAR BLOCOS

        if len(jogo["blocos"]) == 0:

            if (
                len(jogo["obstaculos"]) > 0
                and jogo["obstaculos"][-1][0] < 500
            ):

                if random.randint(0, 100) < 25:

                    quantidade = random.randint(3, 5)

                    for i in range(quantidade):

                        x = 800 + (i * 65)
                        y = 395 - (i * 30)

                        jogo["blocos"].append(
                            [x, y]
                        )


        # GERAR MOEDAS

        if (
            len(jogo["moedas"]) == 0
            or jogo["moedas"][-1][0] < 550
        ):

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

                    moeda_rect = pygame.Rect(
                        x,
                        y,
                        30,
                        30
                    )

                    pode_criar = True


                    # VERIFICAR DINOSSAUROS

                    for obs in jogo["obstaculos"]:

                        obstaculo_rect = pygame.Rect(
                            obs[0] - 100,
                            obs[1] - 50,
                            150,
                            100
                        )

                        if moeda_rect.colliderect(
                            obstaculo_rect
                        ):

                            pode_criar = False
                            break


                    # VERIFICAR BLOCOS

                    if pode_criar:

                        for bloco in jogo["blocos"]:

                            bloco_rect = pygame.Rect(
                                bloco[0] - 20,
                                bloco[1] - 20,
                                100,
                                60
                            )

                            if moeda_rect.colliderect(
                                bloco_rect
                            ):

                                pode_criar = False
                                break


                    # CRIAR MOEDA

                    if pode_criar:

                        jogo["moedas"].append(
                            [x, y]
                        )

                        moeda_criada = True

                    tentativas += 1


        # VELOCIDADE

        velocidade = (
            jogo["velocidade_base"]
            + (jogo["pontos"] / 1000) * 0.5
        )


        # MOVIMENTO

        for obs in jogo["obstaculos"]:

            obs[0] -= velocidade

        for bloco in jogo["blocos"]:

            bloco[0] -= velocidade

        for moeda in jogo["moedas"]:

            moeda[0] -= velocidade


        # REMOVER OBJETOS FORA DA TELA

        jogo["obstaculos"] = [
            o
            for o in jogo["obstaculos"]
            if o[0] > -50
        ]

        jogo["blocos"] = [
            b
            for b in jogo["blocos"]
            if b[0] > -60
        ]

        jogo["moedas"] = [
            m
            for m in jogo["moedas"]
            if m[0] > -30
        ]


        # COLISÃO DO JOGADOR

        player_rect = pygame.Rect(
            jogo["player_x"],
            jogo["player_y"],
            60,
            60
        )


        # COLETAR MOEDAS

        for moeda in jogo["moedas"]:

            moeda_rect = pygame.Rect(
                moeda[0],
                moeda[1],
                30,
                30
            )

            if player_rect.colliderect(
                moeda_rect
            ):

                jogo["moedas_coletadas"] += 1
                jogo["pontos"] += 25

                jogo["moedas"].remove(moeda)

                break


        # COLISÃO COM OBSTÁCULOS

        for obs in jogo["obstaculos"]:

            obstaculo_rect = pygame.Rect(
                obs[0],
                obs[1],
                50,
                50
            )

            if player_rect.colliderect(
                obstaculo_rect
            ):

                salvar_ranking(
                    nome_jogador,
                    jogo["pontos"]
                )

                ranking = carregar_ranking()
                estado = "game_over"

                break


        if estado == "game_over":

            continue


        # COLISÃO COM BLOCOS

        for bloco in jogo["blocos"]:

            bloco_rect = pygame.Rect(
                bloco[0],
                bloco[1],
                60,
                20
            )

            if player_rect.colliderect(
                bloco_rect
            ):

                if (
                    jogo["vel_y"] > 0
                    and player_y_anterior + 60
                    <= bloco_rect.top + 15
                ):

                    jogo["player_y"] = (
                        bloco_rect.top - 60
                    )

                    jogo["vel_y"] = 0
                    jogo["no_chao"] = True


        # PONTOS

        jogo["pontos"] += 1


        # DESENHAR JOGADOR

        tela.blit(
            player_img,
            (
                jogo["player_x"],
                jogo["player_y"]
            )
        )


        # DESENHAR OBSTÁCULOS

        for obs in jogo["obstaculos"]:

            tela.blit(
                obstaculo_img,
                (
                    obs[0],
                    obs[1]
                )
            )


        # DESENHAR BLOCOS

        for bloco in jogo["blocos"]:

            tela.blit(
                bloco_img,
                (
                    bloco[0],
                    bloco[1]
                )
            )


        # DESENHAR MOEDAS

        for moeda in jogo["moedas"]:

            centro_x = int(
                moeda[0] + 15
            )

            centro_y = int(
                moeda[1] + 15
            )

            pygame.draw.circle(
                tela,
                AMARELO,
                (centro_x, centro_y),
                15
            )

            pygame.draw.circle(
                tela,
                BRANCO,
                (
                    centro_x - 5,
                    centro_y - 5
                ),
                4
            )


        # PONTOS E MOEDAS

        texto = fonte.render(
            f"Pontos: {jogo['pontos']}   Moedas: {jogo['moedas_coletadas']}",
            True,
            BRANCO
        )

        tela.blit(
            texto,
            (10, 10)
        )


    # GAME OVER

    elif estado == "game_over":

        # FUNDO

        tela.blit(
            game_over_img,
            (0, 0)
        )


        # TITULO GAME OVER

        titulo = fonte_grande.render(
            "GAME OVER",
            True,
            (220, 30, 30)
        )

        titulo_rect = titulo.get_rect(
            center=(400, 65)
        )


        # BORDA AZUL DO TITULO

        borda = fonte_grande.render(
            "GAME OVER",
            True,
            (30, 70, 200)
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


        # NOME

        nome = fonte.render(
            f"Jogador: {nome_jogador}",
            True,
            BRANCO
        )

        nome_rect = nome.get_rect(
            center=(400, 130)
        )

        tela.blit(
            nome,
            nome_rect
        )


        # PONTOS

        pontos = fonte.render(
            f"Pontos: {jogo['pontos']}",
            True,
            BRANCO
        )

        pontos_rect = pontos.get_rect(
            center=(400, 165)
        )

        tela.blit(
            pontos,
            pontos_rect
        )


        # MOEDAS

        moedas = fonte.render(
            f"Moedas coletadas: {jogo['moedas_coletadas']}",
            True,
            BRANCO
        )

        moedas_rect = moedas.get_rect(
            center=(400, 200)
        )

        tela.blit(
            moedas,
            moedas_rect
        )


        # BOTÃO JOGAR NOVAMENTE

        if BOTAO_JOGAR_NOVAMENTE.collidepoint(mouse_pos):

            cor_jogar = (50, 180, 70)

        else:

            cor_jogar = BRANCO

        pygame.draw.rect(
            tela,
            cor_jogar,
            BOTAO_JOGAR_NOVAMENTE,
            border_radius=10
        )

        texto_jogar = fonte.render(
            "JOGAR NOVAMENTE",
            True,
            PRETO
        )

        texto_jogar_rect = texto_jogar.get_rect(
            center=BOTAO_JOGAR_NOVAMENTE.center
        )

        tela.blit(
            texto_jogar,
            texto_jogar_rect
        )


        # BOTÃO VOLTAR AO MENU

        if BOTAO_MENU_GAME_OVER.collidepoint(mouse_pos):

            cor_menu = (50, 180, 70)

        else:

            cor_menu = BRANCO

        pygame.draw.rect(
            tela,
            cor_menu,
            BOTAO_MENU_GAME_OVER,
            border_radius=10
        )

        texto_menu = fonte.render(
            "VOLTAR AO MENU",
            True,
            PRETO
        )

        texto_menu_rect = texto_menu.get_rect(
            center=BOTAO_MENU_GAME_OVER.center
        )

        tela.blit(
            texto_menu,
            texto_menu_rect
        )


    mostrar_tela()

    pygame.display.flip()


pygame.quit()