import pygame

from predios import largura_predio

TAMANHO_PLAYER = 60
MARGEM_X = 12
MARGEM_TOPO = 4
PES_FOLGA = 16


def hitbox_player(x, y):
    return pygame.Rect(
        int(x) + MARGEM_X,
        int(y) + MARGEM_TOPO,
        TAMANHO_PLAYER - MARGEM_X * 2,
        TAMANHO_PLAYER - MARGEM_TOPO
    )


def rect_obstaculo(obstaculo):
    return pygame.Rect(
        int(obstaculo["x"]),
        int(obstaculo["y"]),
        int(obstaculo["largura"]),
        int(obstaculo["altura"])
    )


def _pousar(jogo, topo, id_predio):
    jogo["player_y"] = topo - TAMANHO_PLAYER
    jogo["vel_y"] = 0
    jogo["no_chao"] = True
    jogo["em_cima_de"] = id_predio


def resolver_colisoes(
    jogo,
    velocidade,
    deslocamento_camera,
    player_x_anterior,
    player_y_anterior
):
    """Resolve pousos e bloqueios laterais em obstáculos e prédios."""

    player_rect = hitbox_player(jogo["player_x"], jogo["player_y"])
    anterior = hitbox_player(
        player_x_anterior - deslocamento_camera,
        player_y_anterior
    )

    # Obstáculos colocados sobre os telhados.
    for predio in jogo["predios"]:
        for obstaculo in predio.get("obstaculos", []):
            obs = rect_obstaculo(obstaculo)
            obs_ant = obs.move(velocidade + deslocamento_camera, 0)
            pes = player_rect.inflate(-PES_FOLGA, 0)

            if (
                jogo["vel_y"] >= 0
                and anterior.bottom <= obs_ant.top + 4
                and player_rect.bottom >= obs.top
                and pes.right > obs.left
                and pes.left < obs.right
            ):
                _pousar(jogo, obs.top, predio["id"])
                player_rect = hitbox_player(jogo["player_x"], jogo["player_y"])
                continue

            if (
                jogo["vel_y"] < 0
                and anterior.top >= obs_ant.bottom
                and player_rect.top <= obs.bottom
                and player_rect.right > obs.left
                and player_rect.left < obs.right
            ):
                jogo["player_y"] = obs.bottom - MARGEM_TOPO
                jogo["vel_y"] = 0
                player_rect = hitbox_player(jogo["player_x"], jogo["player_y"])

            if player_rect.colliderect(obs):
                if anterior.right <= obs_ant.left:
                    jogo["player_x"] = obs.left - TAMANHO_PLAYER + MARGEM_X
                elif anterior.left >= obs_ant.right:
                    jogo["player_x"] = obs.right - MARGEM_X
                elif player_rect.centerx < obs.centerx:
                    jogo["player_x"] = obs.left - TAMANHO_PLAYER + MARGEM_X
                else:
                    jogo["player_x"] = obs.right - MARGEM_X
                player_rect = hitbox_player(jogo["player_x"], jogo["player_y"])

    # Telhados: pouso por cima e bloqueio das paredes laterais.
    for predio in jogo["predios"]:
        topo = int(predio["telhado_y"])
        esquerda = int(predio["x"] + 6)
        direita = int(predio["x"] + largura_predio(predio) - 6)
        pes = player_rect.inflate(-PES_FOLGA, 0)

        # O personagem só pousa se estiver descendo e atravessar o nível do telhado.
        if (
            jogo["vel_y"] >= 0
            and anterior.bottom <= topo + 4
            and player_rect.bottom >= topo
            and pes.right > esquerda
            and pes.left < direita
        ):
            _pousar(jogo, topo, predio["id"])
            player_rect = hitbox_player(jogo["player_x"], jogo["player_y"])
            continue

        # Impede entrar pela lateral no corpo do prédio quando está abaixo do telhado.
        # Se os pés ainda estão acima do telhado, o personagem pode passar por cima.
        sobrepoe_vertical = (
            player_rect.bottom > topo + 3
            and player_rect.top < 410
        )
        if not sobrepoe_vertical:
            continue

        corpo = pygame.Rect(esquerda, topo + 2, max(1, direita - esquerda), 410 - topo)
        if player_rect.colliderect(corpo):
            if anterior.right <= esquerda:
                jogo["player_x"] = esquerda - (TAMANHO_PLAYER - MARGEM_X)
            elif anterior.left >= direita:
                jogo["player_x"] = direita - MARGEM_X
            elif player_rect.centerx < corpo.centerx:
                jogo["player_x"] = esquerda - (TAMANHO_PLAYER - MARGEM_X)
            else:
                jogo["player_x"] = direita - MARGEM_X
            player_rect = hitbox_player(jogo["player_x"], jogo["player_y"])


def desenhar_debug(tela, jogo):
    pygame.draw.rect(
        tela, (0, 255, 0),
        hitbox_player(jogo["player_x"], jogo["player_y"]), 2
    )
    for predio in jogo["predios"]:
        x = int(predio["x"])
        topo = int(predio["telhado_y"])
        pygame.draw.line(
            tela, (0, 120, 255), (x, topo),
            (x + largura_predio(predio), topo), 2
        )
        for obstaculo in predio.get("obstaculos", []):
            pygame.draw.rect(tela, (255, 0, 0), rect_obstaculo(obstaculo), 2)
    for caixa in jogo.get("caixas", []):
        pygame.draw.rect(tela, (255, 255, 0), caixa.rect(), 2)
