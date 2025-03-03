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
        self.nave = pygame.rect(largura // 2 - 25, altura - 60, 50, 30)
        self.balas = []
        self.inimigos = []
        self.placar = 0

        self.velocidade_bala = 10
        self.velocidade_inimigos = 2

        self.fonte = pygame.font.SysFont(("Arial", 12))

        self.criar_inimigos()

        self.jogo_iniciado = False
        self.botao_iniciar = pygame.rect(largura // 2 - 100, altura // 2 -25, 200, 50)

    def criar_inimigos(self):
        for i in range(5):
            for j in range(5):
                pos_x = 100 + (i * 60)
                pos_y = 100 + (j * 50)
                inimigo = pygame.rect(pos_x, pos_y, 50, 30)
                self.inimigos.append(inimigo)

    def desenhar_placar(self):
        placar_texto = self.fonte.render(f'Placar: {self.placar}', True, branco)
        tela.blit(placar_texto, (10,10))

    def desenhar_botao_iniciar(self):
        pygame.draw.rect(tela, branco, self.botao_iniciar)
        texto_iniciar = self.font.render("Iniciar", True, preto)
        tela.blit(texto_iniciar, (largura // 2 - 50, altura // 2 -20))

    def desenhar(self):
        tela.fill(preto)
        pygame.draw.rect(tela, verde, self.nave)

        for bala in self.balas:
            pygame.draw.rect(tela, vermelho, bala)

        for inimigos in self.inimigos:
            pygame.draw.rect(tela, amarelo, inimigos)

        self.desenhar_placar()

    def mover_nave(self, mov_x):
        if self.nave.x + mov_x >= 0 and self.nave.x + mov_x <= largura - self.nave.width:
            self.nave.x += mov_x

    def atirar_bala(self):
        if len(self.balas) < 5:
            nova_bala = pygame.rect(self.nave.x + self.nave.width // 2 - 2, self.nave.y, 5, 20)
            self.balas.append(nova_bala)

    def atualizar_balas(self):
        for bala in self.balas[:]:
            bala.y -= self.velocidade_bala
            if bala.y < 0:
                self.balas.remove(bala)

    def atualizar_inimigos(self):
        for inimigo in self.inimigos[:]:
            inimigo.y += self.velocidade_inimigos
            if inimigo.y > altura:
                self.inimigos.remove(inimigo)

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
        self.criar_inimigos()

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
                    jogo.mover_nave(-10)
                if evento.key == pygame.K_RIGHT:
                    jogo.mover_nave(10)
                if evento.key == pygame.K_SPACE:
                    jogo.atirar_bala()

        if jogo.jogo_iniciado:
            jogo.atualizar_balas()
            jogo.atualizar_inimigos()
            jogo.checar_colisoes()
            jogo.desenhar()
        else:
            jogo.desenhar_botao_iniciar()

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()


""" from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock

class Jogo(Widget):
        super().__init__(**kwargs)

        self.botao_iniciar = Button(text="Iniciar", size_hint=(None, None), size=(200, 50), pos=(Window.width // 2 - 100, Window.height // 2))
        self.botao_iniciar.bind(on_press=self.iniciar_jogo)
        self.add_widget(self.botao_start)

        self.nave = None
        self.balas = []
        self.inimigos = []
        self.placar = 0

        self.velocidade_bala = 10
        self.velocidade_inimigos = 2

        self.placar_label = Label(text=f'Placar: {self.placar}', font_size=20, color=(1, 1, 1, 1))
        self.placar_label.pos = (10, Window.height - 30)

    def iniciar_jogo(self, instance):

        self.remove_widget(self.botao_start)
        self.nave = Rectangle(size=(50, 30), pos=(Window.width // 2 - 25, 50))
        self.criar_inimigos()
        self.add_widget(self.placar_label)

        Clock.schedule_interval(self.update, 1.0 / 60.0)



    def mover_nave(self, instance, touch):
        if touch.x > self.nave.pos[0] and touch.x < self.nave.pos[0] + self.nave.size[0]:
            self.nave.pos = (touch.x - self.nave.size[0] / 2, self.nave.pos[1])

    def atirar_bala(self, instance, touch):
        if len(self.balas) < 5:
            pos_x = self.nave.pos[0] + self.nave.size[0] / 2
            bala = Rectangle(size=(5, 20), pos=(pos_x, self.nave.pos[1] + self.nave.size[1]))


    def update(self, dt):
        for bala in self.balas[:]:
            bala.pos = (bala.pos[0], bala.pos[1] + self.velocidade_bala)
            if bala.pos[1] > Window.height:
                self.balas.remove(bala)

        for inimigo in self.inimigos[:]:
            inimigo.pos = (inimigo.pos[0], inimigo.pos[1] - self.velocidade_inimigos)
            if inimigo.pos[1] < 50:
                self.inimigos.remove(inimigo)

            for bala in self.balas[:]:
                if (bala.pos[0] < inimigo.pos[0] + inimigo.size[0] and
                        bala.pos[0] + bala.size[0] > inimigo.pos[0] and
                        bala.pos[1] < inimigo.pos[1] + inimigo.size[1] and
                        bala.pos[1] + bala.size[1] > inimigo.pos[1]):
                    self.balas.remove(bala)
                    self.inimigos.remove(inimigo)
                    self.placar += 1
                    self.placar_label.text = f'Placar: {self.placar}'
                    break

        self.canvas.clear()
        with self.canvas:

            if self.nave:
                Color(0, 1, 0)  # Cor verde
                self.nave

            Color(1, 0, 0)
            for bala in self.balas:
                bala

            Color(1, 1, 0)
            for inimigo in self.inimigos:
                inimigo

class InvasorApp(App):
    def build(self):
        jogo = Jogo()
        return jogo

"""