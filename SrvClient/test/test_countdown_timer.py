#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import re
import argparse
import random
import tkinter as tk

class App():
  def __init__(self):
    self.window_size = 150
    self.fps = 10
    self.font_size = 23
    self.option = self.parse_args()
    self.time = self.get_timesec()
    self.period = self.time
    self.root = self.set_root()
    self.canvas = self.set_canvas()
    self.label = self.set_label()
    self.progress = self.init_progress()
    self.update()
    self.run()

  def parse_args(self):
    parser = argparse.ArgumentParser(description="Show simple countdown timer on desktop.")
    parser.add_argument("period", action="store", type=str, help="Set period for your timer.")
    parser.add_argument("-t", dest="title", action="store", default="Timer", help="Set title for your timer.")
    parser.add_argument("-n", dest="notify", action="store_false", default=True, help="Disable notification.")
    return parser.parse_args()

  def get_timesec(self):
    if re.search("\A(?:\d+h)?(?:\d+m)?(?:\d+s)?$", self.option.period) is None:
      #print "Incorrect format of period:", self.option.period
      print("Incorrect format of period: {}".format(self.option.period) )
      print("Set period like 10m30s")
      sys.exit()
    time = 0
    if re.search("\d+h", self.option.period) is not None:
      time += int(re.search("\d+h", self.option.period).group(0)[:-1]) * 3600
    if re.search("\d+m", self.option.period) is not None:
      time += int(re.search("\d+m", self.option.period).group(0)[:-1]) * 60
    if re.search("\d+s", self.option.period) is not None:
      time += int(re.search("\d+s", self.option.period).group(0)[:-1])
    if time > 9 * 3600 + 59 * 60 + 59:
      print("Too long period.")
      sys.exit()
    return time

  def set_root(self):
    root = tk.Tk()
    root.resizable(0,0)
    window_size = self.window_size
    colors = ["#f44336", "#E91E63", "#9C27B0", "#673AB7", "#3F51B5", "#2196F3", "#03A9F4", "#00BCD4", "#009688", "#4CAF50", "#8BC34A", "#CDDC39", "#FFEB3B", "#FFC107", "#FF9800", "#FF5722", "#795548", "#9E9E9E", "#607D8B"]
    root.title(self.option.title)
    root.geometry("%dx%d+%d+%d" % (window_size, window_size, root.winfo_screenwidth() - window_size, 0))
    root.configure(bg=random.choice(colors))
    root.attributes("-alpha", 0.5)
    root.attributes("-topmost", True)
    return root

  def set_label(self):
    window_size = self.window_size
    label = self.canvas.create_text((window_size / 2, window_size / 2), text="")
    self.canvas.itemconfig(label, font=("Menlo-Regular", self.font_size))
    return label

  def set_canvas(self):
    window_size = self.window_size
    canvas = tk.Canvas(self.root, width=window_size, height=window_size, highlightthickness=0)
    canvas.grid()
    return canvas

  def format_time(self, timesec):
    m, s = divmod(timesec, 60)
    h, m = divmod(m, 60)
    if h == 0:
      if m == 0:
        return "%02ds" % (s)
      else:
        return "%02dm%02ds" % (m, s)
    else:
      return "%dh%02dm%02ds" % (h, m, s)

  def init_progress(self):
    color = self.root["bg"]
    window_size = self.window_size
    progress = self.canvas.create_arc(window_size * 0.1, window_size * 0.1, window_size * 0.9, window_size * 0.9, style="arc", width="%d" % (window_size / 15), outline=color, start=90, extent=360)
    return progress

  def update(self):
    window_size = self.window_size
    self.canvas.itemconfig(self.label, text=self.format_time(self.time))
    extent = 360.0 * self.time / self.period
    self.canvas.itemconfig(self.progress, start=450-extent, extent=extent)
    self.time -= 1.0 / self.fps
    if self.time < 0:
      if self.option.notify:
        print('\a') 
      sys.exit()
    #self.root.after(1000/self.fps, self.update)
    self.root.after(int(1000/self.fps), self.update)

  def run(self):
    self.root.mainloop()

app = App()