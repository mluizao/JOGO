
import pygame
import os
import random

from player import Player
from ranking import carregar_ranking, salvar_ranking
from cortina import (
    converter_mouse,
    mostrar_tela,
    alternar_tela_cheia,
    RankingCortina
)

pygame.init()

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

# Altura do chão do jogo
CHAO_Y = 420

BOTAO_JOGAR = pygame.Rect(250, 270, 300, 50)
BOTAO_RANKING = pygame.Rect(250, 335, 300, 50)
BOTAO_SAIR = pygame.Rect(250, 400, 300, 50)

BOTAO_JOGAR_NOVAMENTE = pygame.Rect(
    200, 270, 400, 50
)

BOTAO_MENU_GAME_OVER = pygame.Rect(
    200, 330, 400, 50
)

tela_cheia = False

ranking = carregar_ranking()
ranking_cortina = RankingCortina()

try:
    fundo_menu = pygame.image.load(
        "assets/imagens/fundo_menu.png"
    ).convert()

    fundo_menu = pygame.transform.scale(
        fundo_menu, (800, 500)
    )

    game_over_img = pygame.image.load(
        "assets/imagens/game_over.png"
    ).convert()

    player_img = pygame.image.load(
        "assets/imagens/player.png"
    ).convert_alpha()

    player_img = pygame.transform.scale(
        player_img, (60, 60)
    )

    obstaculo_img = pygame.image.load(
        "assets/imagens/obstaculo.png"
    ).convert_alpha()

    obstaculo_img = pygame.transform.scale(
        obstaculo_img, (50, 50)
    )

    # Caminho corrigido da imagem do fundo da cidade
    caminho_fundo = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "assets",
        "imagens",
        "fundo_cidade.png"
    )

    print(
        "Caminho procurado para o fundo:",
        caminho_fundo
    )

    print(
        "Imagem encontrada:",
        os.path.isfile(caminho_fundo)
    )

    fundo_img = pygame.image.load(
        caminho_fundo
    ).convert()

    fundo_img = pygame.transform.scale(
        fundo_img, (800, 500)
    )

    bloco_img = pygame.image.load(
        "assets/imagens/bloco.png"
    ).convert_alpha()

    bloco_img = pygame.transform.scale(
        bloco_img, (60, 20)
    )

except Exception as erro:
    print("Erro ao carregar uma imagem:", erro)

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


def resetar_jogo():
    return {
        "player_x": 100,

        # Personagem começa apoiado no chão
        "player_y": CHAO_Y - 60,

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


estado = "menu"
nome_jogador = ""
jogo = resetar_jogo()

rodando = True

while rodando:
    clock.tick(60)

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.VIDEORESIZE:
            if not tela_cheia:
                janela = pygame.display.set_mode(
                    evento.size,
                    pygame.RESIZABLE
                )

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_F11:
                janela, tela_cheia = alternar_tela_cheia(
                    janela,
                    tela_cheia,
                    LARGURA,
                    ALTURA
                )

            if estado == "menu":

                if (
                    evento.key == pygame.K_RETURN
                    and nome_jogador.strip() != ""
                ):
                    jogo = resetar_jogo()
                    estado = "jogo"

                elif evento.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1]

                elif evento.unicode.isprintable():
                    nome_jogador += evento.unicode

            elif estado == "ranking":

                if evento.key == pygame.K_ESCAPE:
                    estado = "menu"

            elif estado == "game_over":

                if evento.key == pygame.K_RETURN:
                    jogo = resetar_jogo()
                    estado = "jogo"

                elif evento.key == pygame.K_ESCAPE:
                    estado = "menu"
                    nome_jogador = ""

        if (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
        ):

            mouse_pos = converter_mouse(
                evento.pos,
                janela,
                LARGURA,
                ALTURA
            )

            if (
                estado == "menu"
                and BOTAO_JOGAR.collidepoint(mouse_pos)
            ):
                if nome_jogador.strip() != "":
                    jogo = resetar_jogo()
                    estado = "jogo"

            elif (
                estado == "menu"
                and BOTAO_RANKING.collidepoint(mouse_pos)
            ):
                ranking = carregar_ranking()
                ranking_cortina.iniciar()
                estado = "ranking"

            elif (
                estado == "menu"
                and BOTAO_SAIR.collidepoint(mouse_pos)
            ):
                rodando = False

            elif estado == "ranking":

                resultado = ranking_cortina.clicar(
                    mouse_pos
                )

                if resultado == "menu":
                    estado = "menu"
                    nome_jogador = ""

                elif resultado == "ranking":
                    estado = "ranking"

            elif (
                estado == "game_over"
                and BOTAO_JOGAR_NOVAMENTE.collidepoint(
                    mouse_pos
                )
            ):
                jogo = resetar_jogo()
                estado = "jogo"

            elif (
                estado == "game_over"
                and BOTAO_MENU_GAME_OVER.collidepoint(
                    mouse_pos
                )
            ):
                estado = "menu"
                nome_jogador = ""

    tela.fill(BRANCO)

    mouse_pos = converter_mouse(
        pygame.mouse.get_pos(),
        janela,
        LARGURA,
        ALTURA
    )

    # =========================
    # MENU PRINCIPAL
    # =========================

    if estado == "menu":

        tela.blit(fundo_menu, (0, 0))

        titulo = fonte_grande.render(
            "JUMP HOMEM-ARANHA",
            True,
            (220, 30, 30)
        )

        titulo_rect = titulo.get_rect(
            center=(400, 70)
        )

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

        tela.blit(titulo, titulo_rect)

        texto_nome = fonte.render(
            "DIGITE SEU NOME",
            True,
            (30, 70, 200)
        )

        tela.blit(
            texto_nome,
            texto_nome.get_rect(
                center=(400, 170)
            )
        )

        caixa_nome = pygame.Rect(
            200, 195, 400, 50
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

        tela.blit(
            texto_digitado,
            texto_digitado.get_rect(
                center=caixa_nome.center
            )
        )

        cor_jogar = (
            (50, 180, 70)
            if BOTAO_JOGAR.collidepoint(mouse_pos)
            else BRANCO
        )

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

        tela.blit(
            texto_jogar,
            texto_jogar.get_rect(
                center=BOTAO_JOGAR.center
            )
        )

        cor_ranking = (
            (50, 180, 70)
            if BOTAO_RANKING.collidepoint(mouse_pos)
            else BRANCO
        )

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

        tela.blit(
            texto_ranking,
            texto_ranking.get_rect(
                center=BOTAO_RANKING.center
            )
        )

        cor_sair = (
            (50, 180, 70)
            if BOTAO_SAIR.collidepoint(mouse_pos)
            else BRANCO
        )

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

        tela.blit(
            texto_sair,
            texto_sair.get_rect(
                center=BOTAO_SAIR.center
            )
        )

    # =========================
    # RANKING
    # =========================

    elif estado == "ranking":

        ranking_cortina.atualizar()
        ranking_cortina.desenhar(tela, ranking)

    # =========================
    # JOGO
    # =========================

    elif estado == "jogo":

        player_y_anterior = jogo["player_y"]

        # Movimento do fundo
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

        # Pulo
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_SPACE] and jogo["no_chao"]:
            jogo["vel_y"] = -15
            jogo["no_chao"] = False
            jogo["tempo_pulo"] = 0

        # Aumenta o pulo enquanto segura espaço
        if (
            teclas[pygame.K_SPACE]
            and not jogo["no_chao"]
        ):
            if jogo["tempo_pulo"] < 10:
                jogo["vel_y"] -= 0.5
                jogo["tempo_pulo"] += 1

        # Gravidade e movimento vertical
        jogo["vel_y"] += jogo["gravidade"]
        jogo["player_y"] += jogo["vel_y"]

        # CORREÇÃO: mantém o personagem no chão
        if jogo["player_y"] + 60 >= CHAO_Y:
            jogo["player_y"] = CHAO_Y - 60
            jogo["vel_y"] = 0
            jogo["no_chao"] = True
        else:
            jogo["no_chao"] = False

        # Criação dos obstáculos
        if (
            len(jogo["obstaculos"]) == 0
            or jogo["obstaculos"][-1][0] < 450
        ):
            jogo["obstaculos"].append([800, 405])

        # Criação dos blocos em escada
        if (
            len(jogo["blocos"]) == 0
            and len(jogo["obstaculos"]) > 0
            and jogo["obstaculos"][-1][0] < 500
        ):

            if random.randint(0, 100) < 25:

                quantidade = random.randint(3, 5)

                for i in range(quantidade):
                    x = 800 + i * 65
                    y = 395 - i * 30

                    jogo["blocos"].append([x, y])

        # Criação das moedas
        if (
            len(jogo["moedas"]) == 0
            or jogo["moedas"][-1][0] < 550
        ):

            quantidade_moedas = random.randint(2, 3)
            alturas = [280, 230, 180]

            for i in range(quantidade_moedas):

                x = 850 + i * 60
                tentativas = 0
                moeda_criada = False

                while tentativas < 20 and not moeda_criada:

                    y = random.choice(alturas)

                    moeda_rect = pygame.Rect(
                        x, y, 30, 30
                    )

                    pode_criar = True

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

                    if pode_criar:
                        jogo["moedas"].append([x, y])
                        moeda_criada = True

                    tentativas += 1

        # Velocidade aumenta a cada 1000 pontos
        velocidade = (
            jogo["velocidade_base"]
            + (jogo["pontos"] / 1000) * 0.5
        )

        # Movimento dos obstáculos
        for obs in jogo["obstaculos"]:
            obs[0] -= velocidade

        # Movimento dos blocos
        for bloco in jogo["blocos"]:
            bloco[0] -= velocidade

        # Movimento das moedas
        for moeda in jogo["moedas"]:
            moeda[0] -= velocidade

        # Remove objetos que saíram da tela
        jogo["obstaculos"] = [
            o for o in jogo["obstaculos"]
            if o[0] > -50
        ]

        jogo["blocos"] = [
            b for b in jogo["blocos"]
            if b[0] > -60
        ]

        jogo["moedas"] = [
            m for m in jogo["moedas"]
            if m[0] > -30
        ]

        # Retângulo do personagem
        player_rect = pygame.Rect(
            jogo["player_x"],
            jogo["player_y"],
            60,
            60
        )

        # Colisão com moedas
        for moeda in jogo["moedas"]:

            moeda_rect = pygame.Rect(
                moeda[0],
                moeda[1],
                30,
                30
            )

            if player_rect.colliderect(moeda_rect):
                jogo["moedas_coletadas"] += 1
                jogo["pontos"] += 25
                jogo["moedas"].remove(moeda)
                break

        # Colisão com obstáculos
        for obs in jogo["obstaculos"]:

            obstaculo_rect = pygame.Rect(
                obs[0],
                obs[1],
                50,
                50
            )

            if player_rect.colliderect(obstaculo_rect):

                salvar_ranking(
                    nome_jogador,
                    jogo["pontos"]
                )

                ranking = carregar_ranking()
                estado = "game_over"
                break

        if estado == "game_over":
            continue

        # Colisão e pouso nos blocos
        for bloco in jogo["blocos"]:

            bloco_rect = pygame.Rect(
                bloco[0],
                bloco[1],
                60,
                20
            )

            if player_rect.colliderect(bloco_rect):

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

        # Pontuação
        jogo["pontos"] += 1

        # Desenha o personagem
        tela.blit(
            player_img,
            (
                jogo["player_x"],
                jogo["player_y"]
            )
        )

        # Desenha os obstáculos
        for obs in jogo["obstaculos"]:
            tela.blit(
                obstaculo_img,
                (obs[0], obs[1])
            )

        # Desenha os blocos
        for bloco in jogo["blocos"]:
            tela.blit(
                bloco_img,
                (bloco[0], bloco[1])
            )

        # Desenha as moedas
        for moeda in jogo["moedas"]:

            centro_x = int(moeda[0] + 15)
            centro_y = int(moeda[1] + 15)

            pygame.draw.circle(
                tela,
                AMARELO,
                (centro_x, centro_y),
                15
            )

            pygame.draw.circle(
                tela,
                BRANCO,
                (centro_x - 5, centro_y - 5),
                4
            )

        # HUD
        texto = fonte.render(
            f"Pontos: {jogo['pontos']}   "
            f"Moedas: {jogo['moedas_coletadas']}",
            True,
            BRANCO
        )

        tela.blit(texto, (10, 10))

    # =========================
    # GAME OVER
    # =========================

    elif estado == "game_over":

        tela.blit(game_over_img, (0, 0))

        titulo = fonte_grande.render(
            "GAME OVER",
            True,
            (220, 30, 30)
        )

        titulo_rect = titulo.get_rect(
            center=(400, 65)
        )

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

        tela.blit(titulo, titulo_rect)

        nome = fonte.render(
            f"Jogador: {nome_jogador}",
            True,
            BRANCO
        )

        tela.blit(
            nome,
            nome.get_rect(
                center=(400, 130)
            )
        )

        pontos = fonte.render(
            f"Pontos: {jogo['pontos']}",
            True,
            BRANCO
        )

        tela.blit(
            pontos,
            pontos.get_rect(
                center=(400, 165)
            )
        )

        moedas = fonte.render(
            f"Moedas coletadas: {jogo['moedas_coletadas']}",
            True,
            BRANCO
        )

        tela.blit(
            moedas,
            moedas.get_rect(
                center=(400, 200)
            )
        )

        cor_jogar = (
            (50, 180, 70)
            if BOTAO_JOGAR_NOVAMENTE.collidepoint(
                mouse_pos
            )
            else BRANCO
        )

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

        tela.blit(
            texto_jogar,
            texto_jogar.get_rect(
                center=BOTAO_JOGAR_NOVAMENTE.center
            )
        )

        cor_menu = (
            (50, 180, 70)
            if BOTAO_MENU_GAME_OVER.collidepoint(
                mouse_pos
            )
            else BRANCO
        )

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

        tela.blit(
            texto_menu,
            texto_menu.get_rect(
                center=BOTAO_MENU_GAME_OVER.center
            )
        )

    # Desenha a tela e adapta à janela
    mostrar_tela(
        tela,
        janela,
        LARGURA,
        ALTURA,
        PRETO
    )

    pygame.display.flip()

pygame.quit()
