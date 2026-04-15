import pygame
import random
import os

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
except:
    print("Erro: Imagens não encontradas.")
    player_img = pygame.Surface((60, 60))
    player_img.fill((255, 0, 0))

    obstaculo_img = pygame.Surface((50, 50))
    obstaculo_img.fill((0, 0, 0))

    fundo_img = pygame.Surface((800, 400))
    fundo_img.fill((200, 200, 200))

player_x = 100
player_y = 300
vel_y = 0
gravidade = 0.7
pulando = False

obstaculos = []

pontos = 0
fonte = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()
rodando = True
velocidade = 7

fundo_x = 0

while rodando:
    clock.tick(60)

    fundo_x -= 2
    if fundo_x <= -800:
        fundo_x = 0

    tela.blit(fundo_img, (fundo_x, 0))
    tela.blit(fundo_img, (fundo_x + 800, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not pulando:
                vel_y = -15
                pulando = True

    vel_y += gravidade
    player_y += vel_y

    if player_y >= 300:
        player_y = 300
        vel_y = 0
        pulando = False

    if len(obstaculos) == 0 or obstaculos[-1][0] < 600:
        quantidade = random.randint(1, 2)

        for i in range(quantidade):
            posicao_x = 800 + (i * 70)
            obstaculos.append([posicao_x, 310])

    for obs in obstaculos:
        obs[0] -= velocidade

    obstaculos = [obs for obs in obstaculos if obs[0] > -50]

    player_rect = pygame.Rect(player_x, player_y, 60, 60)

    for obs in obstaculos:
        obs_rect = pygame.Rect(obs[0], obs[1], 50, 50)
        if player_rect.colliderect(obs_rect):
            print(f"GAME OVER! Pontuação: {pontos}")
            pygame.time.delay(1000)
            rodando = False

    pontos += 1
    velocidade += 0.002

    texto = fonte.render(f"Pontos: {pontos}", True, PRETO)

    tela.blit(player_img, (player_x, player_y))

    for obs in obstaculos:
        tela.blit(obstaculo_img, (obs[0], obs[1]))

    pygame.draw.rect(tela, PRETO, (0, 360, 800, 40))

    tela.blit(texto, (10, 10))

    pygame.display.update()
pygame.quit()