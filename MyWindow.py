import pyglet
from pyglet import gl
from pathlib import Path
from collections import deque
import queue
from Process import Process
from src.Rectangle import Rectangle
from src.botoes.botao_main import BotaoInput,Widget
from quadradosprocessos import ProcessSquare
# from MemoryWindow import MemoryWindow
from Grid import Grid

HEIGHT = 40
class MyWindow(pyglet.window.Window):
  def __init__(self, width, height):
    super().__init__(width=1366, height=768,caption = "MENU")
    # self.processes = [Process(1,5,5,4),Process(2,5,1,3),Process(3,5,5,6),Process(4,10,1,5)]
    self.processes = []
    self.processes_right_order = []
    self.window = "Menu"
    self.x_square = 80
    self.squares = []
    self.y_square = 290
    self.squareIndex = 0

    """
      Gantt Chart
    """
    self.batch = pyglet.graphics.Batch()
    self.rects = []
    self.current_rect_index = 0
    self.current_process_index = 0
    self.speed = 0.5
    self.turnaround = 0
    self.pixels_time_ratio = 20
    self.window_update_counter = 1

    """
      Memoria
    """
    # Na tela do gantt teremos dois grids, um de disco e outro de RAM
    self.ram = Grid(memory="RAM")
    self.disk = Grid(memory="Disk")

    """
      Menu
    """
    self.contagem = 1
    self.sobrecarga = Widget(1030,10,150,70,"Sobrecarga = 1",self.window)

    self.execution_time = BotaoInput(30, 660, 150, 70, "Duração:")

    self.quantum = BotaoInput(830, 10, 150, 70, "Quantum:")

    self.arrival_time = BotaoInput(205, 660, 150, 70, "Chegada:")

    self.deadline = BotaoInput(390, 660, 150, 70, "Deadline:")

    self.pages = BotaoInput(575,660,150,70,"Páginas:")

    self.eraseprocesses = Widget(760 ,660,200,70,"Apagar Processos",self.window)

    self.add_process = Widget(1000 ,660,325,70,"Criar Processo",self.window)

    self.EDF = Widget(630,50,150,30,"EDF",self.window)

    self.FIFO = Widget(430,50,150,30,"FIFO",self.window)

    self.SJF= Widget(630,10,150,30,"SJF",self.window)

    self.LRUPAGE = Widget(25,10,150,70,"LRU",self.window)

    self.FIFOPAGE = Widget(205,10,150,70,"FIFO",self.window)

    self.ROUND_ROBIN = Widget(430,10,150,30,"Round Robin",self.window)

    self.fundo = pyglet.image.load(Path('sprites/fundomenu.jpg'))

    self.background = pyglet.sprite.Sprite(self.fundo)

    self.widgets = [self.EDF,self.FIFO,self.SJF,self.ROUND_ROBIN,self.add_process,self.sobrecarga,self.eraseprocesses,self.FIFOPAGE,self.LRUPAGE]

    self.editaveis = [self.execution_time,self.quantum,self.arrival_time,self.deadline,self.pages]

    self.logo = pyglet.image.load(Path('sprites/ufba-png-1.png'))

    self.sprite = pyglet.sprite.Sprite(self.logo)

    self.sprite2 = pyglet.sprite.Sprite(self.logo)

    self.sprite.position = 1245,20,0

    self.sprite.scale = 0.2

    self.linhasup = pyglet.shapes.Rectangle(2,600, self.width, 20, color=(128,0,0))

    self.linhainf = pyglet.shapes.Rectangle(2, self.height - 615, self.width, 20, color=(128,0,0))

    self.linhaSep1 = pyglet.shapes.Rectangle(380,0, 30, self.height - 615, color=(128,0,0))

    self.linhaSep2 = pyglet.shapes.Rectangle(790,0, 30, self.height - 615, color=(128,0,0))

    self.back2menu = Widget(630,60,150,30,"MENU",self.window)
    
    self.paginationlabel = pyglet.text.Label("ESCALONAMENTO DE PÁGINA",font_name= "Times New Roman",font_size=18,
                                          x=190, y= 140,
                                          anchor_x='center', anchor_y='top', color=(128, 0, 0, 255))
    
    self.schedulingLabel = pyglet.text.Label("ESCALONAMENTO DE PROCESSO",font_name= "Times New Roman",font_size=18,
                                          x=600, y= 140,
                                          anchor_x='center', anchor_y='top', color=(128, 0, 0, 255))
    


  def on_mouse_release(self, x, y, button, modifiers):
    for widget in self.widgets:
      if widget == self.sobrecarga:
        continue

      if widget == self.add_process and widget.is_clicked(x,y):
        self.addprocess()
        continue

      if widget == self.eraseprocesses and widget.is_clicked(x,y):
        self.apagarprocessos()
        continue
      
      if widget == self.LRUPAGE and widget.is_clicked(x,y):
        self.pagination = "LRU"
        print("Algoritmo de Paginação: " + self.pagination)
        continue

      if widget == self.FIFOPAGE and widget.is_clicked(x,y):
        self.pagination = "FIFO"
        print("Algoritmo de Paginação: " + self.pagination)
        continue
      
      if widget.is_clicked(x,y):
        self.window = widget.texto
      
    for widget in self.editaveis:
      widget.clica(x,y)

  def on_key_press(self, symbol, modifiers):
    for widget in self.editaveis:
      if symbol == pyglet.window.key.BACKSPACE:
        widget.digita("BACKSPACE")
      if symbol == pyglet.window.key.ENTER:
        widget.valor = widget.label.text

      
  def on_text(self, text):
    for widget in self.editaveis:
      widget.digita(text)

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
    self.linhaSep1.draw()
    self.linhaSep2.draw()
    self.paginationlabel.draw()
    self.schedulingLabel.draw()

  
  def addprocess(self):
    if self.contagem < 6:    
      if self.execution_time.label.text != "" and self.deadline.label.text != "" and self.arrival_time.label.text != "" and self.pages.label.text != "":

        self.duracaoprocesso = int(self.execution_time.valor)

        self.tempochegadaprocesso = int(self.arrival_time.valor)

        self.deadlineprocesso = int(self.deadline.valor)

        self.pagesprocesso = int(self.pages.valor)

        # Adjust the time to pixels units
        self.processes.append(Process(self.contagem,self.duracaoprocesso * self.pixels_time_ratio,self.tempochegadaprocesso * self.pixels_time_ratio,self.deadlineprocesso * self.pixels_time_ratio,self.pagesprocesso))
      
        square = ProcessSquare(self.x_square, self.y_square, 200, Process(self.contagem,self.duracaoprocesso,self.tempochegadaprocesso,self.deadlineprocesso,self.pagesprocesso))
        self.squares.append(square)
        self.x_square += 250
        self.contagem += 1
      
      else:
        print("Atributos não preenchidos corretamente!")
    else:
      print("Número máximo de processos atingido !")
      
  def apagarprocessos(self):
      self.processes.clear()
      self.squares.clear()
      self.x_square = 80
      self.contagem = 1

  def update(self,dt):
    self.window_update_counter += 1
    rect = self.rects[self.current_rect_index]
    
    if rect.width < rect.desired_width:
      rect.width += self.speed
    else:
      self.current_rect_index += 1
      if rect.nature == "process":
        self.current_process_index += 1

      if self.current_rect_index >= len(self.rects):
        pyglet.clock.unschedule(self.update)  # Stop the animation if all rectangles are drawn

  def draw_graph(self):
    gl.glClearColor(1, 1, 1, 1)  # Set background color to white
    self.clear()

    # Draw x-axis line
 
    line = pyglet.shapes.Rectangle(50, 48, 1265, 2, color=(0, 0, 0))
    line.draw()

    # Draw x-axis labels
    label_interval = 5
    # Adjust label_count based on window width
    label_count = (self.width - 100) // 100
    label_width = (self.width - 100) // label_count


    for i in range(label_count + 1):
      label = str(i * label_interval)
      x_pos = 50 + i * label_width - len(label) * 5
      time_range = i * label_interval
      
      
      pyglet.text.Label(
          label,
          font_size=12,
          x=x_pos,
          y=30,
          anchor_x='center',
          anchor_y='top',
          color=(0, 0, 0, 255)  # Set label color to black
      ).draw()


  def scheduling_FIFO(self):
    
    self.processes.sort(key=lambda p: p.arrival_time)
    self.processes_right_order = self.processes
    prev_end = 50  # Set the initial x-position to the beginning of the x-axis line

    for i, process in enumerate(self.processes):
      # Antes de executar o algoritmo, precisamos alocar ele na memoria e garantir q tds as paginas estão la
       
      # Verifica se o processo não chegou na fila de prontos no tempo em que o ultimo acabou 
      if prev_end - 50 < process.arrival_time:
        prev_end = process.arrival_time + 50

      rectangle = Rectangle(x=prev_end, y=50 + i * 50, desired_width= process.duration,width=0, height=HEIGHT,color=(0, 255, 0), id='P'+str(process.id), nature = "process", batch=self.batch)

      self.rects.append(rectangle)
      prev_end += process.duration

    
  
  def scheduling_SJF(self):
    current_time = 0
    next_process_index = 0
    total_processes = len(self.processes)
    ready_queue = [] 
    completed_processes = 0
    right_order = []
    prev_end = 50
    self.processes.sort(key = lambda p: p.arrival_time)

    y_rects_positions= [50*i for i in range(1,len(self.processes)+1)]

    while completed_processes < total_processes:
      for i in range(next_process_index, total_processes):
        if self.processes[i].arrival_time <= current_time:
          ready_queue.append(self.processes[i])
          next_process_index = i + 1

      if len(ready_queue) == 0:
        current_time += 20
        prev_end += 20
        continue
      # Garante que pegamos sempre o de menor duração
      ready_queue.sort(key = lambda p: p.duration)
      current_process = ready_queue.pop(0)
      right_order.append(current_process)
      
      rectangle = Rectangle(x=prev_end, y=y_rects_positions[current_process.id-1], desired_width= current_process.duration,width=0, height=HEIGHT,color=(0, 255, 0), id='P'+str(current_process.id), nature = "process", batch=self.batch)

      self.rects.append(rectangle)
      prev_end += current_process.duration
      current_time += current_process.duration
      completed_processes += 1

    """"
    Os algoritmos vao executar varias vezes, na primeira vez ele vai alterar as duracoes de cada processo, entao
    so podemos pegar a ordem certa dos processos na primeira vez q ele executa, depois perdemos essa ordem
    """
    if self.window_update_counter == 1:
      self.processes_right_order = right_order
    

  def scheduling_Round_Robin(self, overload = 20):
    quantum = int(self.quantum.valor) * self.pixels_time_ratio
    ready_queue = deque()
    current_time = 0
    total_processes = len(self.processes)
    completed_processes = [] 
    right_order = []   
    self.processes.sort(key= lambda p: p.arrival_time)
 
    y_rects_positions= [50*i for i in range(1,len(self.processes)+1)]
    prev_end = 50

    next_process_index = 0
    
    while len(completed_processes) < total_processes:

      for i in range(next_process_index,total_processes):

        if self.processes[i].arrival_time <= current_time:
          ready_queue.append(self.processes[i])
          next_process_index = i + 1
      
      
      if len(ready_queue) == 0:
        prev_end += 20
        current_time += 20
        continue

      current_process = ready_queue.popleft()
      right_order.append(current_process)

      if current_process.duration <= quantum:
        process_rectangle = Rectangle(x = prev_end, y = y_rects_positions[current_process.id-1],width= 0,desired_width=current_process.duration,height=HEIGHT, color = (0,255,0), id = 'P'+str(current_process.id), nature = "process")

        current_time += current_process.duration
        prev_end += current_process.duration
        current_process.duration = 0
        completed_processes.append(current_process)
        self.rects.append(process_rectangle)
      
      else:
        process_rectangle = Rectangle(x = prev_end, y = y_rects_positions[current_process.id-1],width= 0, desired_width=quantum,height=HEIGHT, color = (0,255,0), id = 'P'+str(current_process.id), nature = "process")

        prev_end += quantum
        overload_rectangle = Rectangle(x = prev_end, y = y_rects_positions[current_process.id-1], width= 0,desired_width=overload, height=HEIGHT, color = (255,0,0),id = "", nature = "overload")
        prev_end += overload
        self.rects.append(process_rectangle)
        self.rects.append(overload_rectangle)
        
        current_time += quantum + overload
        current_process.duration -= quantum
        ready_queue.append(current_process)
        

    """"
    Os algoritmos vao executar varias vezes, na primeira vez ele vai alterar as duracoes de cada processo, entao
    so podemos pegar a ordem certa dos processos na primeira vez q ele executa, depois perdemos essa order
    """
    if self.window_update_counter == 1:
      self.processes_right_order = right_order
    

  def scheduling_EDF(self,overload = 20):
    quantum = int(self.quantum.valor) * self.pixels_time_ratio
    ready_queue = queue.PriorityQueue()
    current_time = 0 
    total_processes = len(self.processes)
    completed_processes = []
    right_order  = []
    self.processes.sort(key = lambda p: (p.arrival_time,p.deadline))
    
    y_rects_positions= [50*i for i in range(1,len(self.processes)+1)]
    next_process_index = 0

    prev_end = 50
    while len(completed_processes) < total_processes:
      for i in range(next_process_index,total_processes):

        if self.processes[i].arrival_time <= current_time:
          ready_queue.put(self.processes[i])
          next_process_index = i + 1
      
      if ready_queue.qsize() == 0:
        current_time += 20
        prev_end += 20
        continue
      

      current_process = ready_queue.get()
      right_order.append(current_process)

      if current_process.duration <= quantum:
        if current_process.deadline < current_time:
          process_rectangle = Rectangle(x = prev_end, y = y_rects_positions[current_process.id-1], width= 0, desired_width=current_process.duration, height=HEIGHT, color=(211, 211, 211), id='P'+str(current_process.id), nature = "process") 
        else:
          process_rectangle = Rectangle(x = prev_end, y = y_rects_positions[current_process.id-1],width= 0,desired_width=current_process.duration,height=HEIGHT, color = (0,255,0), id = 'P'+str(current_process.id), nature = "process")

        current_time += current_process.duration
        prev_end += current_process.duration

        current_process.duration = 0
        completed_processes.append(current_process)
        self.rects.append(process_rectangle)
        
      else:
        if current_process.deadline < current_time:
          process_rectangle = Rectangle(x = prev_end, y = y_rects_positions[current_process.id-1], width= 0, desired_width=quantum, height=HEIGHT, color=(211, 211, 211), id='P'+str(current_process.id), nature = "process") 
        else:
          process_rectangle = Rectangle(x = prev_end, y = y_rects_positions[current_process.id-1],width= 0, desired_width=quantum,height=HEIGHT, color = (0,255,0), id = 'P'+str(current_process.id), nature = "process")

        prev_end += quantum
        overload_rectangle = Rectangle(x = prev_end, y = y_rects_positions[current_process.id-1], width= 0,desired_width=overload, height=HEIGHT, color = (255,0,0),id = "", nature = "overload")
        prev_end += overload
        self.rects.append(process_rectangle)
        self.rects.append(overload_rectangle)
        
        
        current_time += quantum + overload
        current_process.duration -= quantum
        current_process.deadline -= quantum
        # If the process isnt finished, we add it do the end of queue
        ready_queue.put(current_process)

    """"
    Os algoritmos vao executar varias vezes, na primeira vez ele vai alterar as duracoes de cada processo, entao
    so podemos pegar a ordem certa dos processos na primeira vez q ele executa, depois perdemos essa order
    """
    if self.window_update_counter == 1:
      self.processes_right_order = right_order
    

  def draw_processes_labels(self):
    for i,rect in enumerate(self.rects):
      rect.draw()

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

 
  def on_draw(self):
    self.clear()
    
    if self.window == "Menu":
      self.draw_menu()
      if self.add_process.is_clicked:
        for square in self.squares:
          square.draw()
    else:
        
      self.draw_graph()
      self.draw_processes_labels()
      self.ram.draw_grid()
      self.disk.draw_grid()

    if self.window == "FIFO":
      self.scheduling_FIFO()
      self.ram.draw_processes_pages(self.processes_right_order,self.current_process_index+1,self.pagination)
      self.batch.draw()
      self.start_animation()
    elif self.window == "SJF":
      self.scheduling_SJF()
      self.ram.draw_processes_pages(self.processes_right_order,self.current_process_index+1,self.pagination)
      self.batch.draw()
      self.start_animation()
    
    elif self.window == "Round Robin":
      self.scheduling_Round_Robin()
      self.ram.draw_processes_pages(self.processes_right_order,self.current_process_index+1,self.pagination)
      self.batch.draw()
      self.start_animation()
    
    elif self.window == "EDF":
      self.scheduling_EDF()
      self.ram.draw_processes_pages(self.processes_right_order,self.current_process_index+1,self.pagination)
      self.batch.draw()
      self.start_animation()

  def start_animation(self):


    pyglet.clock.schedule_interval(self.update, 1/60)  # Update the animation 60 times per second




screen = MyWindow(1920,1080)
icon = pyglet.image.load(Path('sprites/blackjack_icon.png'))
screen.set_icon(icon)

pyglet.app.run()

