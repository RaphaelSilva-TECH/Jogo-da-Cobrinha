import pygame
import random

# Inicialização do Pygame
pygame.init()

# Músicas do jogo
pygame.mixer.music.load("cruising-down-8bit-lane-159615.mp3")
pygame.mixer.music.set_volume(0.3)  # Volume da música de fundo (30%)
pygame.mixer.music.play(-1, 0.0)
som_comer = pygame.mixer.Sound("Apple_Bite-Simon_Craggs-1683647397.wav")
som_comer.set_volume(0.3)
som_perder = pygame.mixer.Sound("GameOver.wav")
som_perder.set_volume(0.3)

# Janela
LARGURA, ALTURA = 760, 520
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cobrinha - By Rapha")

# Cores
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)

# Tamanho do bloco e velocidade inicial
TAMANHO_BLOCO = 20
velocidade = 10

# Clock
relogio = pygame.time.Clock()

# Fonte do placar
fonte = pygame.font.SysFont(None, 35)

def exibir_texto(msg, cor, y):
    """Desenha o texto centralizado na horizontal na posição y."""
    texto = fonte.render(msg, True, cor)
    largura_texto = texto.get_width()
    x_central = (LARGURA - largura_texto) // 2
    tela.blit(texto, (x_central, y))

# Alternar cores da cobra
def cor_cobra_personalizada(tamanho):
    if tamanho < 10:
        return (0, min(255, tamanho * 10), 0)  # Verde
    elif tamanho < 30:
        return (255, 255, 0)  # Amarelo
    else:
        return (255, 0, 255)  # Roxo

# Brilho na cobra
def efeito_brilho(x, y):
    for i in range(5):
        pygame.draw.circle(tela, (255, 255, 0), (x + random.randint(-5, 5), y + random.randint(-5, 5)), random.randint(5, 10))

# Piscar quando perde
def piscar_cobra(segmentos, cor_cobra, relogio, tela, TAMANHO_BLOCO):
    piscar_visivel = True
    contador_piscar = 0
    total_piscadas = 5  # número total de alternâncias
    piscar_intervalo = 200  # tempo em ms entre piscar

    tempo_ultima_alteracao = pygame.time.get_ticks()

    while contador_piscar < total_piscadas:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_ultima_alteracao > piscar_intervalo:
            piscar_visivel = not piscar_visivel
            tempo_ultima_alteracao = tempo_atual
            contador_piscar += 1

        tela.fill((0,0,0))  # limpa tela

        if piscar_visivel:
            for parte in segmentos:
                pygame.draw.rect(tela, cor_cobra, [parte[0], parte[1], TAMANHO_BLOCO, TAMANHO_BLOCO])

        pygame.display.update()
        relogio.tick(60)  # manter 60 FPS

def jogo():
    global velocidade
    velocidade = 10 # Reinicia a velocidade ao iniciar o jogo
    """Loop principal do jogo."""
    jogando = True
    perdeu = False

    # Mostra mensagem inicial
    tela.fill(PRETO)
    exibir_texto("Bem-vindo ao jogo da Cobrinha!", BRANCO, ALTURA // 3)
    exibir_texto("Dica: Alcançando 50 pontos, você atravessa as paredes!", AMARELO, ALTURA // 2)
    pygame.display.update()
    pygame.time.delay(3000)  # exibe por 3 segundos

    # Posição inicial
    x = LARGURA // 2
    y = ALTURA // 2

    mov_x = 0
    mov_y = 0

    segmentos = []
    tamanho = 1

    # Posição inicial da maçã
    maca_x = random.randrange(0, LARGURA - TAMANHO_BLOCO, TAMANHO_BLOCO)
    maca_y = random.randrange(0, ALTURA - TAMANHO_BLOCO, TAMANHO_BLOCO)

    modo_infinito = False
    mostrou_mensagem_50 = False

    while jogando:

        # Tela de "game over"
        while perdeu:

            tela.fill(PRETO)
            exibir_texto("Oops! Você perdeu... Tente de novo!", VERMELHO, ALTURA // 3)
            exibir_texto("Pressione R para reinicar ou Q para sair", VERMELHO, ALTURA // 3 + 40)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        jogando = False
                        perdeu = False
                    if evento.key == pygame.K_r:
                        pygame.mixer.music.play(-1, 0.0)  # reinicia música de fundo
                        jogo()

        # Eventos principais
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and mov_x == 0:
                    mov_x = -TAMANHO_BLOCO
                    mov_y = 0
                elif evento.key == pygame.K_RIGHT and mov_x == 0:
                    mov_x = TAMANHO_BLOCO
                    mov_y = 0
                elif evento.key == pygame.K_UP and mov_y == 0:
                    mov_y = -TAMANHO_BLOCO
                    mov_x = 0
                elif evento.key == pygame.K_DOWN and mov_y == 0:
                    mov_y = TAMANHO_BLOCO
                    mov_x = 0

        # Modo infinito a partir de 50 pontos
        if (tamanho - 1) >= 50:
            modo_infinito = True

        # Colisão com as bordas (ou atravessar se modo infinito)
        if modo_infinito:
            if x >= LARGURA:
                x = 0
            elif x < 0:
                x = LARGURA - TAMANHO_BLOCO
            if y >= ALTURA:
                y = 0
            elif y < 0:
                y = ALTURA - TAMANHO_BLOCO
        else:
            if x >= LARGURA or x < 0 or y >= ALTURA or y < 0:
                perdeu = True
                pygame.mixer.music.stop()
                som_perder.play()
                piscar_cobra(segmentos, cor_cobra_personalizada(tamanho), relogio, tela, TAMANHO_BLOCO)

        x += mov_x
        y += mov_y
        x = int(x)
        y = int(y)

        # Fundo dinâmico
        nivel = (tamanho - 1) // 5
        cores = [(0,0,0), (20,20,60), (60,0,60), (100,0,0)]
        cor_fundo = cores[nivel % len(cores)]
        tela.fill(cor_fundo)

        # Desenha maçã
        pygame.draw.rect(tela, VERMELHO, [maca_x, maca_y, TAMANHO_BLOCO, TAMANHO_BLOCO])

        # Corpo da cobra
        cabeca = [x, y]
        segmentos.append(cabeca)
        if len(segmentos) > tamanho:
            del segmentos[0]

        # Colisão com o próprio corpo
        for parte in segmentos[:-1]:
            if parte == cabeca:
                perdeu = True
                pygame.mixer.music.stop()
                som_perder.play()
                piscar_cobra(segmentos, cor_cobra_personalizada(tamanho), relogio, tela, TAMANHO_BLOCO)

        # Desenha a cobra
        for parte in segmentos:
            for parte in segmentos:
                cor_cobra = cor_cobra_personalizada(tamanho)
                pygame.draw.rect(tela, cor_cobra, [parte[0], parte[1], TAMANHO_BLOCO, TAMANHO_BLOCO])

        # Placar
        exibir_texto(f"Pontos: {tamanho - 1}", BRANCO, 5)
        pygame.display.update()

        # Comer a maçã
        if abs(x - maca_x) < TAMANHO_BLOCO and abs(y - maca_y) < TAMANHO_BLOCO:
            som_comer.play()
            maca_x = random.randrange(0, LARGURA - TAMANHO_BLOCO, TAMANHO_BLOCO)
            maca_y = random.randrange(0, ALTURA - TAMANHO_BLOCO, TAMANHO_BLOCO)
            efeito_brilho(maca_x, maca_y)
            maca_x = int(maca_x)
            maca_y = int(maca_y)
            crescimento = random.randint(1, 3)
            tamanho += crescimento

            # Aumenta velocidade a cada 5 pontos
            if (tamanho - 1) % 5 == 0:
                velocidade += 2

            # Mensagem ao atingir 50 pontos
            pontos_atuais = tamanho - 1
            if pontos_atuais >= 50 and not mostrou_mensagem_50:
                tela.fill(PRETO)
                exibir_texto("🎉 Parabéns! Você atingiu 50 pontos! 🎉", AMARELO, ALTURA // 2 - 20)
                pygame.display.update()
                pygame.time.delay(2500)
                mostrou_mensagem_50 = True

        relogio.tick(velocidade)

    pygame.quit()
    quit()

if __name__ == "__main__":
    jogo()
