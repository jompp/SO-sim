import pyglet

window = pyglet.window.Window()

process_num_txt = pyglet.text.Label('Numero de processos:',
                          font_name='Times New Roman',
                          font_size=25,
                          x=10, y=window.height-40)

quantum_txt = pyglet.text.Label('Quantum:',
                          font_name='Times New Roman',
                          font_size=25,
                          x=500, y=window.height-40)

process_num_ipt = ''
quantum_ipt = ''

@window.event
def on_key_press(symbol, modifiers):
    global process_num_ipt
    if symbol == pyglet.window.key.BACKSPACE:
        process_num_ipt = process_num_ipt[:-1]
    elif symbol == pyglet.window.key.ENTER:
        print('Entrada do usuário:', process_num_ipt)
        process_num_ipt = ''

@window.event
def on_draw():
    window.clear()
    process_num_txt.draw()
    quantum_txt.draw()

pyglet.app.run()