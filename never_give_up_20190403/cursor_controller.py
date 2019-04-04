
class ControlSys():
    def __init__(self, fig, imdis, vol_tran, vol_fron, vol_sagi, ax_tran, ax_fron, ax_sagi):
        self.fig =fig
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

        self.lx_tran = ax_tran.axhline(color='b', linewidth=0.8)
        self.ly_tran = ax_tran.axvline(color='b', linewidth=0.8)
        self.lx_fron = ax_fron.axhline(color='b', linewidth=0.8)
        self.ly_fron = ax_fron.axvline(color='b', linewidth=0.8)
        self.lx_sagi = ax_sagi.axhline(color='b', linewidth=0.8)
        self.ly_sagi = ax_sagi.axvline(color='b', linewidth=0.8)

        self.txt_tran = ax_tran.text(0, -10, '', color='b')
        self.txt_fron = ax_fron.text(0, -10, '', color='b')
        self.txt_sagi = ax_sagi.text(0, -10, '', color='b')

        self.fig.canvas.mpl_connect('button_press_event', self.button_press_events)

    def button_press_events(self, event):

        if self.ax_tran.in_axes(event):
            self.fig.canvas.mpl_connect('button_press_event', self.add_cursor(event, self.ax_tran))
            self.fig.canvas.mpl_connect('button_press_event', self.frontal_view(int(event.ydata)))
            self.fig.canvas.mpl_connect('button_press_event', self.sagittal_view(int(event.xdata)))
            # self.scroll_tran = self.fig.canvas.mpl_connect('scroll_event', self.transverse_scroll)
            # self.fig.canvas.mpl_disconnect(self.scroll_fron)
            # self.fig.canvas.mpl_disconnect(self.scroll_sagi)

        elif self.ax_fron.in_axes(event):
            self.fig.canvas.mpl_connect('button_press_event', self.add_cursor(event, self.ax_fron))
            self.fig.canvas.mpl_connect('button_press_event', self.transverse_view(int(event.ydata)))
            self.fig.canvas.mpl_connect('button_press_event', self.sagittal_view(int(event.xdata)))
            # self.scroll_fron = self.fig.canvas.mpl_connect('scroll_event', self.frontal_scroll)
            # self.fig.canvas.mpl_disconnect(self.scroll_tran)
            # self.fig.canvas.mpl_disconnect(self.scroll_sagi)

        elif self.ax_sagi.in_axes(event):
            self.fig.canvas.mpl_connect('button_press_event', self.add_cursor(event, self.ax_sagi))
            self.fig.canvas.mpl_connect('button_press_event', self.transverse_view(int(event.ydata)))
            self.fig.canvas.mpl_connect('button_press_event', self.frontal_view(int(event.xdata)))
            # self.scroll_sagi = self.fig.canvas.mpl_connect('scroll_event', self.sagittal_scroll)
            # self.fig.canvas.mpl_disconnect(self.scroll_tran)
            # self.fig.canvas.mpl_disconnect(self.scroll_fron)

    def transverse_view(self, index):
        self.ax_tran.index = index
        self.imdis.update_transverse_display(self.ax_tran.index)
        self.fig.canvas.draw_idle()

    def frontal_view(self, index):
        self.ax_fron.index = index
        self.imdis.update_frontal_display(self.ax_fron.index)
        self.fig.canvas.draw_idle()

    def sagittal_view(self, index):
        self.ax_sagi.index = index
        self.imdis.update_sagittal_display(self.ax_sagi.index)
        self.fig.canvas.draw_idle()

    def add_cursor(self, event, ax):
        if ax is self.ax_tran:
            x, y, z = event.xdata, event.ydata, self.ax_tran.index
            coord_tran = [x, y, z]
            coord_fron = [x, z, y]
            coord_sagi = [y, z, x]
            self.plot_cursor(coord_tran, self.lx_tran, self.ly_tran, self.txt_tran)
            self.plot_cursor(coord_fron, self.lx_fron, self.ly_fron, self.txt_fron)
            self.plot_cursor(coord_sagi, self.lx_sagi, self.ly_sagi, self.txt_sagi)

        if ax is self.ax_fron:
            x, y, z = event.xdata, event.ydata, self.ax_fron.index
            coord_fron = [x, y, z]
            coord_tran = [x, z, y]
            coord_sagi = [z, y, x]
            self.plot_cursor(coord_tran, self.lx_tran, self.ly_tran, self.txt_tran)
            self.plot_cursor(coord_fron, self.lx_fron, self.ly_fron, self.txt_fron)
            self.plot_cursor(coord_sagi, self.lx_sagi, self.ly_sagi, self.txt_sagi)

        if ax is self.ax_sagi:
            x, y, z = event.xdata, event.ydata, self.ax_sagi.index
            coord_sagi = [x, y, z]
            coord_tran = [z, x, y]
            coord_fron = [z, y, x]
            self.plot_cursor(coord_tran, self.lx_tran, self.ly_tran, self.txt_tran)
            self.plot_cursor(coord_fron, self.lx_fron, self.ly_fron, self.txt_fron)
            self.plot_cursor(coord_sagi, self.lx_sagi, self.ly_sagi, self.txt_sagi)

    def plot_cursor(self, coord, lx, ly, txt):
        x, y, z = coord[0], coord[1], coord[2]
        lx.set_ydata(y)
        ly.set_xdata(x)
        txt.set_text('x=%1d y=%1d z=%1d' % (x, y, z))
        self.fig.canvas.draw_idle()


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
