import pyglet
from Process import Process
window = pyglet.window.Window()
HEIGHT = 100

processes = []
for i in range(1,4):
    id = "P" + str(i)
    duration = i * 100
    arrival_time = 0
    
    processes.append(Process(id,duration,arrival_time))

def scheduling_FIFO(processes):

    prev_end = 0
    counter = 0

    rects = []
    for process in processes:
        
        rectangle = pyglet.shapes.Rectangle(x = prev_end, y = 100*counter,width= process.duration,height=HEIGHT, color = (0,255,0))

        rects.append(rectangle)
        prev_end += process.duration
        counter += 1


    for p in processes:
        print(p.id)
    @window.event
    def on_draw():
        window.clear()
        
        for rect in rects:
            rect.draw()


def scheduling_SJF(processes):
    def get_durations(process):
        return process.duration
    
    processes.sort(key = get_durations)
    scheduling_FIFO(processes)



scheduling_FIFO(processes)
pyglet.app.run()
