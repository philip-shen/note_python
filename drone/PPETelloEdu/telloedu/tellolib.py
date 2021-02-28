#
# Tello Edu (SDK2.0 対応) Python3 Common Library
#

# type check function
def is_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


def is_float(s):
	try:
		float(s)
		return True
	except ValueError:
		return False
