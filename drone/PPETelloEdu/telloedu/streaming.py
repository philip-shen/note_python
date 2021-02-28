#
# Tello Edu (SDK2.0 対応) Python3 Streaming Library
#

import datetime
import cv2
from PIL import Image
from pyzbar.pyzbar import decode

video_recording = 0
qr_code = ""

# Video Recording Thread
def video_recording_thread():
	global video_recording
	while main_thread:
		try:
			if video_recording == 1:
				video_recording_start()
			if video_recording == 10:
				analyze_qrcode()
			if video_recording == 20:
				take_photo()
			if video_recording == 999:
				break
		except KeyboardInterrupt:
			print('\nExit . . .\n')
			break


def video_recording_start():
	global video_recording
	vr_udp_ip = '0.0.0.0'
	vr_udp_port = 11111
	path = './mpg/'
	date_fmt = '%Y-%m-%d_%H%M%S'
	file_name = '%stello-video-%s.m4v' % (path, datetime.datetime.now().strftime(date_fmt))
	udp_video_address = 'udp://@' + vr_udp_ip + ':' + str(vr_udp_port)

	cap = cv2.VideoCapture(udp_video_address)
	frame_rate = cap.get(cv2.CAP_PROP_FPS)  # 40   フレームレート
	size = (640, 480)  # 動画の画面サイズ
	fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
	writer = cv2.VideoWriter(file_name, fmt, frame_rate, size)

	if not cap.isOpened():
		cap.open(udp_video_address)

	while video_recording == 1:
		try:
			ret, frame = cap.read()
			frame = cv2.resize(frame, size)
			writer.write(frame)
		except cv2.error:
			print('\nExit (cv2.error). . .\n')
			writer.release()
			cap.release()
			break
	#video_recording = 0
	writer.release()
	cap.release()


def analyze_qrcode():
	global video_recording
	global qr_code
	qr_code = ""

	if video_recording <= 9:
		return 'analyze qrcode: error'

	vr_udp_ip = '0.0.0.0'
	vr_udp_port = 11111
	path = './img/'
	date_fmt = '%Y-%m-%d_%H%M%S'
	file_name = '%sqrcode-%s.png' % (path, datetime.datetime.now().strftime(date_fmt))
	cap = None
	udp_video_address = 'udp://@' + vr_udp_ip + ':' + str(vr_udp_port)

	if cap is None:
		cap = cv2.VideoCapture(udp_video_address)

	if not cap.isOpened():
		cap.open(udp_video_address)

	ret, frame = cap.read()
	cv2.imwrite(file_name, frame)
	qr = decode(Image.open(file_name))
	if len(qr) != 0:
		qr_code = qr[0][0].decode('utf-8', 'ignore')
		print('QR Code: %s' % qr_code)
	else:
		qr_code = ""
		print('No QR Code !!!!!!')
	video_recording = 0
	cap.release()

def take_photo():
	global video_recording

	if video_recording <= 19:
		return 'take a photo: error'

	vr_udp_ip = '0.0.0.0'
	vr_udp_port = 11111
	path = './img/'
	date_fmt = '%Y-%m-%d_%H%M%S'
	file_name = '%sphoto-%s.png' % (path, datetime.datetime.now().strftime(date_fmt))
	cap = None
	udp_video_address = 'udp://@' + vr_udp_ip + ':' + str(vr_udp_port)

	if cap is None:
		cap = cv2.VideoCapture(udp_video_address)

	if not cap.isOpened():
		cap.open(udp_video_address)

	ret, frame = cap.read()
	cv2.imwrite(file_name, frame)

	video_recording = 0
	cap.release()

main_thread = True

def set_mainthread(x):
	global main_thread
	main_thread = x