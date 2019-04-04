from region_of_interest import *
from matplotlib.widgets import RectangleSelector

class ControlROI():
    def __init__(self, fig, imdis, vol_tran, vol_fron, vol_sagi, ax_tran, ax_fron, ax_sagi):
        self.fig = fig
        self.imdis = imdis

        self.vol_tran = vol_tran
        self.vol_fron = vol_fron
        self.vol_sagi = vol_sagi

        self.ax_tran = ax_tran
        self.ax_fron = ax_fron
        self.ax_sagi = ax_sagi

        self.scroll_tran = None
        self.scroll_fron = None
        self.scroll_sagi = None

        self.fig.canvas.mpl_connect('axes_enter_event', self.fig_enter_event)
        self.fig.canvas.mpl_connect('axes_leave_event', self.fig_leave_event)

    def fig_enter_event(self, event):
        if self.ax_tran.in_axes(event):
            self.scroll_tran = self.fig.canvas.mpl_connect('scroll_event', self.transverse_scroll)

        elif self.ax_fron.in_axes(event):
            self.scroll_fron = self.fig.canvas.mpl_connect('scroll_event', self.frontal_scroll)

        elif self.ax_sagi.in_axes(event):
            self.scroll_sagi = self.fig.canvas.mpl_connect('scroll_event', self.sagittal_scroll)

    def fig_leave_event(self, event):
        self.fig.canvas.mpl_disconnect(self.scroll_tran)
        self.fig.canvas.mpl_disconnect(self.scroll_tran)
        self.fig.canvas.mpl_disconnect(self.scroll_sagi)

    def transverse_scroll(self, event):
        if event.button == 'down':
            self.ax_tran.index -= 1
        if event.button == 'up':
            self.ax_tran.index += 1
        self.imdis.update_transverse_display(self.ax_tran.index)
        self.fig.canvas.draw_idle()

    def frontal_scroll(self, event):
        if event.button == 'down':
            self.ax_fron.index -= 1
        if event.button == 'up':
            self.ax_fron.index += 1
        self.imdis.update_frontal_display(self.ax_fron.index)
        self.fig.canvas.draw_idle()

    def sagittal_scroll(self, event):
        if event.button == 'down':
            self.ax_sagi.index -= 1
        if event.button == 'up':
            self.ax_sagi.index += 1
        self.imdis.update_sagittal_display(self.ax_sagi.index)
        self.fig.canvas.draw_idle()
