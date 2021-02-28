from telloedu.command import *
import time


def gotello():
    # ここから以下が修正可能です
    takeoff()
    forward(200)
    moji = get_qrcode()
    if moji == 'osaka':
        streamon()
        cw(360)
        streamoff()
    cw(90)
    forward(100)
    take_picture()
    land()
# これから以下は修正できません
if __name__ == "__main__":
    gotello()
    