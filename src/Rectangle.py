import pyglet

class Rectangle(pyglet.shapes.Rectangle):
  def __init__(self, x, y, width, height,id,nature, desired_width,color=..., batch=None, group=None):
    super().__init__(x, y, width, height, color, batch, group)
    self.id = id
    self.nature = nature
    self.desired_width = desired_width

  def update(self,dt):
    if self.width < self.desired_width:
      self.width += 0.5
    else:
      pyglet.clock.unschedule(self.update)  # Stop the animation if all rectangles are drawn