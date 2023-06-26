from pathlib import Path
import pyglet
from src.menu import MeuMenu

menu = MeuMenu(1366,768)
icon = pyglet.image.load(Path('sprites/blackjack_icon.png'))
menu.set_icon(icon)
pyglet.app.run()