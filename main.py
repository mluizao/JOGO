import pygame
import os
import random

from ranking import carregar_ranking, salvar_ranking

from cortina import (
    converter_mouse,
    mostrar_tela,
    alternar_tela_cheia,
    RankingCortina
)

from predios import (
    carregar_predios,
    largura_predio,
    criar_predio,
    escolher_predio_compativel
)

from obstaculo import Teia
from caixas import carregar_caixa, adicionar_caixa_no_predio
from colisoes import resolver_colisoes
from animacao import AnimacaoPlayer

animacao_player = AnimacaoPlayer()


pygame.init()

# =========================================================
# CONFIGURAÇÕES
# =========================================================

LARGURA = 800
ALTURA = 500
TAMANHO_PLAYER = 60

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

CHAO_Y = 410

LIMITE_CAMERA_ESQUERDA = 180
LIMITE_CAMERA_DIREITA = 430

VELOCIDADE_PARALLAX = 0.25

BOTAO_JOGAR = pygame.Rect(250, 270, 300, 50)
BOTAO_RANKING = pygame.Rect(250, 335, 300, 50)
BOTAO_SAIR = pygame.Rect(250, 400, 300, 50)

BOTAO_JOGAR_NOVAMENTE = pygame.Rect(200, 270, 400, 50)
BOTAO_MENU_GAME_OVER = pygame.Rect(200, 330, 400, 50)

tela_cheia = False

ranking = carregar_ranking()
ranking_cortina = RankingCortina()


# =========================================================
# CAMINHO DAS IMAGENS
# =========================================================

PASTA_IMAGENS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "imagens"
)


def carregar_imagem(nome, tamanho=None, alpha=False):

    caminho = os.path.join(
        PASTA_IMAGENS,
        nome
    )

    imagem = pygame.image.load(caminho)

    if alpha:
        imagem = imagem.convert_alpha()
    else:
        imagem = imagem.convert()

    if tamanho:
        imagem = pygame.transform.smoothscale(
            imagem,
            tamanho
        )

    return imagem


# =========================================================
# CARREGAMENTO DAS IMAGENS
# =========================================================

try:

    fundo_menu = carregar_imagem(
        "fundo_menu.png",
        (800, 500)
    )

    game_over_img = carregar_imagem(
        "game_over.png",
        (800, 500)
    )

    player_img = carregar_imagem(
        "player.png",
        (60, 60),
        alpha=True
    )

    fundo_img = carregar_imagem(
        "fundo_cidade.png",
        (800, 500)
    )

except Exception as erro:

    print("Erro ao carregar imagem:", erro)

    fundo_menu = pygame.Surface((800, 500))
    fundo_menu.fill((20, 20, 35))

    game_over_img = pygame.Surface((800, 500))
    game_over_img.fill((20, 20, 35))

    player_img = pygame.Surface(
        (60, 60),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        player_img,
        (255, 0, 0),
        (5, 5, 50, 55)
    )

    fundo_img = pygame.Surface((800, 500))
    fundo_img.fill((35, 30, 70))


# Carrega a caixa pelo arquivo caixas.py.
caixa_img = carregar_caixa()

# Carrega os modelos dos prédios.
predios_imagens = carregar_predios()


# =========================================================
# RESETAR JOGO
# =========================================================

def resetar_jogo():

    modelo_inicial = max(
        predios_imagens,
        key=lambda modelo: modelo["imagem"].get_width()
    )

    primeiro_predio = criar_predio(
        0,
        CHAO_Y,
        predios_imagens,
        modelo_inicial
    )

    jogo_novo = {

        "player_x": 100.0,
        "direcao_player": 1,  # 1 = direita; -1 = esquerda

        "player_y": (
            primeiro_predio["telhado_y"]
            - TAMANHO_PLAYER
        ),

        "vel_y": 0.0,
        "gravidade": 0.7,
        "no_chao": True,
        "tempo_pulo": 0,

        "em_cima_de": primeiro_predio["id"],

        "predios": [primeiro_predio],

        "caixas": [],
        "teias": [],
        "moedas": [],

        "moedas_coletadas": 0,
        "pontos": 0,

        "velocidade_base": 2.0,

        "camera_x": 0.0,
        "fundo_x": 0.0
    }

    adicionar_caixa_no_predio(
        jogo_novo,
        primeiro_predio,
        caixa_img
    )

    return jogo_novo


# =========================================================
# ESTADOS DO JOGO
# =========================================================

estado = "menu"

nome_jogador = ""

jogo = resetar_jogo()

rodando = True


# =========================================================
# LOOP PRINCIPAL
# =========================================================

while rodando:

    clock.tick(60)

    # =====================================================
    # EVENTOS
    # =====================================================

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

            elif estado == "jogo":

                # F lança a teia.
                if evento.key == pygame.K_f:

                    jogo["teias"].append(
                        Teia(
                            jogo["player_x"] + TAMANHO_PLAYER,
                            jogo["player_y"] + 30
                        )
                    )

            elif estado == "ranking":

                if evento.key == pygame.K_ESCAPE:
                    estado = "menu"

            elif estado == "game_over":

                if evento.key == pygame.K_RETURN:

                    jogo = resetar_jogo()
                    estado = "jogo"

                elif evento.key == pygame.K_ESCAPE:

                    estado = "menu"

        # =================================================
        # CLIQUES DO MOUSE
        # =================================================

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
                and BOTAO_JOGAR_NOVAMENTE.collidepoint(mouse_pos)
            ):

                jogo = resetar_jogo()
                estado = "jogo"

            elif (
                estado == "game_over"
                and BOTAO_MENU_GAME_OVER.collidepoint(mouse_pos)
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

    # =====================================================
    # MENU
    # =====================================================

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

    # =====================================================
    # RANKING
    # =====================================================

    elif estado == "ranking":

        ranking_cortina.atualizar()

        ranking_cortina.desenhar(
            tela,
            ranking
        )

    # =====================================================
    # JOGO
    # =====================================================

    elif estado == "jogo":

        teclas = pygame.key.get_pressed()

        player_y_anterior = jogo["player_y"]
        player_x_anterior = jogo["player_x"]
        no_chao_anterior = jogo["no_chao"]

        velocidade = min(
            jogo["velocidade_base"]
            + (jogo["pontos"] // 500) * 0.25,
            5.5
        )

        # -----------------------------------------------
        # MOVIMENTAÇÃO DO JOGADOR
        # -----------------------------------------------

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jogo["player_x"] -= 4.5
            jogo["direcao_player"] = -1

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jogo["player_x"] += 4.5
            jogo["direcao_player"] = 1

        jogo["player_x"] = max(
            0,
            jogo["player_x"]
        )

        # -----------------------------------------------
        # PULO
        # -----------------------------------------------

        if teclas[pygame.K_SPACE] and jogo["no_chao"]:

            jogo["vel_y"] = -15
            jogo["no_chao"] = False
            jogo["tempo_pulo"] = 0
            jogo["em_cima_de"] = None

        if teclas[pygame.K_SPACE] and not jogo["no_chao"]:

            if jogo["tempo_pulo"] < 8:

                jogo["vel_y"] -= 0.35
                jogo["tempo_pulo"] += 1

        jogo["vel_y"] += jogo["gravidade"]

        jogo["player_y"] += jogo["vel_y"]

        jogo["no_chao"] = False

        # -----------------------------------------------
        # MOVIMENTAÇÃO DOS PRÉDIOS
        # -----------------------------------------------

        for predio in jogo["predios"]:

            predio["x"] -= velocidade

            for obstaculo in predio["obstaculos"]:
                obstaculo["x"] -= velocidade

        # -----------------------------------------------
        # MOVIMENTAÇÃO DAS MOEDAS
        # -----------------------------------------------

        for moeda in jogo["moedas"]:
            moeda[0] -= velocidade

        # -----------------------------------------------
        # MOVIMENTAÇÃO DAS CAIXAS
        # -----------------------------------------------

        for caixa in jogo["caixas"]:
            caixa.mover(velocidade)

        # -----------------------------------------------
        # MOVIMENTAÇÃO DAS TEIAS
        # -----------------------------------------------

        for teia in jogo["teias"]:
            teia.mover()

        # -----------------------------------------------
        # CÂMERA
        # -----------------------------------------------

        deslocamento_camera = 0.0

        if jogo["player_x"] > LIMITE_CAMERA_DIREITA:

            deslocamento_camera = (
                jogo["player_x"] - LIMITE_CAMERA_DIREITA
            )

        elif jogo["player_x"] < LIMITE_CAMERA_ESQUERDA:

            deslocamento_camera = (
                jogo["player_x"] - LIMITE_CAMERA_ESQUERDA
            )

        if deslocamento_camera != 0:

            jogo["player_x"] -= deslocamento_camera

            for predio in jogo["predios"]:

                predio["x"] -= deslocamento_camera

                for obstaculo in predio.get("obstaculos", []):
                    obstaculo["x"] -= deslocamento_camera

            for moeda in jogo["moedas"]:
                moeda[0] -= deslocamento_camera

            for caixa in jogo["caixas"]:
                caixa.x -= deslocamento_camera

            for teia in jogo["teias"]:
                teia.x -= deslocamento_camera

            jogo["camera_x"] += deslocamento_camera

        # -----------------------------------------------
        # FUNDO
        # -----------------------------------------------

        movimento_fundo = (
            velocidade + deslocamento_camera
        ) * VELOCIDADE_PARALLAX

        jogo["fundo_x"] = (
            jogo["fundo_x"] + movimento_fundo
        ) % LARGURA

        fundo_x = int(jogo["fundo_x"])

        tela.blit(
            fundo_img,
            (-fundo_x, 0)
        )

        tela.blit(
            fundo_img,
            (LARGURA - fundo_x, 0)
        )

        # -----------------------------------------------
        # CRIAR NOVOS PRÉDIOS
        # -----------------------------------------------

        ultimo_predio = jogo["predios"][-1]

        if (
            ultimo_predio["x"]
            + largura_predio(ultimo_predio)
            + 60
            < LARGURA
        ):

            distancia = random.randint(45, 75)

            novo_x = (
                ultimo_predio["x"]
                + largura_predio(ultimo_predio)
                + distancia
            )

            modelo = escolher_predio_compativel(
                predios_imagens,
                ultimo_predio["telhado_y"],
                CHAO_Y
            )

            novo_predio = criar_predio(
                novo_x,
                CHAO_Y,
                predios_imagens,
                modelo
            )

            jogo["predios"].append(novo_predio)

            # A criação das caixas fica no arquivo caixas.py.
            adicionar_caixa_no_predio(
                jogo,
                novo_predio,
                caixa_img
            )

        # -----------------------------------------------
        # REMOVER PRÉDIOS FORA DA TELA
        # -----------------------------------------------

        jogo["predios"] = [
            predio
            for predio in jogo["predios"]
            if predio["x"] + largura_predio(predio) > -60
        ]

        # -----------------------------------------------
        # REMOVER OBJETOS FORA DA TELA
        # -----------------------------------------------

        jogo["moedas"] = [
            moeda
            for moeda in jogo["moedas"]
            if moeda[0] > -35
        ]

        jogo["caixas"] = [
            caixa
            for caixa in jogo["caixas"]
            if caixa.x > -60 and caixa.ativa
        ]

        jogo["teias"] = [
            teia
            for teia in jogo["teias"]
            if not teia.saiu_da_tela()
        ]

        # -----------------------------------------------
        # COLISÕES DO JOGADOR
        # -----------------------------------------------

        velocidade_impacto = jogo["vel_y"]

        resolver_colisoes(
            jogo,
            velocidade,
            deslocamento_camera,
            player_x_anterior,
            player_y_anterior
        )

        if not no_chao_anterior and jogo["no_chao"]:
            animacao_player.pousar(velocidade_impacto)

        animacao_player.atualizar(
            jogo["no_chao"],
            jogo["vel_y"],
            velocidade
        )

        # -----------------------------------------------
        # COLISÃO DA TEIA COM AS CAIXAS
        # -----------------------------------------------

        for teia in jogo["teias"][:]:

            acertou_caixa = False

            for caixa in jogo["caixas"][:]:

                if teia.rect().colliderect(caixa.rect()):

                    caixa.ativa = False

                    # Recompensa em moedas.
                    jogo["moedas"].append([
                        int(caixa.x),
                        int(caixa.y)
                    ])

                    # Pontuação por destruir a caixa.
                    jogo["pontos"] += 50

                    if teia in jogo["teias"]:
                        jogo["teias"].remove(teia)

                    acertou_caixa = True

                    break

            if acertou_caixa:
                continue

        # -----------------------------------------------
        # REMOVER CAIXAS DESTRUÍDAS
        # -----------------------------------------------

        jogo["caixas"] = [
            caixa
            for caixa in jogo["caixas"]
            if caixa.ativa
        ]

        # -----------------------------------------------
        # COLETAR MOEDAS
        # -----------------------------------------------

        player_rect = pygame.Rect(
            int(jogo["player_x"]),
            int(jogo["player_y"]),
            TAMANHO_PLAYER,
            TAMANHO_PLAYER
        )

        for moeda in jogo["moedas"][:]:

            moeda_rect = pygame.Rect(
                int(moeda[0]),
                int(moeda[1]),
                25,
                25
            )

            if player_rect.colliderect(moeda_rect):

                jogo["moedas_coletadas"] += 1
                jogo["pontos"] += 25

                jogo["moedas"].remove(moeda)

        # -----------------------------------------------
        # GAME OVER
        # -----------------------------------------------

        if jogo["player_y"] > ALTURA:

            salvar_ranking(
                nome_jogador,
                jogo["pontos"]
            )

            ranking = carregar_ranking()

            estado = "game_over"

        if estado == "game_over":
            continue

        # -----------------------------------------------
        # DESENHAR PRÉDIOS
        # -----------------------------------------------

        for predio in jogo["predios"]:

            desenho_y = (
                predio["telhado_y"]
                - predio["telhado_offset"]
            )

            tela.blit(
                predio["imagem"],
                (
                    int(predio["x"]),
                    int(desenho_y)
                )
            )

        # -----------------------------------------------
        # DESENHAR CAIXAS
        # -----------------------------------------------

        for caixa in jogo["caixas"]:
            caixa.desenhar(tela)

        # -----------------------------------------------
        # DESENHAR MOEDAS
        # -----------------------------------------------

        for moeda in jogo["moedas"]:

            centro = (
                int(moeda[0] + 12),
                int(moeda[1] + 12)
            )

            pygame.draw.circle(
                tela,
                AMARELO,
                centro,
                12
            )

            pygame.draw.circle(
                tela,
                BRANCO,
                (
                    centro[0] - 4,
                    centro[1] - 4
                ),
                3
            )

        # -----------------------------------------------
        # DESENHAR TEIAS
        # -----------------------------------------------

        for teia in jogo["teias"]:
            teia.desenhar(tela)


        # -----------------------------------------------
        # DESENHAR JOGADOR
        # -----------------------------------------------

        animacao_player.desenhar(
            tela,
            player_img,
            int(jogo["player_x"]),
            int(jogo["player_y"]),
            TAMANHO_PLAYER,
            ajuste_pes=0,
            direcao=jogo["direcao_player"]
        )

        # -----------------------------------------------
        # HUD
        # -----------------------------------------------

        texto = fonte.render(
            (
                f"Pontos: {jogo['pontos']}   "
                f"Moedas: {jogo['moedas_coletadas']}"
            ),
            True,
            BRANCO
        )

        tela.blit(
            texto,
            (10, 10)
        )

        texto_teia = fonte.render(
            "F: LANCAR TEIA",
            True,
            BRANCO
        )

        tela.blit(
            texto_teia,
            (10, 45)
        )

    # =====================================================
    # GAME OVER
    # =====================================================

    elif estado == "game_over":

        tela.blit(
            game_over_img,
            (0, 0)
        )

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

        tela.blit(
            titulo,
            titulo_rect
        )

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
            if BOTAO_JOGAR_NOVAMENTE.collidepoint(mouse_pos)
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
            if BOTAO_MENU_GAME_OVER.collidepoint(mouse_pos)
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

    # =====================================================
    # ATUALIZAR TELA
    # =====================================================

    mostrar_tela(
        tela,
        janela,
        LARGURA,
        ALTURA,
        PRETO
    )

    pygame.display.flip()


pygame.quit()