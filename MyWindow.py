import pyglet
from pyglet import gl
from Process import Process
from src.Rectangle import Rectangle
import queue

HEIGHT = 40
class MyWindow(pyglet.window.Window):
  def __init__(self, width, height):
    super().__init__(width=1366, height=768)
    self.processes = [Process(1,200,5,5),Process(2,180,1,3),Process(3,50,1,6)]
    self.batch = pyglet.graphics.Batch()
    self.rects = []
    self.turnaround = 0

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

  def scheduling_FIFO(self):
     
    self.processes.sort(key=lambda p: p.arrival_time)
    prev_end = 50  # Set the initial x-position to the beginning of the x-axis line
    # rects = []
    

    for i, process in enumerate(self.processes):
        # rectangle = pyglet.shapes.Rectangle(x=prev_end, y=50 + i * 50, width=process.duration, height=HEIGHT,color=(0, 255, 0))
        rectangle = Rectangle(x=prev_end, y=50 + i * 50, width=process.duration, height=HEIGHT,color=(0, 255, 0), id='P'+str(process.id), nature = "process", batch=self.batch)
        self.rects.append(rectangle)
        prev_end += process.duration

    
  
  def scheduling_SJF(self):
    
    self.processes.sort(key = lambda p: (p.arrival_time,p.duration))
    return self.scheduling_FIFO()
    

  def scheduling_Round_Robin(self,quantum = 20, overload = 10):
    prev_end = 50
    counter = 0

    
    q = self.processes
    
    y_rects_positions= [50*i for i in range(1,len(q)+1)]
    

    while len(q) != 0:
      process = q.pop(0)

      process_rectangle = None
      
      if process.duration <= quantum:

        process_rectangle = Rectangle(x = prev_end, y = y_rects_positions[process.id-1],width= process.duration,height=HEIGHT, color = (0,255,0), id = 'P'+str(process.id), nature = "process")
        prev_end += process.duration

      else:

        process_rectangle = Rectangle(x = prev_end, y = y_rects_positions[process.id-1],width= quantum,height=HEIGHT, color = (0,255,0), id = 'P'+str(process.id), nature = "process")

        prev_end += quantum
        overload_rectangle = Rectangle(x = prev_end, y = y_rects_positions[process.id-1], width= overload, height=HEIGHT, color = (255,0,0),id = "", nature = "quantum")

        self.rects.append(overload_rectangle)
        self.turnaround += self.turnaround + quantum
        prev_end += overload
    

      self.rects.append(process_rectangle)
     


      process.duration -= quantum
      if process.duration > 0:
        q.append(process)
      
      
   
  def scheduling_EDF(self, quantum = 20,overload = 10):
    
    q = self.processes
    
    y_rects_positions= [50*i for i in range(1,len(q)+1)]
    prev_end = 50
    
    
    while len(q) != 0:
      process = min(q)
      q.remove(process)
      process_rectangle = Rectangle(x = prev_end, y = y_rects_positions[process.id-1],width= quantum,height=HEIGHT, color = (0,255,0), id = 'P'+ str(process.id), nature = "process")

      overload_rectangle = Rectangle(x = prev_end + quantum, y =y_rects_positions[process.id-1], width= overload, height=HEIGHT, color = (255,0,0),id = "", nature = "quantum")

      self.rects.append(process_rectangle)
      self.rects.append(overload_rectangle)
      prev_end += overload + quantum

      process.duration -= quantum
      if process.duration > 0:
        
        q.append(process)



 
  def on_draw(self):
    self.clear()
    self.draw_graph()

    self.scheduling_Round_Robin()
    
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




menu = MyWindow(1920,1080)

pyglet.app.run()