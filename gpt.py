import pyglet

class MyAnimatedObject:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity

    def update(self, dt):
        # Update the position of the animated object
        self.x += self.velocity * dt

class MyWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=800, height=600)

        # Create an animated object
        self.animated_object = MyAnimatedObject(x=100, y=300, velocity=100)

        # Create a stationary rectangle
        self.stationary_object = pyglet.shapes.Rectangle(x=500, y=300, width=100, height=100, color=(255, 0, 0))

        # Schedule the update method of the animated object
        pyglet.clock.schedule_interval(self.animated_object.update, 1/60)

    def on_draw(self):
        self.clear()
        self.stationary_object.draw()
        pyglet.shapes.Rectangle(x=self.animated_object.x, y=self.animated_object.y, width=100, height=100, color=(0, 255, 0)).draw()

    def update(self, dt):
        # Update any other logic or properties here if needed
        pass

window = MyWindow()
pyglet.app.run()
