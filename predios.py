import os
import random
import pygame


# =========================================================
# CAMINHOS
# =========================================================

PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))

PASTA_PREDIOS = os.path.join(
    PASTA_PROJETO,
    "assets",
    "imagens",
    "predios"
)

BASE_PREDIOS = 410


# =========================================================
# CONFIGURAÇÕES DOS PRÉDIOS
# =========================================================

CONFIGURACAO_PREDIOS = {
    1: {
        "escala": 1.20,
        "telhado": 59,
        "obstaculos": [
            (45, 34, 75, 27),
            (199, 0, 9, 62)
        ]
    },

    2: {
        "escala": 1.05,
        "telhado": 151,
        "obstaculos": [
            (12, 115, 255, 35),
            (190, 0, 58, 132)
        ]
    },

    3: {
        "escala": 1.05,
        "telhado": 80,
        "obstaculos": [
            (48, 43, 135, 34),
            (198, 0, 9, 78)
        ]
    },

    4: {
        "escala": 0.95,
        "telhado": 168,
        "obstaculos": [
            (48, 125, 75, 25),
            (125, 0, 83, 150),
            (215, 130, 42, 25)
        ]
    },

    5: {
        "escala": 1.00,
        "telhado": 168,
        "obstaculos": [
            (85, 20, 145, 130),
            (15, 140, 245, 25)
        ]
    },

    6: {
        "escala": 0.95,
        "telhado": 137,
        "obstaculos": [
            (40, 27, 130, 25)
        ]
    },

    7: {
        "escala": 1.00,
        "telhado": 208,
        "obstaculos": [
            (0, 135, 395, 34),
            (238, 0, 13, 150),
            (270, 115, 65, 45)
        ]
    },

    8: {
        "escala": 1.00,
        "telhado": 120,
        "obstaculos": [
            (215, 15, 75, 125),
            (300, 25, 13, 110),
            (12, 60, 58, 50)
        ]
    },

    9: {
        "escala": 1.25,
        "telhado": 1,
        "obstaculos": []
    },

    10: {
        "escala": 1.15,
        "telhado": 70,
        "obstaculos": [
            (105, 20, 65, 35),
            (205, 0, 13, 65)
        ]
    },

    11: {
        "escala": 0.95,
        "telhado": 76,
        "obstaculos": [
            (20, 0, 100, 35),
            (110, 25, 430, 35),
            (540, 0, 15, 60)
        ]
    }
}


# =========================================================
# CONTAGEM DE APARIÇÕES
# =========================================================

CONTAGEM_PREDIOS = {}


# =========================================================
# CARREGAR IMAGENS DOS PRÉDIOS
# =========================================================

def carregar_predios():

    modelos_predios = []

    for numero in range(1, 12):

        caminho = os.path.join(
            PASTA_PREDIOS,
            f"predio_{numero:02d}.png"
        )

        try:

            imagem = pygame.image.load(caminho).convert_alpha()

            configuracao = CONFIGURACAO_PREDIOS[numero]

            escala = configuracao["escala"]

            largura_original = imagem.get_width()
            altura_original = imagem.get_height()

            nova_largura = int(largura_original * escala)
            nova_altura = int(altura_original * escala)

            imagem = pygame.transform.smoothscale(
                imagem,
                (nova_largura, nova_altura)
            )

            telhado = int(
                configuracao["telhado"] * escala
            )

            obstaculos = []

            for obstaculo in configuracao["obstaculos"]:

                x, y, largura, altura = obstaculo

                obstaculos.append((
                    int(x * escala),
                    int(y * escala),
                    int(largura * escala),
                    int(altura * escala)
                ))

            modelo = {
                "imagem": imagem,
                "telhado": telhado,
                "numero": numero,
                "escala": escala,
                "obstaculos": obstaculos
            }

            modelos_predios.append(modelo)

            print(
                f"Prédio {numero:02d} carregado: "
                f"{nova_largura}x{nova_altura} | "
                f"Telhado: {telhado} | "
                f"Obstáculos: {len(obstaculos)}"
            )

        except Exception as erro:

            print(
                f"Erro ao carregar prédio {numero:02d}: {erro}"
            )

    print(
        f"\nTotal de prédios carregados: "
        f"{len(modelos_predios)} de 11\n"
    )

    return modelos_predios


# =========================================================
# LARGURA DO PRÉDIO
# =========================================================

def largura_predio(predio):

    return predio["imagem"].get_width()


# =========================================================
# ALTURA DO TELHADO
# =========================================================

def altura_telhado(modelo, base_y=BASE_PREDIOS):

    altura_imagem = modelo["imagem"].get_height()

    return (
        base_y
        - altura_imagem
        + modelo["telhado"]
    )


# =========================================================
# ESCOLHER PRÉDIO
# =========================================================

def escolher_predio_compativel(
    modelos_predios,
    telhado_anterior=None,
    base_y=BASE_PREDIOS
):

    if not modelos_predios:

        raise ValueError(
            "Nenhum modelo de prédio foi carregado."
        )

    # No primeiro prédio, todos os modelos podem ser escolhidos.
    if telhado_anterior is None:

        candidatos = modelos_predios

    else:

        candidatos = []

        # Primeiro, procura prédios com diferença de altura
        # de até 55 pixels em relação ao anterior.
        for modelo in modelos_predios:

            telhado_atual = altura_telhado(
                modelo,
                base_y
            )

            diferenca = abs(
                telhado_atual - telhado_anterior
            )

            if diferenca <= 55:

                candidatos.append(modelo)

        # Se nenhum prédio for compatível, escolhe os
        # que possuem a menor diferença de altura.
        if not candidatos:

            diferencas = {
                modelo["numero"]: abs(
                    altura_telhado(modelo, base_y)
                    - telhado_anterior
                )
                for modelo in modelos_predios
            }

            menor_diferenca = min(
                diferencas.values()
            )

            candidatos = [
                modelo
                for modelo in modelos_predios
                if diferencas[modelo["numero"]]
                == menor_diferenca
            ]

    # Descobre qual prédio apareceu menos vezes.
    menor_contagem = min(
        CONTAGEM_PREDIOS.get(
            modelo["numero"],
            0
        )
        for modelo in candidatos
    )

    # Mantém apenas os prédios menos utilizados.
    menos_utilizados = [
        modelo
        for modelo in candidatos
        if CONTAGEM_PREDIOS.get(
            modelo["numero"],
            0
        ) == menor_contagem
    ]

    # Sorteia entre os menos utilizados.
    return random.choice(menos_utilizados)


# =========================================================
# CRIAR PRÉDIO
# =========================================================

def criar_predio(
    x,
    base_y,
    modelos_predios,
    modelo=None
):

    if not modelos_predios:

        raise ValueError(
            "Não existem prédios carregados."
        )

    if modelo is None:

        modelo = escolher_predio_compativel(
            modelos_predios,
            None,
            base_y
        )

    imagem = modelo["imagem"]

    imagem_y = base_y - imagem.get_height()

    telhado_y = (
        imagem_y
        + modelo["telhado"]
    )

    obstaculos = []

    for obstaculo in modelo["obstaculos"]:

        ox, oy, largura, altura = obstaculo

        # Os obstáculos são dicionários porque o main.py
        # acessa suas posições por "x", "y", "largura" e "altura".
        obstaculos.append({
            "x": int(x + ox),
            "y": int(imagem_y + oy),
            "largura": largura,
            "altura": altura
        })

    predio = {
        "x": float(x),
        "y": imagem_y,
        "base_y": base_y,
        "telhado_y": telhado_y,
        "imagem": imagem,
        "telhado_offset": modelo["telhado"],
        "numero": modelo["numero"],
        "obstaculos": obstaculos,
        "id": random.randint(100000, 999999)
    }

    # Registra que esse modelo apareceu.
    numero_predio = modelo["numero"]

    CONTAGEM_PREDIOS[numero_predio] = (
        CONTAGEM_PREDIOS.get(
            numero_predio,
            0
        ) + 1
    )

    return predio


# =========================================================
# CRIAR MOEDAS SOBRE O TELHADO
# =========================================================

def criar_moedas_predio(predio):

    moedas = []

    largura = largura_predio(predio)

    telhado_y = predio["telhado_y"]

    # Todas as moedas ficam na mesma altura.
    moeda_y = int(telhado_y - 35)

    # Espaços possíveis ao longo do telhado.
    inicio_x = int(predio["x"] + 20)
    final_x = int(predio["x"] + largura - 35)

    candidatos = []

    for x in range(inicio_x, final_x, 35):

        moeda_rect = pygame.Rect(
            x,
            moeda_y,
            25,
            25
        )

        espaco_livre = True

        # Não coloca moeda dentro de obstáculos.
        for obstaculo in predio.get("obstaculos", []):

            obstaculo_rect = pygame.Rect(
                obstaculo["x"],
                obstaculo["y"],
                obstaculo["largura"],
                obstaculo["altura"]
            )

            if moeda_rect.colliderect(obstaculo_rect):
                espaco_livre = False
                break

        if espaco_livre:
            candidatos.append([x, moeda_y])

    if candidatos:

        quantidade = min(
            random.randint(1, 3),
            len(candidatos)
        )

        moedas = random.sample(
            candidatos,
            quantidade
        )

    print(
        f"Prédio: {predio['numero']} | "
        f"Telhado Y: {predio['telhado_y']} | "
        f"Moedas: {moedas}"
    )
    
    return moedas