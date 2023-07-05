import pyglet

from Process import Process
class Grid:
  def __init__(self, memory):
    self.square_size = 50
    self.font_size = int(self.square_size * 0.4)
    self.processes = [Process(1,4,0,0,2),Process(2,2,2,0,5),Process(3,1,3,0,1)]
    self.border_size = 2
    if memory == "RAM":
      self.label_text = "RAM"
      self.num_rows = 5
      self.num_cols = 10
      self.grid_width = self.num_cols * self.square_size
      self.grid_x = (1366 - self.grid_width) // 2 + 400  # Push grid 1 to the right by 400 pixels
    
    else:
      self.label_text = "Disk"
      self.num_rows = 10
      self.num_cols = 12
      self.grid_width = self.num_cols * self.square_size
      self.grid_x = (1366 - self.grid_width) // 2 - 350
    
    self.grid_height = self.num_rows * self.square_size
    self.grid_y = (768 - self.grid_height) // 2
    self.hashTable = {}
    for row in range(self.num_rows):
      for col in range(self.num_cols):
        self.hashTable[str((row,col))] = "True"

  def draw_grid(self):

    label = pyglet.text.Label(
        self.label_text,
        font_name='Arial',
        font_size=24,
        x=self.grid_x + self.grid_width//2,  # Center the label horizontally
        y=self.grid_y + self.grid_height + 50,
        anchor_x='center'
    )
    label.draw()

    address = 0
    for row in range(self.num_rows):
      for col in range(self.num_cols):
        # Calculate the position of each square in grid 1
        square_x = self.grid_x + col * self.square_size
        square_y = self.grid_y + row * self.square_size

        square = pyglet.shapes.Rectangle(
            x=square_x,
            y=square_y,
            width=self.square_size,
            height=self.square_size,
            color=(255, 255, 255)
        )

        # Set the border color to black
        border_color = (0, 0, 0)

        # Draw the border of the square
        
        border_x = square_x - self.border_size
        border_y = square_y - self.border_size
        border_width = self.square_size + 2 * self.border_size
        border_height = self.square_size + 2 * self.border_size

        # Draw the border
        pyglet.shapes.Rectangle(
        x=border_x, y=border_y, width=border_width, height=border_height, color=border_color
        ).draw()

        # Draw the square
        square.draw()

        border_x = square_x - self.border_size
        border_y = square_y - self.border_size
        border_width = self.square_size + 2 * self.border_size
        border_height = self.square_size + 2 * self.border_size


        # Draw number in the top left corner with decreased font size in black
        small_font_size = int(self.font_size * 0.6)
        small_label = pyglet.text.Label(
            str(address),
            font_name='Arial',
            font_size=small_font_size,
            x=border_x + self.border_size,
            y=border_y + border_height - self.border_size,
            anchor_x='left',
            anchor_y='top',
            color=(0, 0, 0, 255)  # Set the text color to black
        )
        address += 1
        small_label.draw()


  def pagination_FIFO(self):
    pass

  def draw_processes_pages(self):
    self.processes.sort(key = lambda p: p.arrival_time)

    for process in self.processes:
      for page in range(process.pages):
        self.find_page_address(process.id)
      
  def find_page_address(self,process_id):
      for i in range(self.num_rows-1,-1,-1):
        for j in range(0,self.num_cols):
          
          if self.hashTable[str((i,j))] == "True":
            self.allocate_process(process_id,i,j)
            self.hashTable[str((i,j))] = "False"
            return
            
  def allocate_process(self,process_id, row, col):
    square_x = self.grid_x + col * self.square_size
    square_y = self.grid_y + row * self.square_size
    
    label = pyglet.text.Label(
        str(process_id),
        font_name='Arial',
        font_size=self.font_size,
        x=square_x + self.square_size // 2,
        y=square_y + self.square_size // 2,
        anchor_x='center',
        anchor_y='center',
        color=(0, 0, 0, 255)  # Set the text color to black
    )
    label.draw()

