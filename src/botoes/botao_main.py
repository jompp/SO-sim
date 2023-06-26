import pyglet
import pyglet.shapes
numeros = ["0","1","2","3","4","5","6","7","8","9"]

class Widget:

    def __init__(self, x, y, width, height, texto):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texto = texto
        self.moldura = pyglet.shapes.BorderedRectangle(x, y, width, height, color=(128,0,0), border_color=(255, 255, 255))
        self.label = pyglet.text.Label(self.texto,
                font_name='Times New Roman',
                font_size=18,
                anchor_x='center', anchor_y='center',
                x = self.x + self.width // 2,
                y = self.y + self.height // 2)

    def contem_ponto(self, x, y):
        return x >= self.x and x <= self.x + self.width \
            and y >= self.y and y <= self.y + self.height

    def clica(self, x, y):
        if self.contem_ponto(x, y):
            self.on_click()
    
    def draw(self):
        self.moldura.draw()
        self.label.draw()

    def __repr__(self):
        return f"Botão '{self.texto}'"

class Botao(Widget):
    def __init__(self, x, y, width, height, texto, func):
        super().__init__(x, y, width, height, texto)
        self.on_click = func

class BotaoInput(Widget):
    def __init__(self, x, y, width, height, texto=""):
        super().__init__(x, y, width, height,texto)
        self.selecionado = False
        self.texto = texto
        self.valor = 0
        self.moldura = pyglet.shapes.BorderedRectangle(x, y, width, height, color=(128,0,0), border_color=(255, 255, 255))
        self.linha = pyglet.shapes.Line(x, y + 5, x + width, y + 5)
        self.label = pyglet.text.Label(self.texto,
                font_name='Times New Roman',
                font_size=18,
                anchor_x='center', anchor_y='center',
                x = self.x + self.width // 2,
                y = self.y + self.height // 2)
    def draw(self):
        self.moldura.draw()
        self.linha.draw()
        self.label.draw()
    def clica(self, x, y):
        self.selecionado = False
        super().clica(x, y)
    def on_click(self):
        self.selecionado = True
        self.label.text = ""
        
    def digita(self, symbol):
        if not self.selecionado:
            return
        elif symbol == "BACKSPACE":
            self.label.text = self.label.text[0:-1]
        elif symbol in numeros:
            self.label.text += symbol
        elif symbol == "ENTER":
            pass
        else:
            print("Erro, digite apenas números !")

    def __repr__(self):
        return f"Input '{self.texto}'"