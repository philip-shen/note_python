from concurrent import futures
import sys
import tkinter
import tkinter.scrolledtext
import os, os.path
import datetime
import glob
from PIL import Image, ImageTk

from matplotlib.backends.backend_tkagg import (
	FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation

import numpy as np
import random

import importlib

from telloedu.status import *
from telloedu.streaming import *
from telloedu.tellostart import *
from telloedu.command import *

import ugoki

def _quit():
	end()
	#root.quit()
	root.destroy()

def init_tof():
	global x_tof, y_tof
	x_tof = np.arange(-50, 0, 0.5)
	y_tof = np.zeros(100)
	line_tof.set_ydata(y_tof)
	line_tof.set_xdata(x_tof)
	return line_tof,

def animate_tof(n):
	global t_tof,x_tof,y_tof
	if get_drone_flg():
		y_tof = np.append(y_tof, get_tof())
		y_tof = np.delete(y_tof, 0)
		t_tof = t_tof + 1
		x_tof = np.append(x_tof, t_tof)
		x_tof = np.delete(x_tof, 0)
	plt_tof.set_ylim(0, 200)
	plt_tof.set_xlim(min(x_tof), max(x_tof))
	line_tof.set_ydata(y_tof)
	line_tof.set_xdata(x_tof)
	return line_tof,

def init_h():
	global x_h, y_h
	x_h = np.arange(-50, 0, 0.5)
	y_h = np.zeros(100)
	line_h.set_ydata(y_h)
	line_h.set_xdata(x_h)
	return line_h,

def animate_h(n):
	global t_h,x_h,y_h
	if get_drone_flg():
		y_h = np.append(y_h, get_height())
		y_h = np.delete(y_h, 0)
		t_h = t_h + 1
		x_h = np.append(x_h, t_h)
		x_h = np.delete(x_h, 0)
	plt_h.set_ylim(0, 200)
	plt_h.set_xlim(min(x_h), max(x_h))
	line_h.set_ydata(y_h)
	line_h.set_xdata(x_h)
	return line_h,

def init_temp():
	global x_temp, y_temp
	x_temp = np.arange(-50, 0, 0.5)
	y_temp = np.zeros(100)
	line_h.set_ydata(y_temp)
	line_h.set_xdata(x_temp)
	return line_temp,

def animate_temp(n):
	global t_temp,x_temp,y_temp
	if get_drone_flg():
		y_temp = np.append(y_temp, get_temph())
		y_temp = np.delete(y_temp, 0)
		t_temp = t_temp + 1
		x_temp = np.append(x_temp, t_temp)
		x_temp = np.delete(x_temp, 0)
	plt_temp.set_ylim(0, 100)
	plt_temp.set_xlim(min(x_temp), max(x_temp))
	line_temp.set_ydata(y_temp)
	line_temp.set_xdata(x_temp)
	return line_temp,

def init_bat():
	global x_bat, y_bat
	x_bat = np.arange(-50, 0, 0.5)
	y_bat = np.zeros(100)
	line_bat.set_ydata(y_bat)
	line_bat.set_xdata(x_bat)
	return line_bat,

def animate_bat(n):
	global t_bat,x_bat,y_bat
	if get_drone_flg():
		y_bat = np.append(y_bat, get_bat())
		y_bat = np.delete(y_bat, 0)
		t_bat = t_bat + 1
		x_bat = np.append(x_bat, t_bat)
		x_bat = np.delete(x_bat, 0)
	plt_bat.set_ylim(0, 100)
	plt_bat.set_xlim(min(x_bat), max(x_bat))
	line_bat.set_ydata(y_bat)
	line_bat.set_xdata(x_bat)
	return line_bat,

def _godrone():
	global drone_flg
	textbox1.delete('1.0','end')
	importlib.reload(ugoki)
	set_drone_flg(True)

def _droneEmergency():
	emergency()

def _thumbnail():
	qr_image_path = './img/qrcode-*.png'
	qr_files = glob.glob(qr_image_path)
	#print(qr_files)
	qr_files.sort(key = os.path.getmtime, reverse = True)
	#print(qr_files)
	if qr_files:
		qr_image = Image.open(qr_files[0])
		qr_image = qr_image.resize((184, 144))
		m1_image = ImageTk.PhotoImage(qr_image)
		dt = datetime.datetime.fromtimestamp(os.stat(qr_files[0]).st_mtime)
		'''
		python中time.strftime不支持中文，报错UnicodeEncodeError: 'locale' codec can't encode character '\u5e74' in position 2: encoding error
		
		https://www.cnblogs.com/feiquan/p/11217534.html
		'''
		#qr_image_label = tkinter.Label(canvas2, image = m1_image, text = 'QR Code 撮影日\n'+ dt.strftime(
		#	'%Y年%m月%d日 %H:%M:%S'), compound='top')
		qr_image_label = tkinter.Label(canvas2, image = m1_image, text = 'QR Code 撮影日\n'+ dt.strftime(
			'%YY%mM%dD %H:%M:%S'), compound='top')
		qr_image_label.grid(column = 1, row = 2)
		qr_image_label.image = m1_image
	pic_image_path = './img/photo-*.png'
	pic_files = glob.glob(pic_image_path)
	#print(pic_files)
	pic_files.sort(key = os.path.getmtime, reverse = True)
	#print(pic_files)
	if pic_files:
		pic_image = Image.open(pic_files[0])
		pic_image = pic_image.resize((184, 144))
		m2_image = ImageTk.PhotoImage(pic_image)
		dt = datetime.datetime.fromtimestamp(os.stat(pic_files[0]).st_mtime)
		#pic_image_label = tkinter.Label(canvas2, image = m2_image, text = 'Photo 撮影日\n'+ dt.strftime(
		#	'%Y年%m月%d日 %H:%M:%S'), compound='top')
		pic_image_label = tkinter.Label(canvas2, image = m2_image, text = 'Photo 撮影日\n'+ dt.strftime(
			'%YY%mM%dD %H:%M:%S'), compound='top')	
		pic_image_label.grid(column = 2, row = 2)
		pic_image_label.image = m2_image

def redirector(inputStr):
	textbox1.insert(tkinter.INSERT, inputStr)


if __name__ == "__main__":
	root = tkinter.Tk()
	root.wm_title("ドローン・プログラミング支援システム")

	frame1 = tkinter.Frame(root, width = 1200, height = 400, borderwidth = 4)
	frame1.pack(padx = 5, pady = 5)

	fig = Figure(figsize = (10, 7))
	fig.suptitle('Drone flight status')
	canvas = FigureCanvasTkAgg(fig, master = frame1)  # A tk.DrawingArea.

	# ToF
	t_tof = 1
	x_tof = np.arange(-50, 0, 0.5)
	y_tof = np.zeros(100)
	plt_tof = fig.add_subplot(221)
	plt_tof.set_title('ToF')
	plt_tof.set_xlabel("time[s]")
	plt_tof.set_ylabel("Height[cm]")
	line_tof, = plt_tof.plot(x_tof, y_tof)
	ani_tof = animation.FuncAnimation(fig, animate_tof, init_func = init_tof, interval = 500, blit = False)
	# Height
	t_h = 1
	x_h = np.arange(-50, 0, 0.5)
	y_h = np.zeros(100)
	plt_h = fig.add_subplot(222)
	plt_h.set_title('Height')
	plt_h.set_xlabel("time[s]")
	plt_h.set_ylabel("Height[cm]")
	line_h, = plt_h.plot(x_h, y_h)
	ani_h = animation.FuncAnimation(fig, animate_h, init_func = init_h, interval = 500, blit = False)
	# Temperature
	t_temp = 1
	x_temp = np.arange(-50, 0, 0.5)
	y_temp = np.zeros(100)
	plt_temp = fig.add_subplot(223)
	plt_temp.set_title('Temperature')
	plt_temp.set_xlabel("time[s]")
	plt_temp.set_ylabel("Temperature[c]")
	line_temp, = plt_temp.plot(x_temp, y_temp)
	ani_temp = animation.FuncAnimation(fig, animate_temp, init_func = init_temp, interval = 500, blit = False)
	# battery
	t_bat = 1
	x_bat = np.arange(-50, 0, 0.5)
	y_bat = np.zeros(100)
	plt_bat = fig.add_subplot(224)
	plt_bat.set_title('Battery')
	plt_bat.set_xlabel("time[s]")
	plt_bat.set_ylabel("battery[%]")
	line_bat, = plt_bat.plot(x_bat, y_bat)
	ani_bat = animation.FuncAnimation(fig, animate_bat, init_func = init_bat, interval = 500, blit = False)

	fig.subplots_adjust(wspace = 0.5, hspace = 0.5)
	toolbar = NavigationToolbar2Tk(canvas, root)
	canvas.get_tk_widget().pack(side = 'left')

	frame2 = tkinter.Frame(frame1, borderwidth = 4)
	frame2.pack(padx = 5, pady = 20)

	m1_text_label = tkinter.Label(frame2, text = '送信コマンド・ログ',font = ("",18))
	m1_text_label.pack(side = 'top', fill = 'both')

	#textbox1 = tkinter.Text(frame2)
	textbox1 = tkinter.scrolledtext.ScrolledText(frame2)
	textbox1.configure(bd=1, highlightbackground='gray')
	textbox1.pack(side = 'top', fill = 'both', padx=10)
	sys.stdout.write = redirector

	m2_text_label = tkinter.Label(frame2, text = '\n\n\n撮影した写真データ', font = ("",18))
	m2_text_label.pack(side = 'top', fill = 'both', padx = 10)
	canvas2 = tkinter.Canvas(frame2, width = 400)
	canvas2.pack(side = 'top', fill = 'both')
	_thumbnail()

	frame = tkinter.Frame(root, width = 60, height = 40, borderwidth = 4, bg = 'gray')
	frame.pack(padx = 5, pady = 5)
	button1 = tkinter.Button(master = frame, text = "プログラム実行", command = _godrone, width = 20, fg = '#0000ff')
	button1.pack(fill = 'x', padx = 30, side = 'left')

	button2 = tkinter.Button(master = frame, text = "撮影した写真表示", command = _thumbnail, width = 20)
	button2.pack(fill = 'x', padx = 30, side = 'left')

	button3 = tkinter.Button(master = frame, text = "終了", command = _quit, width = 20)
	button3.pack(fill = 'x', padx = 30, side = 'left')

	button4 = tkinter.Button(master = frame, text = "ドローン緊急停止", command = _droneEmergency, width = 20, fg = '#ff0000')
	button4.pack(fill = 'x', padx = 30, side = 'left')

	with futures.ThreadPoolExecutor(max_workers = 10) as executor:
		executor.submit(tello_status_thread)
		executor.submit(video_recording_thread)
		executor.submit(start_thread)
		set_drone_flg(False)
		tkinter.mainloop()
