import pyglet

window = pyglet.window.Window(800, 600)

# Define the screens
screen1_label = pyglet.text.Label("Screen 1",
                                  font_size=36,
                                  x=window.width // 2,
                                  y=window.height // 2,
                                  anchor_x='center',
                                  anchor_y='center')

screen2_label = pyglet.text.Label("Screen 2",
                                  font_size=36,
                                  x=window.width // 2,
                                  y=window.height // 2,
                                  anchor_x='center',
                                  anchor_y='center')

current_screen = screen1_label

# Define the button
button_radius = 50
button_x = window.width // 2
button_y = window.height - button_radius - 20

button = pyglet.shapes.Circle(button_x, button_y, button_radius, color=(255, 0, 0))

@window.event
def on_draw():
    window.clear()
    current_screen.draw()
    button.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        if button.collide_point(x, y):
            toggle_screen()

def toggle_screen():
    global current_screen
    if current_screen == screen1_label:
        current_screen = screen2_label
    else:
        current_screen = screen1_label

pyglet.app.run()
