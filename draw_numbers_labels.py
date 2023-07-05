import pyglet

# Window dimensions
window_width = 400
window_height = 400

# Grid dimensions
num_rows = 5
num_cols = 5

# Square dimensions
square_size = min(window_width, window_height) // max(num_rows, num_cols)

# Create a window
window = pyglet.window.Window(width=window_width, height=window_height)

@window.event
def on_draw():
    # Set the background color to blue
    pyglet.gl.glClearColor(0, 0, 1, 1)
    window.clear()

    for row in range(num_rows):
        for col in range(num_cols):
            # Calculate the position of each square in the grid
            square_x = col * square_size
            square_y = row * square_size

            # Set the border color to black
            border_color = (0, 0, 0)

            # Draw the border of the square
            border_size = 2
            border_x = square_x - border_size
            border_y = square_y - border_size
            border_width = square_size + 2 * border_size
            border_height = square_size + 2 * border_size

            # Draw the border
            pyglet.shapes.Rectangle(
                x=border_x, y=border_y, width=border_width, height=border_height, color=border_color
            ).draw()

            # Draw the square
            pyglet.shapes.Rectangle(
                x=square_x, y=square_y, width=square_size, height=square_size, color=(255, 255, 255)
            ).draw()

            # Calculate the font size based on the square size
            font_size = int(square_size * 0.4)

            # Calculate the number for the square
            number = row * num_cols + col

            # Draw the number in the center of the square in black
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

pyglet.app.run()
