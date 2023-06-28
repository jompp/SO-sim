import pyglet

class AnimationWindow(pyglet.window.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.batch = pyglet.graphics.Batch()
        self.rect = pyglet.shapes.Rectangle(x=50, y=50, width=0, height=100, color=(0, 255, 0), batch=self.batch)

    def update(self, dt):
        if self.rect.width < 200:
            self.rect.width += 1

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def start_animation(self):
        pyglet.clock.schedule_interval(self.update, 1/60)  # Update the animation 60 times per second
        pyglet.app.run()

# Usage example
window = AnimationWindow(800, 600)
window.start_animation()
