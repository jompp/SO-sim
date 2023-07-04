import pyglet

class Grid:
  def __init__(self, memory):
    self.square_size = 50
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
  
  def draw(self):

    label = pyglet.text.Label(
        self.label_text,
        font_name='Arial',
        font_size=24,
        x=self.grid_x + self.grid_width//2,  # Center the label horizontally
        y=self.grid_y + self.grid_height + 50,
        anchor_x='center'
    )
    label.draw()
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


  # the bigger label stands for the process, and the smaller stands for the address
  def draw_process_pages(self,pages):
    row,col = 4,0

    for page in pages:
      font_size = int(self.square_size * 0.4)
      square_x = self.grid_x + col * self.square_size
      square_y = self.grid_y + row * self.square_size

      border_x = square_x - self.border_size
      border_y = square_y - self.border_size

      border_width = self.square_size + 2 * self.border_size
      border_height = self.square_size + 2 * self.border_size
      number = page[0]
      label = pyglet.text.Label(
          str(number),
          font_name='Arial',
          font_size=font_size,
          x=square_x + self.square_size // 2,
          y=square_y + self.square_size // 2,
          anchor_x='center',
          anchor_y='center',
          color=(0, 0, 0, 255)  # Set the text color to black
      )
      label.draw()

      # Draw number in the top left corner with decreased font size in black
      small_font_size = int(font_size * 0.6)
      small_label = pyglet.text.Label(
          str(number),
          font_name='Arial',
          font_size=small_font_size,
          x=border_x + self.border_size,
          y=border_y + border_height - self.border_size,
          anchor_x='left',
          anchor_y='top',
          color=(0, 0, 0, 255)  # Set the text color to black
      )
      small_label.draw()