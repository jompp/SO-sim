import pyglet
from src.menu import MeuMenu
from MyWindow import MyWindow


class MainWindow(pyglet.window.Window):
  
  def __init__(self):
    self.menu = MeuMenu(1920,1080)
    self.gantt = MyWindow(1920,1080)

    self.current_screen = self.menu



  def on_mouse_press(self, x, y, button, modifiers):
    


      
pyglet.app.run()