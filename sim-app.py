import pyglet

class AnimationWindow(pyglet.window.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.batch = pyglet.graphics.Batch()
        self.rectangles = [
            pyglet.shapes.Rectangle(x=50 + i*100, y=50 + i*100, width=0, height=100, color=(0, 255, 0), batch=self.batch)
            for i in range(4)
        ]
        self.current_index = 0
        self.speed = 2  # Speed of the animation

    def update(self, dt):
        rect = self.rectangles[self.current_index]
        if rect.width < 200:
            rect.width += self.speed
        else:
            self.current_index += 1
            if self.current_index >= len(self.rectangles):
                pyglet.clock.unschedule(self.update)  # Stop the animation if all rectangles are drawn

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def start_animation(self):
        pyglet.clock.schedule_interval(self.update, 1/60)  # Update the animation 60 times per second
        pyglet.app.run()

# Usage example
window = AnimationWindow(800, 600)
window.start_animation()
