import pyglet
from Grid import Grid

class MemoryWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=1366, height=768)
        self.RAM = Grid(memory="RAM")
        self.DISK = Grid(memory="Disk")

        self.pages = [(4,2),(5,1),(1,2)]
        

    def on_draw(self):
        # Set the background color to blue
        pyglet.gl.glClearColor(0, 0, 1, 1)
        self.clear()
        self.RAM.draw_grid()
        # self.RAM.draw_processes_pages()
        self.RAM.draw_processes_pages()
        self.DISK.draw_grid()

        

m = MemoryWindow()

pyglet.app.run()