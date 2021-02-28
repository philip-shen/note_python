import ugoki
from telloedu.command import *
import telloedu.streaming as streaming



def set_drone_flg(x):
	global drone_flg
	drone_flg = x

def get_drone_flg():
	return(drone_flg)

def start_thread():
	while streaming.main_thread:
		try:
			if get_drone_flg():
				command()
				ugoki.gotello()
				#end()
				print("End")
				set_drone_flg(False)
		except KeyboardInterrupt:
			emergency()
			print('\n..... Keyboard Interrupt: emergency!! ......\n')
		except TypeError:
			emergency()
			print('\n..... Type Error: emergency!! ......\n')

drone_flg = False
