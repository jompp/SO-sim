import pyglet

# Window dimensions
window_width = 400
window_height = 400

# Create a window
window = pyglet.window.Window(width=window_width, height=window_height)

@window.event
def on_draw():
    # Set the background color to blue
    pyglet.gl.glClearColor(0, 0, 1, 1)
    window.clear()

    # Draw the rectangle
    square_size = 55
    square_x = (window_width - square_size) // 2
    square_y = (window_height - square_size) // 2

    # Set the border color to black
    border_color = (0, 0, 0)

    # Draw the border of the rectangle
    border_size = 5
    border_x = square_x - border_size
    border_y = square_y - border_size
    border_width = square_size + 2 * border_size
    border_height = square_size + 2 * border_size

    # Draw the border
    pyglet.shapes.Rectangle(
        x=border_x, y=border_y, width=border_width, height=border_height, color=border_color
    ).draw()

    # Draw the rectangle
    pyglet.shapes.Rectangle(
        x=square_x, y=square_y, width=square_size, height=square_size, color=(255, 255, 255)
    ).draw()

    # Calculate the font size based on the square size
    font_size = int(square_size * 0.4)

    # Draw number in the center of the square in black
    number = 42
    label = pyglet.text.Label(
        str(number),
        font_name='Arial',
        font_size=font_size,
        x=square_x + square_size // 2,
        y=square_y + square_size // 2,
        anchor_x='center',
        anchor_y='center',
        color=(0, 0, 0, 255)  # Set the text color to black
    )
    label.draw()

    # Draw number in the top left corner with decreased font size in black
    small_font_size = int(font_size * 0.6)
    small_label = pyglet.text.Label(
        str(number),
        font_name='Arial',
        font_size=small_font_size,
        x=border_x + border_size,
        y=border_y + border_height - border_size,
        anchor_x='left',
        anchor_y='top',
        color=(0, 0, 0, 255)  # Set the text color to black
    )
    small_label.draw()

pyglet.app.run()
