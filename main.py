import pygame
import random

pygame.init()

LARGURA = 800
ALTURA = 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Homem-Aranha: Salto Radical")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

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
    player_img = pygame.Surface((60, 60))
    player_img.fill((255, 0, 0))

    obstaculo_img = pygame.Surface((50, 50))
    obstaculo_img.fill((0, 0, 0))

    fundo_img = pygame.Surface((800, 400))
    fundo_img.fill((200, 200, 200))

    bloco_img = pygame.Surface((60, 20))
    bloco_img.fill((255, 255, 255))

player_x = 100
player_y = 300
vel_y = 0
gravidade = 0.7
no_chao = True

obstaculos = []
blocos = []

clock = pygame.time.Clock()
rodando = True
velocidade = 6

pontos = 0
fonte = pygame.font.SysFont(None, 36)

fundo_x = 0

while rodando:
    clock.tick(60)

    player_y_anterior = player_y

    fundo_x -= 2
    if fundo_x <= -800:
        fundo_x = 0

    tela.blit(fundo_img, (fundo_x, 0))
    tela.blit(fundo_img, (fundo_x + 800, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and no_chao:
                vel_y = -15
                no_chao = False

    vel_y += gravidade
    player_y += vel_y

    no_chao = False

    if player_y >= 300:
        player_y = 300
        vel_y = 0
        no_chao = True

    if len(obstaculos) == 0 or obstaculos[-1][0] < 450:
        obstaculos.append([800, 310])

    if len(blocos) == 0:
        if len(obstaculos) > 0 and obstaculos[-1][0] < 500:
            if random.randint(0, 100) < 25:  # 🔥 MAIS CHANCE

                quantidade = random.randint(3, 5)

                for i in range(quantidade):
                    x = 800 + (i * 65)
                    y = 300 - (i * 30)

                    blocos.append([x, y])

    for obs in obstaculos:
        obs[0] -= velocidade

    for bloco in blocos:
        bloco[0] -= velocidade

    obstaculos = [o for o in obstaculos if o[0] > -50]
    blocos = [b for b in blocos if b[0] > -60]

    player_rect = pygame.Rect(player_x, player_y, 60, 60)

    for obs in obstaculos:
        if player_rect.colliderect(pygame.Rect(obs[0], obs[1], 50, 50)):
            print("GAME OVER")
            pygame.time.delay(1000)
            rodando = False

    for bloco in blocos:
        bloco_rect = pygame.Rect(bloco[0], bloco[1], 60, 20)

        if player_rect.colliderect(bloco_rect):
            if vel_y > 0 and player_y_anterior + 60 <= bloco_rect.top + 15:
                player_y = bloco_rect.top - 60
                vel_y = 0
                no_chao = True

    pontos += 1

    texto = fonte.render(f"Pontos: {pontos}", True, PRETO)

    tela.blit(player_img, (player_x, player_y))

    for obs in obstaculos:
        tela.blit(obstaculo_img, (obs[0], obs[1]))

    for bloco in blocos:
        tela.blit(bloco_img, (bloco[0], bloco[1]))

    pygame.draw.rect(tela, PRETO, (0, 360, 800, 40))
    tela.blit(texto, (10, 10))

    pygame.display.update()

pygame.quit()