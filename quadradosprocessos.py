import pyglet

class Process:
    def __init__(self, id, duration_time, arrival_time, deadline):
        self.id = id
        self.duration_time = duration_time
        self.arrival_time = arrival_time
        self.deadline = deadline

class ProcessSquare:
    def __init__(self, x, y, size, process):
        self.x = x
        self.y = y
        self.size = size
        self.process = process

    def draw(self):
        square = pyglet.shapes.BorderedRectangle(self.x, self.y, self.size, self.size, color=(128, 0, 0), border_color=(255, 255, 255))
        square.draw()

        box_size = self.size // 4 - 10
        box_x = self.x + 60
        box_y = self.y + 5

        for i, key in enumerate(["duration", "arrival_time", "deadline", "id"]):
            box = pyglet.shapes.Rectangle(box_x + 60, box_y + i * (box_size + 10), box_size + 30, box_size, color=(255, 255, 255))
            box.draw()

            key_label = pyglet.text.Label(key, font_size=12,
                                          x=box_x -50, y=box_y + i * (box_size + 10) + box_size/2 + 10,
                                          anchor_x='left', anchor_y='top', color=(255, 255, 255, 255))
            key_label.draw()

            value_label = pyglet.text.Label(str(getattr(self.process, key)), font_size=12,
                                            x=box_x + box_size + 110 / 2, y=box_y + i * (box_size + 10) + box_size / 2,
                                            anchor_x='center', anchor_y='center', color=(0, 0, 0, 255))
            value_label.draw()