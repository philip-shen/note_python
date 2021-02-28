#
# Tello Edu (SDK2.0 対応) Python3 status Library
#

import csv
import datetime
import re
import socket

import telloedu.streaming as streaming

Tello_TOF = 0
Tello_Height = 0
Tello_Bat = 0
Tello_Pitch = 0
Tello_Roll = 0
Tello_yaw = 0
Tello_Temph = 0


def tello_status_thread():
	global Tello_Temph
	global Tello_TOF
	global Tello_Height
	global Tello_Bat
	global Tello_Pitch
	global Tello_Roll
	global Tello_yaw
	path = './data/'
	date_fmt = '%Y-%m-%d_%H%M%S'
	file_name = '%stellostatus-%s.csv' % (path, datetime.datetime.now().strftime(date_fmt))
	csvhead = ["mid", "x", "y", "z", "xxx", "pitch", "roll", "yaw", "vgx", "vgy", "vgz", "templ", "temph", "tof",
	           "h", "bat", "baro", "time", "agx", "agy", "sgz"]
	tshost = '0.0.0.0'
	tsport = 8890
	tslocaddr = (tshost, tsport)
	tssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	tssock.bind(tslocaddr)

	while streaming.main_thread:
		try:
			data, server = tssock.recvfrom(1518)
			res = data.decode(encoding = "utf-8")
			res2 = re.sub('[a-z:\n\r]', '', res)
			res3 = res2.split(';')
			Tello_Temph = res3[12]
			Tello_TOF = res3[13]
			Tello_Height = res3[14]
			Tello_Bat = res3[15]
			Tello_Pitch = res3[5]
			Tello_Roll = res3[6]
			Tello_yaw = res3[7]
			try:
				with open(file_name, 'x') as f:
					writer = csv.writer(f)
					writer.writerow(csvhead)
					writer.writerow(res3)
			except FileExistsError:
				with open(file_name, 'a') as f:
					writer = csv.writer(f)
					writer.writerow(res3)
		except socket.error:
			print('\nTello Status Exit . . .\n')
			tssock.close()
			break
		except KeyboardInterrupt:
			print('\nTello Status Exit . . .\n')
			tssock.close()
			break
	tssock.close()

def get_temph():
	global Tello_Temph
	return(float(Tello_Temph))

def get_tof():
	global Tello_TOF
	return (float(Tello_TOF))


def get_height():
	global Tello_Height
	return (float(Tello_Height))


def get_bat():
	global Tello_Bat
	return (float(Tello_Bat))


def get_pitch():
	global Tello_Pitch
	return (Tello_Pitch)


def get_roll():
	global Tello_Roll
	return (Tello_Roll)


def get_yaw():
	global Tello_yaw
	return (Tello_yaw)

