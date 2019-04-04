

from __future__ import print_function
from numpy import random
from matplotlib.widgets import RectangleSelector
import numpy as np
import matplotlib.pyplot as plt

class run():
    def __init__(self):
      fig, current_ax = plt.subplots()
      yvec = []
      for i in range(200):
          yy = 25 + 3*random.randn()
          yvec.append(yy)
          plt.plot(yvec, 'o')

      self.RS = RectangleSelector(current_ax, self.line_select_callback,
                                             drawtype='box', useblit=True,
                                             button=[1, 3],
                                             minspanx=5, minspany=5,
                                             spancoords='pixels',
                                             interactive=True)
      plt.connect('key_press_event', self.toggle_selector)
      plt.show()

    def line_select_callback(self, eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))

    def toggle_selector(self, event):
        print(' Key pressed.')
        if event.key in ['Q', 'q'] and self.RS.active:
            print(' RectangleSelector deactivated.')
            self.RS.set_active(False)
        if event.key in ['A', 'a'] and not self.RS.active:
            print(' RectangleSelector activated.')
            self.RS.set_active(True)

if __name__ == '__main__':
    run()


