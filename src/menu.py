import pyglet
from src.process import Process
from pathlib import Path
from src.botoes.botao_main import Botao, BotaoInput
#from src.escalonador import scheduling_FIFO

class MeuMenu(pyglet.window.Window):
    def __init__(self, width, height):
        super().__init__(width = 1366, height = 768,
            caption="Menu dos Processos")

        self.process = []

        self.contagem = 1

        self.sobrecarga = Botao(1030,20,150,70,"Sobrecarga = 1",self.turnaround)

        self.execution_time = BotaoInput(30, 680, 250, 70, "Duração:")

        self.quantum = BotaoInput(830, 20, 150, 70, "Quantum:")

        self.arrival_time = BotaoInput(305, 680, 250, 70, "Tempo de Chegada:")

        self.deadline = BotaoInput(580, 680, 250, 70, "Deadline:")

        self.add_process = Botao(855 ,680,325,70,"Criar Processo",self.addprocess)

        self.EDF = Botao(30,20,150,70,"EDF",self.edf)

        self.FIFO = Botao(230,20,150,70,"FIFO",self.fifo)

        self.SJF = Botao(630,20,150,70,"SJF",self.sjf)

        self.ROUND_ROBIN = Botao(430,20,150,70,"Round Robin",self.rr)

        self.fundo = pyglet.image.load(Path('sprites/fundomenu.jpg'))

        self.background = pyglet.sprite.Sprite(self.fundo)

        self.widgets = [self.EDF,self.FIFO,self.SJF,self.ROUND_ROBIN,self.add_process,self.sobrecarga]

        self.editaveis = [self.execution_time,self.quantum,self.arrival_time,self.deadline]

        self.logo = pyglet.image.load(Path('sprites/ufba-png-1.png'))

        self.sprite = pyglet.sprite.Sprite(self.logo)

        self.sprite2 = pyglet.sprite.Sprite(self.logo)

        self.sprite.position = 1245,20,0

        self.sprite2.position = 1245,670,0

        self.sprite.scale = 0.2

        self.sprite2.scale = 0.2

        self.linhasup = pyglet.shapes.BorderedRectangle(2,635, self.width, 20, color=(128,0,0), border_color=(255, 255, 255))

        self.linhainf = pyglet.shapes.BorderedRectangle(2, self.height - 650, self.width, 20, color=(128,0,0), border_color=(255, 255, 255))
                 

    def addprocess(self):
         
        if self.execution_time.label.text != "" and self.deadline.label.text != "" and self.arrival_time.label.text != "":

            self.duracaoprocesso = int(self.execution_time.valor)

            self.tempochegadaprocesso = int(self.arrival_time.valor)

            self.deadlineprocesso = int(self.deadline.valor)

            self.process.append(Process(self.contagem,self.duracaoprocesso,self.tempochegadaprocesso,self.deadlineprocesso))

            print(self.process)
        else:
            print("Atributos não preenchidos corretamente!")

    def turnaround(self): 
        pass

    def rr(self):
        pass

    def sjf(self):
        pass

    def fifo(self):
        #scheduling_FIFO(self.process) 
        pass
        

    def edf(self):
        pass
        
    def on_draw(self):
        self.clear()
        self.background.draw()
        for widget in self.widgets:
            widget.draw()
        for widget in self.editaveis:
            widget.draw()
        self.linhasup.draw()
        self.linhainf.draw()
        self.sprite.draw()
        self.sprite2.draw()
        
    def on_text(self, text):
        for widget in self.editaveis:
            widget.digita(text)
        
    def on_key_press(self, symbol, modifiers):
        for widget in self.editaveis:
            if symbol == pyglet.window.key.BACKSPACE:
                widget.digita("BACKSPACE")
            if symbol == pyglet.window.key.ENTER:
                widget.valor = widget.label.text
                print(widget.valor)

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.widgets:
            widget.clica(x, y)
        for widget in self.editaveis:
            widget.clica(x,y)

