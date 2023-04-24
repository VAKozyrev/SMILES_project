import matplotlib.pyplot as plt
from matplotlib.widgets import Button

fig, ax = plt.subplots()

x = range(10)
y = x

# plot the initial line in blue
line, = ax.plot(x, y, color='blue')

def on_button_click(event):
    current_color = line.get_color()
    if current_color == 'blue':
        line.set_color('green')
    else:
        line.set_color('blue')
    fig.canvas.draw_idle()

# create the button and add it to the plot
button_ax = plt.axes([0.7, 0.05, 0.2, 0.075])
button = Button(button_ax, 'Change color')
button.on_clicked(on_button_click)

plt.show()