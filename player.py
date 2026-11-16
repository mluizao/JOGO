import math
import pygame


class Player:

    def __init__(self, imagem):
        self.imagem = imagem

        self.x = 100
        self.y = 370
        self.chao_y = 370  # posição y do player quando está na rua

        self.largura = 60
        self.altura = 60

        # hitbox menor que a imagem (tira as bordas transparentes)
        self.margem_x = 10
        self.margem_topo = 5

        self.velocidade = 5
        self.vel_y = 0
        self.gravidade = 0.7
        self.forca_pulo = -15

        self.no_chao = True
        self.estava_no_chao = True
        self.tempo_pulo = 0
        self.y_anterior = self.y

        # animação
        self.virado_esquerda = False
        self.andando = False
        self.tempo_anim = 0
        self.escala_x = 1.0
        self.escala_y = 1.0

    # ------------------------------------------------------------------
    # MOVIMENTO
    # ------------------------------------------------------------------
    def pular(self, teclas):

        if teclas[pygame.K_SPACE] and self.no_chao:
            self.vel_y = self.forca_pulo
            self.no_chao = False
            self.tempo_pulo = 0

        if teclas[pygame.K_SPACE] and not self.no_chao:
            if self.tempo_pulo < 10:
                self.vel_y -= 0.5
                self.tempo_pulo += 1

    def atualizar(self, teclas):

        self.y_anterior = self.y
        self.estava_no_chao = self.no_chao
        self.andando = False

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.velocidade
            self.andando = True
            self.virado_esquerda = True

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.velocidade
            self.andando = True
            self.virado_esquerda = False

        if self.x < 0:
            self.x = 0

        self.pular(teclas)

        self.vel_y += self.gravidade
        self.y += self.vel_y

        # A cada frame assumimos que está no ar.
        # Quem encontrar chão (rua ou prédio) marca como True.
        self.no_chao = False

        if self.y >= self.chao_y:
            self.y = self.chao_y
            self.vel_y = 0
            self.no_chao = True
            if not self.estava_no_chao:
                self._efeito_pouso()

    def pousar_em(self, rect_predio):
        """
        Chame para cada prédio, DEPOIS de player.atualizar().
        Só pousa se estiver caindo e se os pés estavam acima do topo
        no frame anterior (evita "grudar" ao bater de lado).
        """
        hitbox = self.rect()

        if self.vel_y < 0 or not hitbox.colliderect(rect_predio):
            return False

        pes_anterior = self.y_anterior + self.altura

        if pes_anterior <= rect_predio.top + 4:
            self.y = rect_predio.top - self.altura
            if not self.estava_no_chao and self.vel_y > 3:
                self._efeito_pouso()
            self.vel_y = 0
            self.no_chao = True
            return True

        return False

    # ------------------------------------------------------------------
    # ANIMAÇÃO (só com código, usando a imagem única)
    # ------------------------------------------------------------------
    def _efeito_pouso(self):
        self.escala_x = 1.3
        self.escala_y = 0.7

    def _animar(self):
        self.tempo_anim += 1

        if self.no_chao:
            alvo_x, alvo_y = 1.0, 1.0
        else:
            # estica na vertical conforme a velocidade
            esticar = min(abs(self.vel_y) / 25, 0.25)
            alvo_x = 1.0 - esticar * 0.6
            alvo_y = 1.0 + esticar

        # aproxima suavemente da escala alvo
        self.escala_x += (alvo_x - self.escala_x) * 0.25
        self.escala_y += (alvo_y - self.escala_y) * 0.25

    # ------------------------------------------------------------------
    # DESENHO E HITBOX
    # ------------------------------------------------------------------
    def desenhar(self, tela):
        self._animar()

        largura = max(1, int(self.largura * self.escala_x))
        altura = max(1, int(self.altura * self.escala_y))
        img = pygame.transform.scale(self.imagem, (largura, altura))

        if self.virado_esquerda:
            img = pygame.transform.flip(img, True, False)

        pulo_corrida = 0
        inclinacao = 0

        if self.andando and self.no_chao:
            onda = math.sin(self.tempo_anim * 0.35)
            pulo_corrida = -abs(onda) * 4   # sobe e desce ao correr
            inclinacao = onda * 6           # balança de um lado pro outro
        elif not self.no_chao:
            # inclina um pouco na direção do movimento no ar
            inclinacao = max(-12, min(12, -self.vel_y * 0.5))
            if self.virado_esquerda:
                inclinacao = -inclinacao

        if inclinacao:
            img = pygame.transform.rotate(img, inclinacao)

        pos = img.get_rect(
            midbottom=(
                self.x + self.largura / 2,
                self.y + self.altura + pulo_corrida
            )
        )
        tela.blit(img, pos)

    def rect(self):
        return pygame.Rect(
            self.x + self.margem_x,
            self.y + self.margem_topo,
            self.largura - self.margem_x * 2,
            self.altura - self.margem_topo
        )