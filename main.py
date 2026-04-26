import pygame
import random

pygame.init()

# ===== CONFIG =====
LARGURA = 800
ALTURA = 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Homem-Aranha: Salto Radical")

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

fonte = pygame.font.SysFont(None, 36)
fonte_grande = pygame.font.SysFont(None, 60)

clock = pygame.time.Clock()

# ===== RANKING =====
def salvar_ranking(nome, pontos):
    with open("ranking.txt", "a") as f:
        f.write(f"{nome},{pontos}\n")

def carregar_ranking():
    ranking = []
    try:
        with open("ranking.txt", "r") as f:
            for linha in f:
                if "," in linha:
                    nome, pontos = linha.strip().split(",")
                    ranking.append((nome, int(pontos)))
    except:
        pass
    return ranking

ranking = carregar_ranking()

# ===== IMAGENS =====
try:
    player_img = pygame.image.load("assets/imagens/player.png")
    player_img = pygame.transform.scale(player_img, (60, 60))

    obstaculo_img = pygame.image.load("assets/imagens/obstaculo.png")
    obstaculo_img = pygame.transform.scale(obstaculo_img, (50, 50))

    fundo_img = pygame.image.load("assets/imagens/fundo.png")
    fundo_img = pygame.transform.scale(fundo_img, (800, 400))

    bloco_img = pygame.image.load("assets/imagens/bloco.png")
    bloco_img = pygame.transform.scale(bloco_img, (60, 20))

except:
    fundo_img = pygame.Surface((800, 400))
    fundo_img.fill((150, 200, 255))

    player_img = pygame.Surface((60, 60))
    player_img.fill((255, 0, 0))

    obstaculo_img = pygame.Surface((50, 50))
    obstaculo_img.fill((0, 0, 0))

    bloco_img = pygame.Surface((60, 20))
    bloco_img.fill((255, 255, 255))

# ===== ESTADOS =====
estado = "menu"
nome_jogador = ""

# ===== RESET =====
def resetar_jogo():
    return {
        "player_x": 100,
        "player_y": 300,
        "vel_y": 0,
        "gravidade": 0.7,
        "no_chao": True,
        "tempo_pulo": 0,
        "obstaculos": [],
        "blocos": [],
        "pontos": 0,
        "fundo_x": 0,
        "velocidade_base": 6
    }

jogo = resetar_jogo()

# ===== LOOP =====
rodando = True
while rodando:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # MENU
        if estado == "menu":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome_jogador.strip() != "":
                    jogo = resetar_jogo()
                    estado = "jogo"
                elif evento.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1]
                else:
                    if evento.unicode.isprintable():
                        nome_jogador += evento.unicode

        # GAME OVER
        elif estado == "game_over":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    estado = "menu"
                    nome_jogador = ""

    tela.fill(BRANCO)

    # ===== MENU =====
    if estado == "menu":
        titulo = fonte_grande.render("SALTO RADICAL", True, PRETO)
        tela.blit(titulo, (200, 50))

        texto_nome = fonte.render(f"Nome: {nome_jogador}", True, PRETO)
        tela.blit(texto_nome, (250, 150))

        instrucao = fonte.render("Pressione ENTER para jogar", True, PRETO)
        tela.blit(instrucao, (200, 200))

        tela.blit(fonte.render("RANKING:", True, PRETO), (250, 250))

        ranking_ordenado = sorted(ranking, key=lambda x: x[1], reverse=True)

        y = 280
        for i, (nome, pontos) in enumerate(ranking_ordenado[:5]):
            texto = fonte.render(f"{i+1}. {nome} - {pontos}", True, PRETO)
            tela.blit(texto, (250, y))
            y += 30

    # ===== JOGO =====
    elif estado == "jogo":

        player_y_anterior = jogo["player_y"]

        # FUNDO
        jogo["fundo_x"] -= 2
        if jogo["fundo_x"] <= -800:
            jogo["fundo_x"] = 0

        tela.blit(fundo_img, (jogo["fundo_x"], 0))
        tela.blit(fundo_img, (jogo["fundo_x"] + 800, 0))

        teclas = pygame.key.get_pressed()

        # PULO
        if teclas[pygame.K_SPACE] and jogo["no_chao"]:
            jogo["vel_y"] = -15
            jogo["no_chao"] = False
            jogo["tempo_pulo"] = 0

        if teclas[pygame.K_SPACE] and not jogo["no_chao"]:
            if jogo["tempo_pulo"] < 10:
                jogo["vel_y"] -= 0.5
                jogo["tempo_pulo"] += 1

        # GRAVIDADE
        jogo["vel_y"] += jogo["gravidade"]
        jogo["player_y"] += jogo["vel_y"]
        jogo["no_chao"] = False

        if jogo["player_y"] >= 300:
            jogo["player_y"] = 300
            jogo["vel_y"] = 0
            jogo["no_chao"] = True

        # OBSTÁCULOS
        if len(jogo["obstaculos"]) == 0 or jogo["obstaculos"][-1][0] < 450:
            jogo["obstaculos"].append([800, 310])

        # BLOCOS
        if len(jogo["blocos"]) == 0:
            if len(jogo["obstaculos"]) > 0 and jogo["obstaculos"][-1][0] < 500:
                if random.randint(0, 100) < 25:
                    quantidade = random.randint(3, 5)
                    for i in range(quantidade):
                        x = 800 + (i * 65)
                        y = 300 - (i * 30)
                        jogo["blocos"].append([x, y])

        velocidade = jogo["velocidade_base"] + (jogo["pontos"] / 1000) * 0.5

        for obs in jogo["obstaculos"]:
            obs[0] -= velocidade

        for bloco in jogo["blocos"]:
            bloco[0] -= velocidade

        jogo["obstaculos"] = [o for o in jogo["obstaculos"] if o[0] > -50]
        jogo["blocos"] = [b for b in jogo["blocos"] if b[0] > -60]

        player_rect = pygame.Rect(jogo["player_x"], jogo["player_y"], 60, 60)

        # COLISÃO
        for obs in jogo["obstaculos"]:
            if player_rect.colliderect(pygame.Rect(obs[0], obs[1], 50, 50)):
                salvar_ranking(nome_jogador, jogo["pontos"])
                ranking = carregar_ranking()
                estado = "game_over"
                break

        if estado == "game_over":
            continue

        # COLISÃO BLOCO
        for bloco in jogo["blocos"]:
            bloco_rect = pygame.Rect(bloco[0], bloco[1], 60, 20)

            if player_rect.colliderect(bloco_rect):
                if jogo["vel_y"] > 0 and player_y_anterior + 60 <= bloco_rect.top + 15:
                    jogo["player_y"] = bloco_rect.top - 60
                    jogo["vel_y"] = 0
                    jogo["no_chao"] = True

        jogo["pontos"] += 1

        tela.blit(player_img, (jogo["player_x"], jogo["player_y"]))

        for obs in jogo["obstaculos"]:
            tela.blit(obstaculo_img, (obs[0], obs[1]))

        for bloco in jogo["blocos"]:
            tela.blit(bloco_img, (bloco[0], bloco[1]))

        pygame.draw.rect(tela, PRETO, (0, 360, 800, 40))

        texto = fonte.render(f"Pontos: {jogo['pontos']}", True, PRETO)
        tela.blit(texto, (10, 10))

    # ===== GAME OVER =====
    elif estado == "game_over":
        tela.fill(BRANCO)

        msg = fonte_grande.render("GAME OVER", True, PRETO)
        tela.blit(msg, (250, 120))

        pontos = fonte.render(f"Pontos: {jogo['pontos']}", True, PRETO)
        tela.blit(pontos, (300, 200))

        voltar = fonte.render("Pressione ENTER", True, PRETO)
        tela.blit(voltar, (270, 250))

    pygame.display.flip()

pygame.quit()