
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

pygame.init()

# =====================================
# CONFIGURAÇÕES
# =====================================

LARGURA = 800
ALTURA = 500
TAMANHO_PLAYER = 60

tela = pygame.Surface((LARGURA, ALTURA))
janela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)

pygame.display.set_caption("Jump Homem-Aranha")
clock = pygame.time.Clock()

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 215, 0)

fonte = pygame.font.SysFont(None, 36)
fonte_grande = pygame.font.SysFont(None, 60)

CHAO_Y = 420

BOTAO_JOGAR = pygame.Rect(250, 270, 300, 50)
BOTAO_RANKING = pygame.Rect(250, 335, 300, 50)
BOTAO_SAIR = pygame.Rect(250, 400, 300, 50)

BOTAO_JOGAR_NOVAMENTE = pygame.Rect(200, 270, 400, 50)
BOTAO_MENU_GAME_OVER = pygame.Rect(200, 330, 400, 50)

tela_cheia = False

ranking = carregar_ranking()
ranking_cortina = RankingCortina()

# =====================================
# CARREGAMENTO DAS IMAGENS
# =====================================

PASTA_IMAGENS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "imagens"
)


def carregar_imagem(nome, tamanho=None, alpha=False):

    caminho = os.path.join(PASTA_IMAGENS, nome)

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


# =====================================
# CARREGAR E RECORTAR OS PRÉDIOS
# =====================================

CAIXAS_PREDIOS = [
    (955, 17, 1235, 395, 180),
    (1277, 84, 1551, 395, 240),
    (296, 127, 581, 395, 228),
    (634, 157, 871, 394, 226),
    (8, 236, 259, 394, 294),
    (654, 410, 1049, 713, 576),
    (1115, 418, 1498, 719, 535),
    (29, 528, 556, 713, 570),
    (298, 774, 559, 965, 847),
    (978, 784, 1548, 965, 833),
    (39, 820, 201, 965, 820)
]

predios_imagens = []


def criar_predio_fallback():

    imagem = pygame.Surface(
        (300, 180),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        imagem,
        (25, 35, 100),
        (0, 35, 300, 145)
    )

    pygame.draw.rect(
        imagem,
        (45, 65, 150),
        (0, 25, 300, 22)
    )

    for x in (35, 105, 175, 245):

        pygame.draw.rect(
            imagem,
            (255, 170, 55),
            (x, 75, 25, 45)
        )

    return {
        "imagem": imagem,
        "telhado": 25
    }


try:

    predios_folha = carregar_imagem(
        "predios_transparentes.png",
        alpha=True
    )

    for x1, y1, x2, y2, telhado_original in CAIXAS_PREDIOS:

        recorte = predios_folha.subsurface(
            (x1, y1, x2 - x1, y2 - y1)
        ).copy()

        escala = min(
            360 / recorte.get_width(),
            220 / recorte.get_height()
        )

        novo_tamanho = (
            max(1, int(recorte.get_width() * escala)),
            max(1, int(recorte.get_height() * escala))
        )

        recorte = pygame.transform.smoothscale(
            recorte,
            novo_tamanho
        )

        deslocamento_telhado = int(
            (telhado_original - y1) * escala
        )

        predios_imagens.append({
            "imagem": recorte,
            "telhado": deslocamento_telhado
        })

    print("Prédios carregados:", len(predios_imagens))

except Exception as erro:

    print("Erro ao carregar os prédios:", erro)

    predios_imagens = [
        criar_predio_fallback()
    ]


# =====================================
# FUNÇÕES DOS PRÉDIOS
# =====================================

def largura_predio(predio):

    return predio["imagem"].get_width()


def criar_predio(x, altura_telhado, modelo=None):

    if modelo is None:
        modelo = random.choice(predios_imagens)

    return {
        "x": float(x),
        "telhado_y": int(altura_telhado),
        "imagem": modelo["imagem"],
        "telhado_offset": modelo["telhado"],
        "id": random.randint(1, 1000000000)
    }


def criar_moedas_predio(predio):

    moedas = []

    largura = largura_predio(predio)

    quantidade = random.randint(1, 3)

    for i in range(quantidade):

        x = (
            predio["x"]
            + largura * 0.30
            + i * 38
        )

        y = predio["telhado_y"] - random.randint(65, 90)

        moedas.append([x, y])

    return moedas


# =====================================
# REINICIAR JOGO
# =====================================

def resetar_jogo():

    modelo_inicial = max(
        predios_imagens,
        key=lambda modelo: modelo["imagem"].get_width()
    )

    primeiro_predio = criar_predio(
        0,
        CHAO_Y,
        modelo_inicial
    )

    return {

        "player_x": 100.0,
        "player_y": CHAO_Y - TAMANHO_PLAYER,

        "vel_y": 0.0,
        "gravidade": 0.7,

        "no_chao": True,
        "tempo_pulo": 0,

        "em_cima_de": primeiro_predio["id"],

        "predios": [primeiro_predio],

        "moedas": [
            [220, CHAO_Y - 85],
            [260, CHAO_Y - 85]
        ],

        "moedas_coletadas": 0,
        "pontos": 0,

        "velocidade_base": 2.0
    }


# =====================================
# ESTADOS DO JOGO
# =====================================

estado = "menu"
nome_jogador = ""

jogo = resetar_jogo()

rodando = True


# =====================================
# LOOP PRINCIPAL
# =====================================

while rodando:

    clock.tick(60)

    # =================================
    # EVENTOS
    # =================================

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

    # =================================
    # MENU PRINCIPAL
    # =================================

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

    # =================================
    # RANKING
    # =================================

    elif estado == "ranking":

        ranking_cortina.atualizar()
        ranking_cortina.desenhar(tela, ranking)

    # =================================
    # JOGO - FASE DA CIDADE
    # =================================

    elif estado == "jogo":

        teclas = pygame.key.get_pressed()

        player_y_anterior = jogo["player_y"]

        # Fundo parado
        tela.blit(fundo_img, (0, 0))

        # ---------------------------------
        # MOVIMENTO HORIZONTAL
        # ---------------------------------

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jogo["player_x"] -= 4.5

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jogo["player_x"] += 4.5

        jogo["player_x"] = max(
            0,
            min(jogo["player_x"], LARGURA - TAMANHO_PLAYER)
        )

        # ---------------------------------
        # PULO
        # ---------------------------------

        if (
            teclas[pygame.K_SPACE]
            and jogo["no_chao"]
        ):

            jogo["vel_y"] = -15
            jogo["no_chao"] = False
            jogo["tempo_pulo"] = 0
            jogo["em_cima_de"] = None

        if (
            teclas[pygame.K_SPACE]
            and not jogo["no_chao"]
        ):

            if jogo["tempo_pulo"] < 8:

                jogo["vel_y"] -= 0.35
                jogo["tempo_pulo"] += 1

        # ---------------------------------
        # VELOCIDADE PROGRESSIVA
        # ---------------------------------

        velocidade = min(
            jogo["velocidade_base"]
            + (jogo["pontos"] // 500) * 0.25,
            5.5
        )

        # O prédio e o personagem se deslocam juntos
        # enquanto o personagem está apoiado no telhado.
        if jogo["em_cima_de"] is not None:

            for predio in jogo["predios"]:

                if predio["id"] == jogo["em_cima_de"]:

                    jogo["player_x"] -= velocidade
                    break

        # ---------------------------------
        # GRAVIDADE
        # ---------------------------------

        jogo["vel_y"] += jogo["gravidade"]
        jogo["player_y"] += jogo["vel_y"]

        jogo["no_chao"] = False

        # ---------------------------------
        # MOVIMENTAR PRÉDIOS
        # ---------------------------------

        for predio in jogo["predios"]:
            predio["x"] -= velocidade

        # ---------------------------------
        # MOVIMENTAR MOEDAS
        # ---------------------------------

        for moeda in jogo["moedas"]:
            moeda[0] -= velocidade

        # ---------------------------------
        # CRIAR NOVOS PRÉDIOS
        # ---------------------------------

        ultimo_predio = jogo["predios"][-1]

        if (
            ultimo_predio["x"]
            + largura_predio(ultimo_predio)
            + 95 < LARGURA
        ):

            distancia = random.randint(75, 115)

            novo_x = (
                ultimo_predio["x"]
                + largura_predio(ultimo_predio)
                + distancia
            )

            nova_altura = random.randint(365, 420)

            novo_predio = criar_predio(
                novo_x,
                nova_altura
            )

            jogo["predios"].append(novo_predio)

            jogo["moedas"].extend(
                criar_moedas_predio(novo_predio)
            )

        # ---------------------------------
        # REMOVER PRÉDIOS FORA DA TELA
        # ---------------------------------

        jogo["predios"] = [
            predio
            for predio in jogo["predios"]
            if predio["x"] + largura_predio(predio) > -60
        ]

        # ---------------------------------
        # REMOVER MOEDAS FORA DA TELA
        # ---------------------------------

        jogo["moedas"] = [
            moeda
            for moeda in jogo["moedas"]
            if moeda[0] > -35
        ]

        # ---------------------------------
        # COLISÃO COM OS TELHADOS
        # ---------------------------------

        player_rect = pygame.Rect(
            int(jogo["player_x"]),
            int(jogo["player_y"]),
            TAMANHO_PLAYER,
            TAMANHO_PLAYER
        )

        for predio in jogo["predios"]:

            topo_telhado = predio["telhado_y"]

            telhado_rect = pygame.Rect(
                int(predio["x"] + 8),
                topo_telhado - 8,
                max(1, largura_predio(predio) - 16),
                12
            )

            chegou_por_cima = (
                jogo["vel_y"] >= 0
                and player_y_anterior + TAMANHO_PLAYER
                <= topo_telhado + 12
            )

            if (
                player_rect.colliderect(telhado_rect)
                and chegou_por_cima
            ):

                jogo["player_y"] = (
                    topo_telhado - TAMANHO_PLAYER
                )

                jogo["vel_y"] = 0
                jogo["no_chao"] = True
                jogo["em_cima_de"] = predio["id"]

                player_rect.y = int(jogo["player_y"])

                break

        # Verifica se ainda está apoiado no prédio.
        if jogo["em_cima_de"] is not None and not jogo["no_chao"]:

            jogo["em_cima_de"] = None

        if jogo["em_cima_de"] is not None and not jogo["no_chao"]:

            for predio in jogo["predios"]:

                if predio["id"] == jogo["em_cima_de"]:

                    faixa = pygame.Rect(
                        int(predio["x"] + 8),
                        predio["telhado_y"] - 4,
                        max(1, largura_predio(predio) - 16),
                        8
                    )

                    if player_rect.colliderect(faixa):

                        jogo["player_y"] = (
                            predio["telhado_y"] - TAMANHO_PLAYER
                        )

                        jogo["vel_y"] = 0
                        jogo["no_chao"] = True

                    else:

                        jogo["em_cima_de"] = None

                    break

        player_rect = pygame.Rect(
            int(jogo["player_x"]),
            int(jogo["player_y"]),
            TAMANHO_PLAYER,
            TAMANHO_PLAYER
        )

        # ---------------------------------
        # COLETAR MOEDAS
        # ---------------------------------

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

        # ---------------------------------
        # DERROTA AO CAIR
        # ---------------------------------

        if jogo["player_y"] > ALTURA:

            salvar_ranking(
                nome_jogador,
                jogo["pontos"]
            )

            ranking = carregar_ranking()

            estado = "game_over"

        if estado == "game_over":
            continue

        # ---------------------------------
        # PONTUAÇÃO
        # ---------------------------------

        jogo["pontos"] += 1

        # ---------------------------------
        # DESENHAR PRÉDIOS
        # ---------------------------------

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

        # ---------------------------------
        # DESENHAR MOEDAS
        # ---------------------------------

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
                (centro[0] - 4, centro[1] - 4),
                3
            )

        # ---------------------------------
        # DESENHAR PERSONAGEM
        # ---------------------------------

        tela.blit(
            player_img,
            (
                int(jogo["player_x"]),
                int(jogo["player_y"])
            )
        )

        # ---------------------------------
        # HUD
        # ---------------------------------

        texto = fonte.render(
            f"Pontos: {jogo['pontos']}   "
            f"Moedas: {jogo['moedas_coletadas']}",
            True,
            BRANCO
        )

        tela.blit(texto, (10, 10))

    # =================================
    # GAME OVER
    # =================================

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
            nome.get_rect(center=(400, 130))
        )

        pontos = fonte.render(
            f"Pontos: {jogo['pontos']}",
            True,
            BRANCO
        )

        tela.blit(
            pontos,
            pontos.get_rect(center=(400, 165))
        )

        moedas = fonte.render(
            f"Moedas coletadas: {jogo['moedas_coletadas']}",
            True,
            BRANCO
        )

        tela.blit(
            moedas,
            moedas.get_rect(center=(400, 200))
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

    # =================================
    # ATUALIZAR TELA
    # =================================

    mostrar_tela(
        tela,
        janela,
        LARGURA,
        ALTURA,
        PRETO
    )

    pygame.display.flip()


pygame.quit()
