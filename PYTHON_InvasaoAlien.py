import pygame
import random
import sys

pygame.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Invasão Alien")

verde = (0,255,0)
vermelho = (255, 0, 0)
amarelo = (255, 255, 0)
preto = (0,0,0)
branco = (255,255,255)

class Jogo:
    def __init__(self):
        self.nave = pygame.Rect(largura // 2 - 25, altura - 60, 50, 30)
        self.balas = []
        self.inimigos = []
        self.placar = 0

        self.velocidade_bala = 10
        self.velocidade_inimigos = 2
        self.direcao_inimigos = 1
        self.inimigos_descendo = False
        self.contador_descida = 0

        self.fonte = pygame.font.SysFont("Arial", 20)

        self.criar_inimigos()

        self.jogo_iniciado = False
        self.botao_iniciar = pygame.Rect(largura // 2 - 100, altura // 2 -25, 200, 50)

        self.velocidade_nave = 5
        self.movendo_esquerda = False
        self.movendo_direita = False
        self.fim_jogo = False

        self.ondas = 0

    def criar_inimigos(self):
        self.inimigos = []
        for i in range(5):
            for j in range(3):
                pos_x = 100 + (i * 100)
                pos_y = 50 + (j * 60)
                inimigo = pygame.Rect(pos_x, pos_y, 50, 30)
                self.inimigos.append(inimigo)

    def desenhar_placar(self):
        placar_texto = self.fonte.render(f'Placar: {self.placar}', True, branco)
        tela.blit(placar_texto, (10,10))

    def desenhar_botao_iniciar(self):
        pygame.draw.rect(tela, branco, self.botao_iniciar)
        texto_iniciar = self.fonte.render("Iniciar", True, preto)
        tela.blit(texto_iniciar, (largura // 2 - 25, altura // 2 - 14))

    def desenhar(self):
        tela.fill(preto)
        pygame.draw.rect(tela, verde, self.nave)

        for bala in self.balas:
            pygame.draw.rect(tela, vermelho, bala)

        for inimigos in self.inimigos:
            pygame.draw.rect(tela, amarelo, inimigos)

        self.desenhar_placar()

    def mover_nave(self):
        if self.movendo_esquerda:
            self.nave.x -= self.velocidade_nave
        if self.movendo_direita:
            self.nave.x += self.velocidade_nave

        if self.nave.x < 0:
            self.nave = 0
        elif self.nave.x > largura - self.nave.width:
            self.nave.x = largura - self.nave.width

    def atirar_bala(self):
        if len(self.balas) < 5:
            nova_bala = pygame.Rect(self.nave.x + self.nave.width // 2 - 2, self.nave.y, 5, 20)
            self.balas.append(nova_bala)

    def atualizar_balas(self):
        for bala in self.balas[:]:
            bala.y -= self.velocidade_bala
            if bala.y < 0:
                self.balas.remove(bala)

    def atualizar_inimigos(self):
        if self.fim_jogo:
            return
        for inimigo in self.inimigos[:]:
            inimigo.x += self.direcao_inimigos * self.velocidade_inimigos

            if inimigo.x <= 0 or inimigo.x >= largura - inimigo.width:
                self.direcao_inimigos *= -1
                self.descer_inimigos()

            if inimigo.y >= altura - 60 or inimigo.colliderect(self.nave):
                self.game_over = True

    def descer_inimigos(self):
        for inimigo in self.inimigos:
            inimigo.y += 2

    def checar_colisoes(self):
        for bala in self.balas[:]:
            for inimigo in self.inimigos[:]:
                if bala.colliderect(inimigo):
                    self.balas.remove(bala)
                    self.inimigos.remove(inimigo)
                    self.placar += 1
                    break

    def iniciar_jogo(self):
        self.jogo_iniciado = True
        self.placar = 0
        self.criar_inimigos()
        self.fim_jogo = False
        self.ondas += 1

        self.velocidade_inimigos *= 1.05

    def reiniciar_onda(self):
        self.criar_inimigos()
        self.ondas += 1
        self.velocidade_inimigos *= 1.05

def main():
    clock = pygame.time.Clock()
    jogo = Jogo()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if jogo.botao_iniciar.collidepoint(evento.pos) and not jogo.jogo_iniciado:
                    jogo.iniciar_jogo()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jogo.movendo_esquerda = True
                if evento.key == pygame.K_RIGHT:
                    jogo.movendo_direita = True
                if evento.key == pygame.K_SPACE:
                    jogo.atirar_bala()

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    jogo.movendo_esquerda = False
                if evento.key == pygame.K_RIGHT:
                    jogo.movendo_direita = False

        if jogo.jogo_iniciado and not jogo.fim_jogo:
            jogo.mover_nave()
            jogo.atualizar_balas()
            jogo.atualizar_inimigos()
            jogo.checar_colisoes()

            if not jogo.inimigos:
                jogo.reiniciar_onda()

            jogo.desenhar()
        else:
            if jogo.fim_jogo:
                font = pygame.font.SysFont("Arial", 50)
                texto_fim_jogo = font.render("FIM DE JOGO", True, vermelho)
                tela.blit(texto_fim_jogo, (largura // 2 - 150, altura // 2 - 25))
            else:
                jogo.desenhar_botao_iniciar()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
