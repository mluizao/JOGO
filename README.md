🕷️ Jump Spider Man

1. Descrição Geral
Este é um jogo do tipo **arcade/plataforma**, desenvolvido em Python.

O jogo se passa em um cenário 2D com movimento automático, onde o personagem corre sem parar enquanto o jogador precisa reagir rapidamente.

A ideia principal é desviar dos obstáculos no tempo certo, sobreviver o máximo possível e acumular pontos.

---

2. Objetivo do Jogo
O objetivo do jogador é:
- Desviar de todos os obstáculos
- Sobreviver o maior tempo possível
- Alcançar a maior pontuação

Futuramente:
- Completar fases
- Salvar a Barbie e levá-la até o castelo

O jogador perde ao colidir com obstáculos.

---

3. Personagem Principal
O personagem principal é inspirado no **Homem-Aranha**.

Características:
- Movimento automático para frente
- Pode pular para desviar dos obstáculos
- Possui:
  - Pontuação
  - Velocidade progressiva
  - (Futuramente) sistema de vidas

---

4. Inimigos e Obstáculos
Tipos de obstáculos:

Atual:
- Obstáculos simples

Futuros:
- Cidade: prédios
- Esgoto: canos e substâncias verdes
- Mundo da Barbie: laços

Comportamento:
- Movimento automático em direção ao jogador

Colisão:
- Game Over (por enquanto)

---

5. Cenário (Mapa)
O jogo possui um mapa contínuo (infinito).

Cenários planejados:
- 🌃 Cidade (tema Homem-Aranha, à noite)
- 🧪 Esgoto (tema Hulk)
- 🎀 Mundo da Barbie

Elementos:
- Obstáculos no caminho
- Progressão contínua

---

6. Sistema de Pontuação
O jogador ganha pontos:
- Pelo tempo de sobrevivência

Futuramente:
- Desviar de obstáculos
- Coletar itens especiais

---

7. Sistema de Vida
Atual:
- Sem vidas (morre ao colidir)

Futuro:
- Sistema de vidas
- Perda de vida ao colidir
- Game Over ao zerar

---

8. Controles
Controles atuais:
- **Barra de espaço** → Pular

Controles futuros:
- **Setas direcionais** → Movimentação
- **Espaço** → Pulo

---

9. Fluxo do Jogo
- O jogo inicia (com ou sem menu)
- O personagem começa correndo automaticamente
- Obstáculos aparecem progressivamente
- O jogador deve desviar pulando

Condições:
- Derrota: colidir com obstáculos
- Vitória (futura): completar fases e salvar a Barbie

---

## 10. Regras do Jogo
- Não pode atravessar obstáculos
- Deve desviar no tempo correto
- O personagem nunca para
- O jogador deve reagir rapidamente

---

## 11. Estrutura do Projeto
JOGO/
│── main.py
│── ranking.txt
│── README.md
│
└── assets/
└── imagens/
├── bloco.png
├── fundo.png
├── obstaculo.png
└── player.png
---

12. Funcionalidades Mínimas
Para a primeira versão:
- Personagem pulando
- Obstáculos funcionando
- Colisão detectando
- Sistema de pontuação
- Game Over

---

13. Melhorias Futuras
- Novos cenários:
  - Cidade à noite (Homem-Aranha)
  - Esgoto (Hulk)
  - Mundo da Barbie
- Sistema de fases
- História no início do jogo
- Resgate da Barbie
- Novos controles (setas)
- Sistema de vidas
- Interface mais bonita

---

14. Storyboard do Jogo
1. Introdução com uma pequena história  
2. 🌃 Fase 1: Cidade (Homem-Aranha)  
3. O personagem cai no esgoto durante a fuga  
4. 🧪 Transformação: ele se transforma no Hulk  
5. 🧪 Fase 2: Esgoto (Hulk)  
6. O personagem é capturado/abduzido por uma nave 👽  
7. 🎀 Fase 3: Mundo da Barbie  
8. Objetivo: salvar a Barbie  
9. Levar a Barbie até o castelo 🏰  
10. Final do jogo  
