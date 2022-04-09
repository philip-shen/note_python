import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

def plot(x, c="c", label=""):
    plt.plot(x, c=c, label=label, alpha=0.8)
    plt.ylim(-1.5, 1.5)
    plt.legend(loc='upper right')
    plt.grid()


duration = 0.025 # 25 msec
sr = 44100 # サンプリング周波数
t  = np.arange(0, sr*duration) / sr # サンプル点の時間
fo = 261.63 #　基本周波数(C4)


# サイン波
x = np.sin(2*np.pi*fo*t)
plt.subplot(5,1,1)
plot(x, "c", "Sine wave")

# 矩形波
x = scipy.signal.square(2*np.pi*fo*t)
plt.subplot(5,1,2)
plot(x, "m", "Square wave")

# のこぎり波（鋸歯状）
x = scipy.signal.sawtooth(2*np.pi*fo*t)
plt.subplot(5,1,3)
plot(x, "g", "Sawtooth wave")

# 三角波
x = scipy.signal.sawtooth(2*np.pi*fo*t, width=0.5)
plt.subplot(5,1,4)
plot(x, "b", "Triangle wave")

# 白色雑音
x = np.random.normal(0.0, 0.25, len(t))
x[x<-1.0] = -1.0
x[x>=1.0] = 1.0
plt.subplot(5,1,5)
plot(x, "k", "Whitenoise")

plt.tight_layout()
plt.show()


# 矩形波　デューティー比変更
cmap = plt.get_cmap("tab10")
duties = np.arange(0.1, 1.0, 0.2)
plt.clf()
for k, duty in enumerate(duties):
    plt.subplot(len(duties), 1, k+1)
    x = scipy.signal.square(2*np.pi*fo*t, duty=duty)
    plot(x, cmap(k), f"Square wave (duty={duty:0.1f})")


# 三角：鋸歯状波　width比変更
cmap = plt.get_cmap("tab10")
width_list = np.arange(0.0, 1.1, 0.2)
plt.clf()
for k, width in enumerate(width_list):
    plt.subplot(len(width_list), 1, k+1)
    x = scipy.signal.sawtooth(2*np.pi*fo*t, width=width)
    plot(x, cmap(k), f"Sawtooth wave (width={width:0.1f})")

plt.tight_layout()
plt.show()