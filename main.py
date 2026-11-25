from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.clock import Clock
from kivy.core.window import Window
from random import choice, randint, uniform

COLORS = [(1, .24, .24), (.24, 1, .47), (.24, .59, 1),
          (1, .86, .24), (1, .31, 1), (.24, 1, 1), (1, .55, .16)]


class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.lives = 3
        self.drops = []
        self.basket_w = 140
        self.basket_h = 24
        self.basket_x = None
        self.basket_color = choice(COLORS)
        self.frame = 0
        self.game_over = False
        self.touch_x = None
        Clock.schedule_interval(self.update, 1 / 60)

    def on_touch_down(self, touch):
        self.touch_x = touch.x
        if self.game_over:
            self.restart()
        return True

    def on_touch_move(self, touch):
        self.touch_x = touch.x
        return True

    def restart(self):
        self.drops = []
        self.score = 0
        self.lives = 3
        self.game_over = False

    def spawn(self):
        self.drops.append({
            "x": randint(30, int(self.width) - 30),
            "y": self.height + 20,
            "speed": uniform(2, 4) + self.score * 0.05,
            "color": choice(COLORS),
        })

    def update(self, dt):
        if self.basket_x is None:
            self.basket_x = self.width / 2
        if self.touch_x is not None:
            self.basket_x = self.touch_x
        half = self.basket_w / 2
        self.basket_x = max(half, min(self.width - half, self.basket_x))

        if not self.game_over:
            self.frame += 1
            if self.frame % max(15, 45 - self.score) == 0:
                self.spawn()
            basket_y = 70
            for d in self.drops[:]:
                d["y"] -= d["speed"]
                caught = (d["y"] - 20 <= basket_y + self.basket_h and
                          d["y"] + 20 >= basket_y and
                          self.basket_x - half <= d["x"] <= self.basket_x + half)
                if caught:
                    self.drops.remove(d)
                    self.score += 1
                    self.basket_color = d["color"]
                elif d["y"] < -20:
                    self.drops.remove(d)
                    self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(.08, .08, .14)
            Rectangle(pos=self.pos, size=self.size)
            for d in self.drops:
                Color(*d["color"])
                Ellipse(pos=(d["x"] - 20, d["y"] - 20), size=(40, 40))
            Color(*self.basket_color)
            half = self.basket_w / 2
            Rectangle(pos=(self.basket_x - half, 70), size=(self.basket_w, self.basket_h))
            Color(1, 1, 1)
            Line(rectangle=(self.basket_x - half, 70, self.basket_w, self.basket_h), width=1.5)
            Color(1, .3, .3)
            Rectangle(pos=(self.width - 120, self.height - 40), size=(12 * self.lives, 12))
        if self.game_over:
            from kivy.uix.label import Label
            self.clear_widgets()
            lbl = Label(text=f"GAME OVER\nScore: {self.score}\nTap to restart",
                        font_size='28sp', halign='center',
                        pos=(self.width / 2 - 150, self.height / 2 - 60),
                        size=(300, 120))
            self.add_widget(lbl)
        else:
            self.clear_widgets()


class ShapeCatcherApp(App):
    def build(self):
        Window.clearcolor = (.08, .08, .14, 1)
        return Game()


if __name__ == "__main__":
    ShapeCatcherApp().run()