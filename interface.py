import sys
import math
import time

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('qt5agg')
from matplotlib.widgets import Button, RadioButtons, Slider


class GUIInterface:
    def __init__(self):
        # based on the answer https://stackoverflow.com/a/43382060/3350732
        # of user buvinj https://stackoverflow.com/users/3220983/buvinj
        # from https://stackoverflow.com/questions/17280637/tkinter-messagebox-without-window
        
        # self.root will store the root of tKinter which is used for message boxes,
        # but we only use matplotlib for the main GUI window
        
        # GUI INIT
        self.waiting_time = 1   # initially the waiting time between plots is 1s
        
        self.fig = plt.figure(figsize=(10, 8), dpi=80)
        self.fig.canvas.set_window_title('OPTIMAL DEGREE-THREE SPANNERS OF THE SQUARE LATTICE')
        
        def handle_close(evt):
            print('Execution terminated')
            plt.close('all')
            sys.exit()
        
        self.fig.canvas.mpl_connect('close_event', handle_close)
        
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.__init_axes()

        self.fig.subplots_adjust(left=0.2, bottom=0.2)
        
        widget_color = 'palegoldenrod'
        
        self.progress_slider_ax = self.fig.add_axes([0.15, 0.08, 0.75, 0.04], facecolor=widget_color)
        self.progress_slider = Slider(self.progress_slider_ax, 'Progress', 0, 100, valinit=0, dragging=False)
        self.progress_slider.set_active(False)    

        self.in_pause = False

        self.pause_button_ax = self.fig.add_axes([0.8, 0.01, 0.1, 0.04])
        self.pause_button = Button(self.pause_button_ax, 'Pause', color=widget_color, hovercolor='lightgray')
        
        self.pause_button.resume_label = self.pause_button_ax.text(0.5, 0.5, 'Resume', verticalalignment = 'center', horizontalalignment = 'center')
        self.pause_button.resume_label.set_visible(False)
        
        def pause_button_callback(mouse_event):
            if self.in_pause:
                self.in_pause = False
                self.pause_button.label.set_visible(True)
                self.pause_button.resume_label.set_visible(False)
            else:
                self.in_pause = True
                self.pause_button.label.set_visible(False)
                self.pause_button.resume_label.set_visible(True)
        self.pause_button.on_clicked(pause_button_callback)

        self.waiting_time_radios_ax = self.fig.add_axes([0.025, 0.5, 0.15, 0.15], facecolor=widget_color)
        self.waiting_time_radios = RadioButtons(self.waiting_time_radios_ax, ('plotting time', '0.3s', '1s', '3s'), active=1)
        def waiting_time_callback(label):
            if label == 'plotting time':
                self.waiting_time = 0.001
            else:
                self.waiting_time = float(label[:-1])
            self.fig.canvas.draw_idle()
        self.waiting_time_radios.on_clicked(waiting_time_callback)

        self.fig.canvas.draw_idle()
        plt.pause(self.waiting_time)
        

    def notify_start(self, edges, forbidden_edges, to_prove):
        self.current_tot = to_prove.tot
        self.progress_slider.set_val(0)
        self.is_uv_constraint = (to_prove.u is not None and to_prove.v is not None)
        self.shortcut = None
        self.pattern = None
        self.unique_path = None
        self.impossible_to_join = None

        print('We now consider the proof of', to_prove.name)
        print('Known lemmas so far:', str([lemma.name for lemma in to_prove.known_lemmas]))
    
    def notify_end(self, to_prove):
        print('Finished the proof of', to_prove.name)

    def notify_finished(self):
        print('The proof is complete!')

    def notify_shortcut(self, edges, forbidden_edges, shortcut):
        self.shortcut = shortcut
        self.__visualize(edges, forbidden_edges)
        self.shortcut = None

    def notify_pattern(self, edges, forbidden_edges, pattern):
        self.pattern = pattern
        self.__visualize(edges, forbidden_edges)
        self.pattern = None

    def notify_unique_path(self, edges, forbidden_edges, unique_path):
        self.unique_path = unique_path
        self.__visualize(edges, forbidden_edges)
        self.unique_path = None

    def notify_impossible_to_join(self, edges, forbidden_edges, p, q):
        self.impossible_to_join = (p, q)
        self.__visualize(edges, forbidden_edges)
        self.impossible_to_join = None

    def notify_branch(self, edges, forbidden_edges, tot):
        self.__visualize(edges, forbidden_edges)
        self.progress_slider.set_val(100*tot/self.current_tot)
    
    
    def __curly_path(self, a, b, col):
        # modified from the answer https://stackoverflow.com/a/50918519/3350732
        # of user hayk-hakobyan https://stackoverflow.com/users/4888158/hayk-hakobyan
        # from https://stackoverflow.com/questions/45365158/matplotlib-wavy-arrow
        xa, ya = a
        xb, yb = b
        dist = np.hypot(xb - xa, yb - ya)
        theta = np.arctan2(yb - ya, xb - xa)

        n = 3 * round(dist)
        x = np.linspace(0, dist, 200)
        y = 0.2 * np.sin(2*np.pi * x * n / dist)
        for i in range(200):
            old_x, old_y = x[i], y[i]
            x[i] = np.cos(theta)*old_x - np.sin(theta)*old_y
            y[i] = np.sin(theta)*old_x + np.cos(theta)*old_y
        
        self.ax.plot(x + xa, y + ya, linewidth=3, color=col)


    def __init_axes(self):
        x_ticks = range(-5, 7)
        y_ticks = range(-5, 7)
        self.ax.set_xticks(x_ticks)
        self.ax.set_yticks(y_ticks)
        self.ax.set_xlim([-5, 6])
        self.ax.set_ylim([-5, 6])
        self.ax.grid(which='both')


    def __visualize(self, edges, forbidden_edges):
        while self.in_pause:
            self.fig.canvas.start_event_loop(0.01)
        
        self.ax.cla()
        self.__init_axes()
        
        for seg in edges:
            a, b = seg
            xa, ya = a
            xb, yb = b
            self.ax.plot((xa, xb), (ya, yb), color='blue')
        
        for seg in forbidden_edges:
            a, b = seg
            xa, ya = a
            xb, yb = b
            self.ax.plot((xa, xb), (ya, yb), color='lightsalmon')
        
        if self.shortcut is not None:
            ls_x = []
            ls_y = []
            for pt in self.shortcut:
                x, y = pt
                ls_x.append(x)
                ls_y.append(y)
            
            len_shortcut = len(self.shortcut)
            for i in range(len_shortcut - 1):
                a, b = self.shortcut[i], self.shortcut[i+1]
                
                if (a, b) in edges:
                    xa, ya = a
                    xb, yb = b
                    self.ax.plot((xa, xb), (ya, yb), linewidth=4, linestyle='--', color='magenta')
                else:
                    self.__curly_path(a, b, 'magenta')
        
        if self.unique_path is not None:
            ls_x = []
            ls_y = []
            for pt in self.unique_path:
                x, y = pt
                ls_x.append(x)
                ls_y.append(y)
            self.ax.plot(ls_x, ls_y, linestyle='--', linewidth=4, color='limegreen')
        
        if self.pattern is not None:
            for seg in self.pattern:
                a, b = seg
                xa, ya = a
                xb, yb = b
                self.ax.plot((xa, xb), (ya, yb), linewidth=5, color='darkviolet')
        
        if self.impossible_to_join is not None:
            a, b = self.impossible_to_join
            self.__curly_path(a, b, 'red')
        
        if self.is_uv_constraint:
            self.ax.plot([0], [0], marker='o', markersize=8, color='magenta')
            self.ax.plot([1], [2], marker='o', markersize=8, color='magenta')
        
        self.fig.canvas.draw_idle()
        self.fig.canvas.start_event_loop(self.waiting_time)

     
class TextInterface:
    def __init__(self):
        self.cp_expand = 0
        self.current_tot = 0

    def notify_start(self, edges, forbidden_edges, to_prove):
        self.cp_expand = 0
        self.current_tot = to_prove.tot

        print('We now consider the proof of', to_prove.name)
        print('Known lemmas so far:', str([lemma.name for lemma in to_prove.known_lemmas]))
        
        input('Press any key to continue')

    def notify_end(self, to_prove):
        print('Finished the proof of', to_prove.name)

    def notify_finished(self):
        print('The proof is complete!')

    def notify_shortcut(self, edges, forbidden_edges, shortcut):
        print('SHORTCUT:', shortcut)

    def notify_pattern(self, edges, forbidden_edges, pattern):
        print('PATTERN:', pattern)

    def notify_unique_path(self, edges, forbidden_edges, unique_path):
        print('UNIQUE PATH:', unique_path)

    def notify_impossible_to_join(self, edges, forbidden_edges, p, q):
        print('IMPOSSIBLE TO JOIN', p, 'AND', q)

    def notify_branch(self, edges, forbidden_edges, tot):
        self.cp_expand += 1
        print('PROGRESS:', str(self.cp_expand) + '/' + str(self.current_tot))
