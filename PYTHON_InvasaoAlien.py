import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock

class Jogo(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.nave = Rectangle(size=(50,30), pos=(Window.width // 2 - 25, 50))
        self.balas = []
        self.inimigos = []
        self.placar = 0

        self.criar_inimigos()

        self.bind(on_touch_move=self.mover_nave)
        self.bind(on_touch_down=self.atirar_bala)

        self.velocidade_bala = 10
        self.velocidade_inimigos = 2

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def criar_inimigos(self):
        for i in range(5):
            for j in range(5):
                pos_x = 100 + (i*60)
                pos_y = 400 + (j+50)
                inimigo = Rectangle(size=(50,30), pos=(pos_x, pos_y))
                self.inimigos.append(inimigo)

    def mover_nave(self, instance, touch):
        if touch.x > self.nave.pos[0] and touch.x < self.nave.pos[0] + self.nave.size[0]:
            self.nave.pos = (touch.x - self.nave.size[0] / 2, self.nave.pos[1])

    def atirar_bala(self, instance, touch):
        if len(self.balas) < 5:
            pos_x = self.nave.pos[0] + self.nave.size[0] / 2
            bala = Rectangle(size=(5, 20), pos=(pos_x, self.nave.pos[1] + self.nave.size[1]))
            self.balas.append(bala)

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
                    break

        self.canvas.clear()
        with self.canvas:
            Color(0,1,0)
            self.nave

            Color(1,0,0)
            for bala in self.balas:
                bala

            Color(1,1,0)
            for inimigo in self.inimigos:
                inimigo

            self.desenhar_placar()

    def desenhar_placar(self):
        placar_label = Label(text=f'Placar: {self.placar}', font_size=20, color=(1,1,1,1))
        placar_label.pos = (10,Window.height - 30)
        self.add_widget(placar_label)

class InvasorApp(App):
    def build(self):
        jogo = Jogo()
        return jogo

if __name__== '__main__':
    InvasorApp().run()