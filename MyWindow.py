import pyglet
from pyglet import gl
from pathlib import Path
from Process import Process
from src.Rectangle import Rectangle
from src.botoes.botao_main import BotaoInput,Widget
from collections import deque
from quadradosprocessos import ProcessSquare


HEIGHT = 40
class MyWindow(pyglet.window.Window):
  def __init__(self, width, height):
    super().__init__(width=1366, height=768, caption = "Menu dos Processos")
    # self.processes = [Process(1,5,5,4),Process(2,5,1,3),Process(3,5,5,6),Process(4,10,1,5)]
    self.processes = []
    self.window = "Menu"
    self.x_square = 25
    self.squares = [ProcessSquare(0,0,0,Process(0,0,0))]
    self.y_square = 400
    self.squareIndex = 0
    """
      Gantt Chart
    """
    self.batch = pyglet.graphics.Batch()
    self.rects = []
    self.current_index = 0
    self.speed = 0.2
    self.turnaround = 0
    self.pixels_time_ratio = 20
    """
      Menu
    """
    self.contagem = 1
    
    self.xSquaresPosition = [50*i for i in range(1,self.contagem)]

    self.sobrecarga = Widget(1030,20,150,70,"Sobrecarga = 1",self.window)

    self.execution_time = BotaoInput(30, 680, 250, 70, "Duração:")

    self.quantum = BotaoInput(830, 20, 150, 70, "Quantum:")

    self.arrival_time = BotaoInput(305, 680, 250, 70, "Tempo de Chegada:")

    self.deadline = BotaoInput(580, 680, 250, 70, "Deadline:")

    self.add_process = Widget(855 ,680,325,70,"Criar Processo",self.window)

    self.EDF = Widget(30,20,150,70,"EDF",self.window)

    self.FIFO = Widget(230,20,150,70,"FIFO",self.window)

    self.SJF = Widget(630,20,150,70,"SJF",self.window)

    self.ROUND_ROBIN = Widget(430,20,150,70,"Round Robin",self.window)

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

  def on_mouse_release(self, x, y, button, modifiers):
    for widget in self.widgets:
      if widget == self.sobrecarga:
        continue

      if widget == self.add_process and widget.is_clicked(x,y):
        self.addprocess()
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
    self.sprite2.draw()
  
  def addprocess(self):
         
    if self.execution_time.label.text != "" and self.deadline.label.text != "" and self.arrival_time.label.text != "":

      self.duracaoprocesso = int(self.execution_time.valor)

      self.tempochegadaprocesso = int(self.arrival_time.valor)

      self.deadlineprocesso = int(self.deadline.valor)

      # Adjust the time to pixels units
      self.processes.append(Process(self.contagem,self.duracaoprocesso * self.pixels_time_ratio,self.tempochegadaprocesso * self.pixels_time_ratio,self.deadlineprocesso * self.pixels_time_ratio))
      
      square = ProcessSquare(self.x_square, self.y_square, 200, Process(self.contagem,self.duracaoprocesso,self.tempochegadaprocesso,self.deadlineprocesso))
      self.squares.append(square)
      self.x_square += 250

      self.contagem += 1

    else:
      print("Atributos não preenchidos corretamente!")

      
  def update(self,dt):
    
    rect = self.rects[self.current_index]

    if rect.width < rect.desired_width:
      rect.width += self.speed
    else:
      self.current_index += 1
      if self.current_index >= len(self.rects):
        pyglet.clock.unschedule(self.update)  # Stop the animation if all rectangles are drawn

  def draw_graph(self):
    gl.glClearColor(1, 1, 1, 1)  # Set background color to white
    self.clear()

    # Draw x-axis line
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES
                          # Extend line across window width
                          )
    line = pyglet.shapes.Line(50, 45, 1300, 45, width=1, color=(0, 0, 0))
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
    prev_end = 50  # Set the initial x-position to the beginning of the x-axis line
    
    for i, process in enumerate(self.processes):

      rectangle = Rectangle(x=prev_end, y=50 + i * 50, desired_width= process.duration,width=0, height=HEIGHT,color=(0, 255, 0), id='P'+str(process.id), nature = "process", batch=self.batch)

      self.rects.append(rectangle)
      prev_end += process.duration

    
  
  def scheduling_SJF(self):
    
    self.processes.sort(key = lambda p: (p.arrival_time,p.duration))
    return self.scheduling_FIFO()
    

  def scheduling_Round_Robin(self, overload = 20):
    quantum = int(self.quantum.valor) * self.pixels_time_ratio
    ready_queue = deque()
    current_time = 0
    total_processes = len(self.processes)
    completed_processes = []    
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
        current_time += 1
        continue

      current_process = ready_queue.popleft()

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
        overload_rectangle = Rectangle(x = prev_end, y = y_rects_positions[current_process.id-1], width= 0,desired_width=overload, height=HEIGHT, color = (255,0,0),id = "", nature = "quantum")
        prev_end += overload
        self.rects.append(process_rectangle)
        self.rects.append(overload_rectangle)
        
        
        current_time += quantum
        current_process.duration -= quantum
        ready_queue.append(current_process)
   
  def scheduling_EDF(self,overload = 20):
    quantum = int(self.quantum.valor) * self.get_pixel_ratio
    ready_queue = deque()
    current_time = 0 
    total_processes = len(self.processes)
    completed_processes = []
    self.processes.sort(key = lambda p: (p.arrival_time,p.deadline))
    
    y_rects_positions= [50*i for i in range(1,len(self.processes)+1)]
    next_process_index = 0

    prev_end = 50
    while len(completed_processes) < total_processes:
      for i in range(next_process_index,total_processes):

        if self.processes[i].arrival_time <= current_time:
          ready_queue.append(self.processes[i])
          next_process_index = i + 1
      
      if len(ready_queue) == 0:
        current_time += 1
        prev_end += current_time
        continue
      

      current_process = ready_queue.popleft()

      if current_process.deadline > current_time:
        # Draw Deadline burst 
        pass
      
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
        overload_rectangle = Rectangle(x = prev_end, y = y_rects_positions[current_process.id-1], width= 0,desired_width=overload, height=HEIGHT, color = (255,0,0),id = "", nature = "quantum")
        prev_end += overload
        self.rects.append(process_rectangle)
        self.rects.append(overload_rectangle)
        
        
        current_time += quantum
        current_process.duration -= quantum
        current_process.deadline -= quantum
        # If the process isnt finished, we add it do the end of queue
        ready_queue.append(current_process)
      

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


  def draw_squares(self):
    pass

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

    if self.window == "FIFO":
      self.scheduling_FIFO()
      self.batch.draw()
      self.start_animation()
    elif self.window == "SJF":
      self.scheduling_SJF()
      self.batch.draw()
      self.start_animation()
    
    elif self.window == "Round Robin":
      self.scheduling_Round_Robin()
      self.batch.draw()
      self.start_animation()
    
    elif self.window == "EDF":
      self.scheduling_EDF()
      self.batch.draw()
      self.start_animation()

  def start_animation(self):

    pyglet.clock.schedule_interval(self.update, 1/60)  # Update the animation 60 times per second




screen = MyWindow(1920,1080)
icon = pyglet.image.load(Path('sprites/blackjack_icon.png'))
screen.set_icon(icon)

pyglet.app.run()

