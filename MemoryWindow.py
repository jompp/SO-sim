import pyglet
from Grid import Grid
from Process import Process
class MemoryWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=1366, height=768)
        self.RAM = Grid(memory="RAM")
        self.DISK = Grid(memory="Disk")
        self.processes = [Process(1,4,0,0,2),Process(2,2,2,0,5),Process(3,1,3,0,5)]
    
    def update(self,dt):
        pass
    def on_draw(self):
        # Set the background color to blue
        pyglet.gl.glClearColor(0, 0, 1, 1)
        self.clear()
        self.RAM.draw_grid()
        # self.RAM.draw_processes_pages()
        
        for process in self.processes:
            self.RAM.draw_process_pages(process)
        self.DISK.draw_grid()
        
    

m = MemoryWindow()

pyglet.app.run()