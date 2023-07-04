import pyglet
from Grid import Grid

class MemoryWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=1366, height=768)
        self.RAM = Grid(memory="RAM")
        print(self.RAM.label_text)
        self.DISK = Grid(memory="Disk")
        

    def on_draw(self):
        # Set the background color to blue
        pyglet.gl.glClearColor(0, 0, 1, 1)
        self.clear()
        self.RAM.draw()
        self.DISK.draw()



m = MemoryWindow()

pyglet.app.run()