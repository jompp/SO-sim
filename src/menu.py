import pyglet
from src.process import Process
from pathlib import Path
from src.botoes.botao_main import Botao, BotaoInput
from src.Rectangle import Rectangle
from pyglet import gl
import queue
#from src.escalonador import scheduling_FIFO
HEIGHT = 40
class MeuMenu(pyglet.window.Window):
    def __init__(self, width, height):
        super().__init__(width = 1366, height = 768,
            caption="Menu dos Processos")

        self.window = "Menu"
        self.processes = [Process("P1",100,0,5),Process("P2",150,0,3),Process("P3",50,0,6)]

        self.contagem = 1
        
        self.process = []
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

        self.sprite.position = 1245,20

        self.sprite2.position = 1245,670

        self.sprite.scale = 0.2

        self.sprite2.scale = 0.2

        self.linhasup = pyglet.shapes.BorderedRectangle(2,635, self.width, 20, color=(128,0,0), border_color=(255, 255, 255))

        self.linhainf = pyglet.shapes.BorderedRectangle(2, self.height - 650, self.width, 20, color=(128,0,0), border_color=(255, 255, 255))
                 
    def draw_graph(self):
        gl.glClearColor(1, 1, 1, 1)  # Set background color to white
        self.clear()

        # Draw x-axis line
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                            # Extend line across window width
                            ('v2f', [50, 50, self.width - 50, 50]),
                            # Set line color to black
                            ('c3B', (0, 0, 0, 0, 0, 0))
                            )

        # Draw x-axis labels
        label_interval = 5
        # Adjust label_count based on window width
        label_count = (self.width - 100) // 100
        label_width = (self.width - 100) // label_count

        for i in range(label_count + 1):
            label = str(i * label_interval)
            x_pos = 50 + i * label_width - len(label) * 5

            pyglet.text.Label(
                label,
                font_size=12,
                x=x_pos,
                y=30,
                anchor_x='center',
                anchor_y='top',
                color=(0, 0, 0, 255)  # Set label color to black
            ).draw()

    def draw_gantt_chart(self):
        self.clear()
        self.draw_graph()

        rects = self.scheduling_SJF()
        for i,rect in enumerate(rects):
            rect.draw()

        # Draw process labels on the y-axis
        # label = self.processes[i].id

            if rect.nature == "process":

                label = rect.id
                y_pos = rect.y + rect.height // 2

                pyglet.text.Label(
                    label,
                    font_size=12,
                    x=30,
                    y=y_pos,
                    anchor_x='right',
                    anchor_y='center',
                    color=(0, 0, 0, 255)  # Set label color to black
                ).draw()
    def addprocess(self):
         
        if self.execution_time.label.text != "" and self.deadline.label.text != "" and self.arrival_time.label.text != "":

            self.duracaoprocesso = int(self.execution_time.valor)

            self.tempochegadaprocesso = int(self.arrival_time.valor)

            self.deadlineprocesso = int(self.deadline.valor)

            self.process.append(Process(self.contagem,self.duracaoprocesso,self.tempochegadaprocesso,self.deadlineprocesso))

            print(self.process)
        else:
            print("Atributos não preenchidos corretamente!")

    def fifo(self):
        pass

    def sjf(self):
        pass
    def turnaround(self): 
        pass

    def rr(self):
        pass

    def scheduling_SJF(self):
        def get_durations(process):
            return process.duration
        
        self.processes.sort(key = get_durations)
        return self.scheduling_FIFO()
    
    def scheduling_FIFO(self):
        prev_end = 50  # Set the initial x-position to the beginning of the x-axis line
        rects = []

        for i, process in enumerate(self.processes):
            # rectangle = pyglet.shapes.Rectangle(x=prev_end, y=50 + i * 50, width=process.duration, height=HEIGHT,color=(0, 255, 0))
            rectangle = Rectangle(x=prev_end, y=50 + i * 50, width=process.duration, height=HEIGHT,color=(0, 255, 0), id=process.id, nature = "process")
            rects.append(rectangle)
            prev_end += process.duration

        return rects

    def edf(self):
        pass
    
    def draw_menu(self):
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
        
    def on_draw(self):
        if self.window == "Menu":
            self.draw_menu()
        else:
            self.draw_gantt_chart()
        
    def on_text(self, text):
        for widget in self.editaveis:
            widget.digita(text)
        
    def on_key_press(self, symbol, modifiers):
        for widget in self.editaveis:
            if symbol == pyglet.window.key.BACKSPACE:
                widget.digita("BACKSPACE")
            if symbol == pyglet.window.key.ENTER:
                widget.valor = widget.label.text

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.widgets:
            widget.clica(x, y)
        for widget in self.editaveis:
            widget.clica(x,y)


# window1 = MeuMenu(1366,768)
# icon = pyglet.image.load(Path('sprites/blackjack_icon.png'))
# window1.set_icon(icon)


# pyglet.app.run()