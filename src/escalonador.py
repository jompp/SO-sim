import pyglet
import queue
from src.process import Process
window = pyglet.window.Window(width = 1195,height = 640)
HEIGHT = 100

processes = []
# for i in range(1,4):
#     id = "P" + str(i)
#     duration = i * 100
#     arrival_time = 0
    
#     processes.append(Process(id,duration,arrival_time))


processes = [Process("P1",100,0,5),Process("P2",150,0,3),Process("P3",50,0,6)]
wallpaper = pyglet.image.load("coordenadas.png")

wallpaper = pyglet.sprite.Sprite(wallpaper)

def draw_image(rects):
    @window.event
    def on_draw():
        window.clear()
        wallpaper.draw()
        for rect in rects:
            rect.draw()

def scheduling_FIFO(processes):
 

    prev_end = 0
    counter = 0
    rects = []
    for process in processes:
        
        rectangle = pyglet.shapes.Rectangle(x = prev_end, y = 100*counter,width= process.duration,height=HEIGHT, color = (0,255,0))

        rects.append(rectangle)
        prev_end += process.duration
        counter += 1


    draw_image(rects)


def scheduling_SJF(processes):
    def get_durations(process):
        return process.duration
    
    processes.sort(key = get_durations)
    scheduling_FIFO(processes)
    


def scheduling_Round_Robin(processes,quantum = 20):
    prev_end = 0
    counter = 0

    rects = []
    q = queue.Queue()
    for process in processes:
        q.put(process)
    

    dict = {
        "P1" : 85,
        "P2" : 170,
        "P3" : 255
    }
    while not q.empty():
        process = q.get()
        proces_rectangle = pyglet.shapes.Rectangle(x = prev_end, y = dict[process.id],width= process.duration,height=HEIGHT, color = (0,255,0))

        quantum_rectangle = pyglet.shapes.Rectangle(x = prev_end + process.duration, y = dict[process.id], width= quantum, height=HEIGHT, color = (255,0,0))

        rects.append(proces_rectangle)
        rects.append(quantum_rectangle)
        prev_end += process.duration + quantum

        process.duration -= quantum
        if process.duration > 0:
            q.put(process)
        
    draw_image(rects)

def scheduling_EDF(processes, quantum = 20):
    q = queue.PriorityQueue()
    for process in processes:
        q.put(process)
    
    
    dict = {
        "P1" : 0,
        "P2" : 100,
        "P3" : 200
    }

    prev_end = 0
    rects = []
    while not q.empty():

        #checar se teve estouro de deadline
        process = q.get()
        
        proces_rectangle = pyglet.shapes.Rectangle(x = prev_end, y = dict[process.id],width= process.duration,height=HEIGHT, color = (0,255,0))

        quantum_rectangle = pyglet.shapes.Rectangle(x = prev_end + process.duration, y = dict[process.id], width= quantum, height=HEIGHT, color = (255,0,0))

        rects.append(proces_rectangle)
        rects.append(quantum_rectangle)
        prev_end += process.duration + quantum

        process.duration -= quantum
        if process.duration > 0:
            q.put(process)

    draw_image(rects)

# scheduling_SJF(processes)
# scheduling_Round_Robin(processes)
scheduling_FIFO(processes)

# scheduling_EDF(processes)
pyglet.app.run()