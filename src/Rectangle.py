import pyglet

class Rectangle(pyglet.shapes.Rectangle):
  def __init__(self, x, y, width, height,id,nature, desired_width,color=..., batch=None, group=None):
    super().__init__(x, y, width, height, color, batch, group)
    self.id = id
    self.nature = nature
    self.desired_width = desired_width