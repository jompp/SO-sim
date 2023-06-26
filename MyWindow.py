import pyglet
from pyglet import gl
from Process import Process
from Rectangle import Rectangle
import queue

HEIGHT = 40
class MyWindow(pyglet.window.Window):
  def __init__(self, width, height):
    super().__init__(width=1366, height=768)
    self.processes = [Process("P1",100,0,5),Process("P2",150,0,3),Process("P3",50,0,6)]
  
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
    prev_end = 50  # Set the initial x-position to the beginning of the x-axis line
    rects = []

    for i, process in enumerate(self.processes):
        # rectangle = pyglet.shapes.Rectangle(x=prev_end, y=50 + i * 50, width=process.duration, height=HEIGHT,color=(0, 255, 0))
        rectangle = Rectangle(x=prev_end, y=50 + i * 50, width=process.duration, height=HEIGHT,color=(0, 255, 0), id=process.id, nature = "process")
        rects.append(rectangle)
        prev_end += process.duration

    return rects
  
  def scheduling_SJF(self):
    def get_durations(process):
        return process.duration
    
    self.processes.sort(key = get_durations)
    return self.scheduling_FIFO()
    

  def scheduling_Round_Robin(self,quantum = 20, overload = 10):
    prev_end = 50
    counter = 0

    rects = []
    q = queue.Queue()
    for process in self.processes:
      q.put(process)
    

    y_label_count = len(self.processes)  # Number of labels on the y-axis
    y_label_height = (self.height - 100) // y_label_count  # Adjust the height of each y-axis label

    while not q.empty():
      process = q.get()
      proces_rectangle = Rectangle(x = prev_end, y = 50 + counter * y_label_height,width= quantum,height=HEIGHT, color = (0,255,0), id = process.id, nature = "process")

      quantum_rectangle = Rectangle(x = prev_end + quantum, y = 50 + counter * y_label_height, width= overload, height=HEIGHT, color = (255,0,0),id = "", nature = "quantum")

      rects.append(proces_rectangle)
      rects.append(quantum_rectangle)
      prev_end += overload + quantum

      process.duration -= quantum
      if process.duration > 0:
        q.put(process)

      counter = (counter + 1) % y_label_count
    return rects
    
  def scheduling_EDF(self, quantum = 20,overload = 10):
    q = queue.PriorityQueue()
    for process in self.processes:
      q.put(process)
    

    y_label_count = len(self.processes)  # Number of labels on the y-axis
    y_label_height = (self.height - 100) // y_label_count  # Adjust the height of each y-axis label
    prev_end = 50
    counter = 0
    rects = []
    while not q.empty():
      #checar estouro de deadline
      process = q.get()
      proces_rectangle = Rectangle(x = prev_end, y = 50 + counter * y_label_height,width= quantum,height=HEIGHT, color = (0,255,0), id = process.id, nature = "process")

      quantum_rectangle = Rectangle(x = prev_end + quantum, y = 50 + counter * y_label_height, width= overload, height=HEIGHT, color = (255,0,0),id = "", nature = "quantum")

      rects.append(proces_rectangle)
      rects.append(quantum_rectangle)
      prev_end += overload + quantum

      process.duration -= quantum
      if process.duration > 0:
        q.put(process)

      counter = (counter + 1) % y_label_count
   
    return rects


  def on_draw(self):
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




menu = MyWindow(1366,768)

pyglet.app.run()