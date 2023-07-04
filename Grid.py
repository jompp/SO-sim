import pyglet

class Grid:
  def __init__(self, memory):
    self.square_size = 50

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
        border_size = 2
        border_x = square_x - border_size
        border_y = square_y - border_size
        border_width = self.square_size + 2 * border_size
        border_height = self.square_size + 2 * border_size

        # Draw the border
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                              ('v2f', (border_x, border_y,
                                        border_x + border_width, border_y,
                                        border_x + border_width, border_y + border_height,
                                        border_x, border_y + border_height)),
                              ('c3B', border_color * 4))

        # Draw the square
        square.draw()