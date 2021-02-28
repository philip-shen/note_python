#
# Tello Edu (SDK2.0 対応) Python3 Command Library
#

import socket
import time

from telloedu.tellolib import *
from telloedu.status import *

import telloedu.streaming as streaming

# Create a UDP socket
host = ''
port = 9000
tello_ip = '192.168.10.1'
tello_port = 8889
locaddr = (host, port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = (tello_ip, tello_port)
sock.bind(locaddr)


# command
def emergency():
	cmd = 'emergency'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: ', cmd, ' to ', tello_address)
	try:
		sock.sendto(cmd, tello_address)

	except socket.error:
		print('\n....ERROR: ', cmd, ' ....\n')
	streaming.video_recording = 0
	# streaming.main_thread = False
	# streaming.set_mainthread(False)


def command():
	cmd = 'command'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: ', cmd, ' to ', tello_address)
	try:
		sock.sendto(cmd, tello_address)
		while streaming.main_thread:
			data, server = sock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			if res == 'ok' or res == 'error':
				print('recv: ', cmd, ' ', res)
				break
	except socket.error:
		print('\n....ERROR: ', cmd, ' ....\n')
		sock.close()


def takeoff():
	cmd = 'takeoff'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: ', cmd, ' to ', tello_address)
	try:
		sock.sendto(cmd, tello_address)
		while streaming.main_thread:
			data, server = sock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			if res == 'ok' or res == 'error':
				print('recv: ', cmd, ' ', res)
				break
	except socket.error:
		print('\n....ERROR: ', cmd, ' ....\n')
		sock.close()


def land():
	cmd = 'land'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: ', cmd, ' to ', tello_address)
	try:
		sock.sendto(cmd, tello_address)
		while streaming.main_thread:
			data, server = sock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			if res == 'ok' or res == 'error':
				print('recv: ', cmd, ' ', res)
				break
	except socket.error:
		print('\n....ERROR: ', cmd, ' ....\n')
		sock.close()


def stop():
	cmd = 'stop'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: ', cmd, ' to ', tello_address)
	try:
		sock.sendto(cmd, tello_address)
		while streaming.main_thread:
			data, server = sock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			if res == 'ok' or res == 'error':
				print('recv: ', cmd, ' ', res)
				break
	except socket.error:
		print('\n....ERROR: ', cmd, ' ....\n')
		sock.close()


def up(x):
	if type(x) is int:
		if (20 <= x) and (x <= 200):
			cmd = 'up ' + str(x)
			cmd = cmd.encode(encoding = "utf-8")
			print('Send: ', cmd, ' to ', tello_address)
			try:
				sock.sendto(cmd, tello_address)
				while streaming.main_thread:
					data, server = sock.recvfrom(1518)
					res = data.decode(encoding = "utf-8")
					if res == 'ok' or res == 'error':
						print('recv: ', cmd, ' ', res)
						break
			except socket.error:
				print('\n....ERROR: ', cmd, ' ....\n')
				sock.close()
		else:
			print('\n...引数の値が10...200の間でない\n')
	else:
		print('\n...引数の値が整数型でない\n')


def down(x):
	if type(x) is int:
		if 20 <= x <= 200:
			cmd = 'down ' + str(x)
			cmd = cmd.encode(encoding = "utf-8")
			print('Send: ', cmd, ' to ', tello_address)
			try:
				sock.sendto(cmd, tello_address)
				while streaming.main_thread:
					data, server = sock.recvfrom(1518)
					res = data.decode(encoding = "utf-8")
					if res == 'ok' or res == 'error':
						print('recv: ', cmd, ' ', res)
						break
			except socket.error:
				print('\n....ERROR: ', cmd, ' ....\n')
				sock.close()
		else:
			print('\n...引数の値が10...200の間でない\n')
	else:
		print('\n...引数の値が整数型でない\n')


def left(x):
	if type(x) is int:
		if 20 <= x <= 200:
			cmd = 'left ' + str(x)
			cmd = cmd.encode(encoding = "utf-8")
			print('Send: ', cmd, ' to ', tello_address)
			try:
				sock.sendto(cmd, tello_address)
				while streaming.main_thread:
					data, server = sock.recvfrom(1518)
					res = data.decode(encoding = "utf-8")
					if res == 'ok' or res == 'error':
						print('recv: ', cmd, ' ', res)
						break
			except socket.error:
				print('\n....ERROR: ', cmd, ' ....\n')
				sock.close()
		else:
			print('\n...引数の値が10...200の間でない\n')
	else:
		print('\n...引数の値が整数型でない\n')


def right(x):
	if type(x) is int:
		if 20 <= x <= 200:
			cmd = 'right ' + str(x)
			cmd = cmd.encode(encoding = "utf-8")
			print('Send: ', cmd, ' to ', tello_address)
			try:
				sock.sendto(cmd, tello_address)
				while streaming.main_thread:
					data, server = sock.recvfrom(1518)
					res = data.decode(encoding = "utf-8")
					if res == 'ok' or res == 'error':
						print('recv: ', cmd, ' ', res)
						break
			except socket.error:
				print('\n....ERROR: ', cmd, ' ....\n')
				sock.close()
		else:
			print('\n...引数の値が10...200の間でない\n')
	else:
		print('\n...引数の値が整数型でない\n')


def forward(x):
	if type(x) is int:
		if 20 <= x <= 200:
			cmd = 'forward ' + str(x)
			cmd = cmd.encode(encoding = "utf-8")
			print('Send: ', cmd, ' to ', tello_address)
			try:
				sock.sendto(cmd, tello_address)
				while streaming.main_thread:
					data, server = sock.recvfrom(1518)
					res = data.decode(encoding = "utf-8")
					if res == 'ok' or res == 'error':
						print('recv: ', cmd, ' ', res)
						break
			except socket.error:
				print('\n....ERROR: ', cmd, ' ....\n')
				sock.close()
		else:
			print('\n...引数の値が10...200の間でない\n')
	else:
		print('\n...引数の値が整数型でない\n')


def back(x):
	if type(x) is int:
		if 20 <= x <= 200:
			cmd = 'back ' + str(x)
			cmd = cmd.encode(encoding = "utf-8")
			print('Send: ', cmd, ' to ', tello_address)
			try:
				sock.sendto(cmd, tello_address)
				while streaming.main_thread:
					data, server = sock.recvfrom(1518)
					res = data.decode(encoding = "utf-8")
					if res == 'ok' or res == 'error':
						print('recv: ', cmd, ' ', res)
						break
			except socket.error:
				print('\n....ERROR: ', cmd, ' ....\n')
				sock.close()
		else:
			print('\n...引数の値が10...200の間でない\n')
	else:
		print('\n...引数の値が整数型でない\n')


def cw(x):
	if type(x) is int:
		if 1 <= x <= 360:
			cmd = 'cw ' + str(x)
			cmd = cmd.encode(encoding = "utf-8")
			print('Send: ', cmd, ' to ', tello_address)
			try:
				sock.sendto(cmd, tello_address)
				while streaming.main_thread:
					data, server = sock.recvfrom(1518)
					res = data.decode(encoding = "utf-8")
					if res == 'ok' or res == 'error':
						print('recv: ', cmd, ' ', res)
						break
			except socket.error:
				print('\n....ERROR: ', cmd, ' ....\n')
				sock.close()
		else:
			print('\n...引数の値が1...360の間でない\n')
	else:
		print('\n...引数の値が整数型でない\n')


def ccw(x):
	if type(x) is int:
		if 1 <= x <= 360:
			cmd = 'ccw ' + str(x)
			cmd = cmd.encode(encoding = "utf-8")
			print('Send: ', cmd, ' to ', tello_address)
			try:
				sock.sendto(cmd, tello_address)
				while streaming.main_thread:
					data, server = sock.recvfrom(1518)
					res = data.decode(encoding = "utf-8")
					if res == 'ok' or res == 'error':
						print('recv: ', cmd, ' ', res)
						break
			except socket.error:
				print('\n....ERROR: ', cmd, ' ....\n')
				sock.close()
		else:
			print('\n...引数の値が1...360の間でない\n')
	else:
		print('\n...引数の値が整数型でない\n')


def set_speed(x):
	if type(x) is int:
		if 10 <= x <= 100:
			cmd = 'speed ' + str(x)
			cmd = cmd.encode(encoding = "utf-8")
			print('Send: ', cmd, ' to ', tello_address)
			try:
				sock.sendto(cmd, tello_address)
				while streaming.main_thread:
					data, server = sock.recvfrom(1518)
					res = data.decode(encoding = "utf-8")
					if res == 'ok' or res == 'error':
						print('recv: ', cmd, ' ', res)
						break
			except socket.error:
				print('\n . . .\n')
				sock.close()
		else:
			print('\n...引数の値が10...100の間でない\n')
	else:
		print('\n...引数の値が整数型でない\n')


def streamon():
	cmd = 'streamon'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: ', cmd, ' to ', tello_address)
	try:
		sock.sendto(cmd, tello_address)
		while streaming.main_thread:
			data, server = sock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			if res == 'ok' or res == 'error':
				streaming.video_recording = 1
				print('recv: ', cmd, ' ', res)
				break
		time.sleep(5)
	except socket.error:
		print('\n....ERROR: ', cmd, ' ....\n')
		streaming.video_recording = 0
		sock.close()


def streamoff():
	cmd = 'streamoff'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: ', cmd, ' to ', tello_address)
	try:
		# time.sleep(5)
		sock.sendto(cmd, tello_address)
		while streaming.main_thread:
			data, server = sock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			if res == 'ok' or res == 'error':
				streaming.video_recording = 0
				print('recv: ', cmd, ' ', res)
				break
	except socket.error:
		print('\n....ERROR: ', cmd, ' ....\n')
		streaming.video_recording = 0
		sock.close()


def get_qrcode():
	cmd = 'streamon'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: get_qrcode(', cmd, ') to ', tello_address)
	try:
		sock.sendto(cmd, tello_address)
		while streaming.main_thread:
			data, server = sock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			if res == 'ok' or res == 'error':
				streaming.video_recording = 10
				print('recv: get_qrcode(', cmd, ') ', res)
				break
	except socket.error:
		print('\n....ERROR:  QR Code ....\n')
		streaming.video_recording = 0
		sock.close()

	time.sleep(5)
	cmd = 'streamoff'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: get_qrcode(', cmd, ') to ', tello_address)
	try:
		sock.sendto(cmd, tello_address)
		while streaming.main_thread:
			data, server = sock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			if res == 'ok' or res == 'error':
				streaming.video_recording = 0
				print('recv: get_qrcode(', cmd, ') ', res)
				break
	except socket.error:
		print('\n....ERROR:  QR Code ....\n')
		streaming.video_recording = 0
		sock.close()
	code = streaming.qr_code
	streaming.qr_code = ""
	return code

def take_picture():
	cmd = 'streamon'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: take a pictur(', cmd, ') to ', tello_address)
	try:
		sock.sendto(cmd, tello_address)
		while streaming.main_thread:
			data, server = sock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			if res == 'ok' or res == 'error':
				streaming.video_recording = 20
				print('recv: take a photograph(', cmd, ') ', res)
				break
	except socket.error:
		print('\n....ERROR:  take a photograph ....\n')
		streaming.video_recording = 0
		sock.close()

	time.sleep(5)
	cmd = 'streamoff'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: take a photograph(', cmd, ') to ', tello_address)
	try:
		sock.sendto(cmd, tello_address)
		while streaming.main_thread:
			data, server = sock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			if res == 'ok' or res == 'error':
				streaming.video_recording = 0
				print('recv: take a photograph(', cmd, ') ', res)
				break
	except socket.error:
		print('\n....ERROR:  take a photograph ....\n')
		streaming.video_recording = 0
		sock.close()

def get_speed():
	cmd = 'speed?'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: ', cmd, ' to ', tello_address)
	try:
		sock.sendto(cmd, tello_address)
		while streaming.main_thread:
			data, server = sock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			if is_float(res):
				res = float(res)
				print('recv: ', cmd, ' ', res, ' cm/s')
				return res
	except socket.error:
		print('\n .......get_speed.........\n')
		sock.close()


def get_battery():
	cmd = 'battery?'
	cmd = cmd.encode(encoding = "utf-8")
	print('Send: ', cmd, ' to ', tello_address)
	try:
		sock.sendto(cmd, tello_address)
		while streaming.main_thread:
			data, server = sock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			if is_int(res):
				res = int(res)
				print('recv: ', cmd, ' ', res, '%')
				return res
	except socket.error:
		print('\n .......get_battery.........\n')
		sock.close()


def end():
	print('Script: end1')
	streaming.main_thread = False
	streaming.set_mainthread(False)
	print('Script: end2')
	time.sleep(2)
	print('Script: end3')
	sock.close()
	print('Script: end4')