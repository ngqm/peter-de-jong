import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import csv
import pandas as pd
import os


def generate_attractor(**kwargs):
    # Initialization
    x, y = 4 * np.random.rand(2) - 2
    with open('attractor.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        a, b, c, d = kwargs['a'], kwargs['b'], kwargs['c'], kwargs['d']
        for it in range(MAX_ITERS):
            writer.writerow([x, y])
            x_temp, y_temp = x, y
            x = np.sin(a * y_temp) - np.cos(b * x_temp)
            y = np.sin(c * x_temp) - np.cos(d * y_temp)


def generate_animation(new_data=True, **kwargs):
    A, B, C, D = kwargs['a'], kwargs['b'], kwargs['c'], kwargs['d']

    if new_data:
        # Clear previous data
        os.remove('attractor.csv')
        # Generate new data
        generate_attractor(a=A, b=B, c=C, d=D)

    # Collect data
    df = pd.read_csv('attractor.csv', header=None)
    x_values = df[0]
    y_values = df[1]

    ratio = (max(y_values) - min(y_values)) / (max(x_values) - min(x_values))

    # Initialize plot
    fig, ax = plt.subplots(figsize=(5, ratio * 5))
    plt.suptitle(f'Peter de Jong attractor (a = {A}, b = {B}, c = {C}, d = {D})')

    plt.xlim(min(x_values) - MARGIN, max(x_values) + MARGIN)
    plt.ylim(min(y_values) - MARGIN, max(y_values) + MARGIN)
    line, = ax.plot([], [], lw=0, marker='o', ms=.5, alpha=1)

    # Animate
    def _init():
        line.set_data([], [])
        return line,

    def _animate(i):
        line.set_data(x_values[:2000 * i], y_values[:2000 * i])
        return line,

    anim = animation.FuncAnimation(fig, _animate, init_func=_init,
                                   frames=100, blit=True)
    anim.save('attractor.gif', fps=60)
    plt.show()


def generate_image(new_data=True, **kwargs):

    plt.style.use('dark_background')

    A, B, C, D = kwargs['a'], kwargs['b'], kwargs['c'], kwargs['d']

    if new_data:
        # Clear previous data
        os.remove('attractor.csv')
        # Generate new data
        generate_attractor(a=A, b=B, c=C, d=D)

    # Collect data
    df = pd.read_csv('attractor.csv', header=None)
    x_values = df[0]
    y_values = df[1]

    ratio = (max(y_values) - min(y_values)) / (max(x_values) - min(x_values))

    # Initialize plot
    fig, axs = plt.subplots(1, 5, figsize=(20, ratio * 4))
    plt.suptitle(f'Peter de Jong attractor (a = {A}, b = {B}, c = {C}, d = {D})')

    # Plot 2d histograms
    for i in range(5):
        axs[i].hist2d(x_values, y_values, bins=100 * (i + 1),
                      cmin=1, cmap='jet')
        axs[i].set_xlim(min(x_values) - MARGIN, max(x_values) + MARGIN)
        axs[i].set_ylim(min(y_values) - MARGIN, max(y_values) + MARGIN)
        axs[i].set_title(f'bins = {100 * (i + 1)}')
    plt.savefig('attractor.jpg')
    plt.show()


# -------------------------------------------------------------------------------

# Constants
MAX_ITERS = int(2e6)
MARGIN = 0.1

# animation style
plt.style.use('seaborn')

# DE JONG
A = 1.4
B = 2.3
C = 2.4
D = -2.1
# generate_animation(new_data=False, a=A, b=B, c=C, d=D)
generate_image(new_data=True, a=A, b=B, c=C, d=D)