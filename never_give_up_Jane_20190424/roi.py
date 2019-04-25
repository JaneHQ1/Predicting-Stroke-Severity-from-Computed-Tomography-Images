import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button

class ROI(object):
    def __init__(self, fig, ax):
        # self.fig = fig
        # self.ax = plt.gca()
        self.ax = ax
        self.rect = Rectangle((0, 0), 1, 1, facecolor='None', edgecolor='red')
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.is_pressed = False
        self.ax.add_patch(self.rect)

        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        self.is_pressed = True
        print('press')
        self.x0 = event.xdata
        self.y0 = event.ydata

    def on_motion(self, event):
        if self.is_pressed == True:
            self.x1 = event.xdata
            self.y1 = event.ydata
            self.rect.set_width(self.x1 - self.x0)
            self.rect.set_height(self.y1 - self.y0)
            self.rect.set_xy((self.x0, self.y0))
            self.rect.set_linestyle('dashed')
            # self.fig.canvas.draw()
            self.ax.figure.canvas.draw()

    def on_release(self, event):
        self.is_pressed = False
        print('release')
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.rect.set_linestyle('solid')
        # self.fig.canvas.draw()
        self.ax.figure.canvas.draw()
        print(self.x0, self.x1, self.y0, self.y1)
        return [self.x0, self.x1, self.y0, self.y1]

