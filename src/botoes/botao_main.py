import pyglet
import pyglet.shapes
numeros = ["0","1","2","3","4","5","6","7","8","9"]

class Widget:

    def __init__(self, x, y, width, height, texto,current_window = None):
        
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
        self.current_window = current_window
    def is_clicked(self, x, y):
        return self.current_window == "Menu" and self.x <= x <= self.x + self.width \
            and self.y <= y <= self.y + self.height
    
    def draw(self):
        self.moldura.draw()
        self.label.draw()

    def __repr__(self):
        return f"Botão '{self.texto}'"


class BotaoInput:
    def __init__(self, x, y, width, height, texto=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
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
        
    def is_clicked(self, x, y):
        return self.x <= x <= self.x + self.width \
and self.y <= y <= self.y + self.height
    
    def draw(self):
        self.moldura.draw()
        self.linha.draw()
        self.label.draw()

    def clica(self, x, y):
        self.selecionado = False
        if self.is_clicked(x,y):
            self.on_click()
        
        
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
        else:
            print("Erro, digite apenas números !")

    def __repr__(self):
        return f"Input '{self.texto}'"