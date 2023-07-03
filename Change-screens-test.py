import pyglet

class Screen1:
    def __init__(self):
        self.label = pyglet.text.Label("Screen 1",
                                       font_name='Arial',
                                       font_size=36,
                                       x=window.width//2, y=window.height//2,
                                       anchor_x='center', anchor_y='center')
        self.button = pyglet.text.Label("Go to Screen 2",
                                        font_name='Arial',
                                        font_size=24,
                                        x=window.width//2, y=window.height//2 - 50,
                                        anchor_x='center', anchor_y='center')

    def on_draw(self):
        window.clear()
        self.label.draw()
        self.button.draw()

    def on_button_click(self, x, y):
        if self.button.x - self.button.content_width//2 <= x <= self.button.x + self.button.content_width//2 and \
           self.button.y - self.button.content_height//2 <= y <= self.button.y + self.button.content_height//2:
            return True
        return False

class Screen2:
    def __init__(self):
        self.label = pyglet.text.Label("Screen 2",
                                       font_name='Arial',
                                       font_size=36,
                                       x=window.width//2, y=window.height//2,
                                       anchor_x='center', anchor_y='center')
        self.button = pyglet.text.Label("Go to Screen 1",
                                        font_name='Arial',
                                        font_size=24,
                                        x=window.width//2, y=window.height//2 - 50,
                                        anchor_x='center', anchor_y='center')

    def on_draw(self):
        window.clear()
        self.label.draw()
        self.button.draw()

    def on_button_click(self, x, y):
        if self.button.x - self.button.content_width//2 <= x <= self.button.x + self.button.content_width//2 and \
           self.button.y - self.button.content_height//2 <= y <= self.button.y + self.button.content_height//2:
            return True
        return False

# Create a window
window = pyglet.window.Window(width=800, height=600)

# Create instances of different screens
screen1 = Screen1()
screen2 = Screen2()

# Set the initial screen
current_screen = screen1

@window.event
def on_draw():
    current_screen.on_draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    global current_screen  # Define current_screen as a global variable
    if button == pyglet.window.mouse.LEFT:
        if current_screen.on_button_click(x, y):
            if current_screen == screen1:
                current_screen = screen2
            else:
                current_screen = screen1

pyglet.app.run()
