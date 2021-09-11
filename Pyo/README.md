
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Purpose](#purpose)
   * [Pyo - Python DSP module](#pyo---python-dsp-module)
      * [Structure of the library](#structure-of-the-library)
      * [Configuring the audio output (especially on Windows)](#configuring-the-audio-output-especially-on-windows)
         * [How to choose the audio host api on Windows](#how-to-choose-the-audio-host-api-on-windows)
         * [Tunning the Windows WASAPI driver](#tunning-the-windows-wasapi-driver)
         * [Server initialization examples](#server-initialization-examples)
         * [Choosing a specific device](#choosing-a-specific-device)
      * [Getting started](#getting-started)
         * [The Pyo Server and GUI](#the-pyo-server-and-gui)
         * [To interact or not to interact](#to-interact-or-not-to-interact)
         * [Changing Object Characteristics](#changing-object-characteristics)
         * [Chaining objects](#chaining-objects)
         * [Class example](#class-example)
      * [How to improve performance of your pyo programs](#how-to-improve-performance-of-your-pyo-programs)
         * [Use the subprocess or multiprocessing modules](#use-the-subprocess-or-multiprocessing-modules)
         * [Avoid memory allocation after initialization](#avoid-memory-allocation-after-initialization)
         * [Don’t do anything that can trigger the garbage collector](#dont-do-anything-that-can-trigger-the-garbage-collector)
         * [Pyo tips_Stop your unused audio objects](#pyo-tips_stop-your-unused-audio-objects)
         * [Pyo tips_Control attribute with numbers instead of PyoObjects](#pyo-tips_control-attribute-with-numbers-instead-of-pyoobjects)
         * [Pyo tips_Use a PyoObject when available](#pyo-tips_use-a-pyoobject-when-available)
         * [Pyo tips_Avoid trigonometric computation](#pyo-tips_avoid-trigonometric-computation)
         * [Pyo tips_Re-use your generators](#pyo-tips_re-use-your-generators)
         * [Pyo tips_Leave ‘mul’ and ‘add’ attributes to their defaults when possible](#pyo-tips_leave-mul-and-add-attributes-to-their-defaults-when-possible)
         * [Pyo tips_Avoid graphical updates](#pyo-tips_avoid-graphical-updates)
         * [Pyo tips_List of CPU intensive objects](#pyo-tips_list-of-cpu-intensive-objects)
   * [Pyo scripts collection](#pyo-scripts-collection)
   * [WASAPI](#wasapi)
      * [Working with WasapiOut](#working-with-wasapiout)
         * [Configuring WasapiOut](#configuring-wasapiout)
         * [Record Soundcard Output with WasapiLoopbackCapture](#record-soundcard-output-with-wasapiloopbackcapture)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)
   

# Purpose  
Take some note of Pyo (dedicated Python module for digital signal processing)

# Pyo - Python DSP module
[ belangeo /pyo ](https://github.com/belangeo/pyo)

## Structure of the library  
[Structure of the library](http://ajaxsoundstudio.com/pyodoc/structure.html)  
<img src="http://ajaxsoundstudio.com/pyodoc/_images/structure.png" width="800" height="600">  

## Configuring the audio output (especially on Windows) 
[Configuring the audio output (especially on Windows)](http://ajaxsoundstudio.com/pyodoc/winaudioinspect.html) 

### How to choose the audio host api on Windows  
```
Choosing the good audio API on Windows can turn out to be a real headache.

This document presents a script that will inspect your system and tell you if:

    Pyo can run in duplex mode. That means both audio input and output instead of output only.

    Pyo is able to connect to the different host APIs that are usually available on Windows.

In the hope that this will help you having a good experience with pyo under Windows!

https://github.com/belangeo/pyo/tree/master/scripts/win_audio_drivers_inspector.py
```

### Tunning the Windows WASAPI driver  
```
The Windows Audio Session API (WASAPI) is Microsoft’s most modern method for talking with audio devices. 
It is available in Windows since Vista. 
Pyo’s default host is DIRECTSOUND but you can change it to WASAPI by changing the winhost argument of the Server object. If the script above tells you:

    Host: wasapi ==> Failed…

there is some things you can do to make it work. 
Open the Sound window by double-clicking on the volume icon and choosing Playback Devices. 
Here, select your device and click on the Properties button. 

In the advanced tab, make sure that the sampling rate is the same that the one used by pyo (pyo defaults to 44100 Hz). 
You can check the exclusive mode box if you want, this will bypass the system mixer, default settings, and typically any effects provided by the audio driver.

Perform the same in the recording tab if you want to run pyo in duplex mode. If you got the message:

    No input available. Duplex mode should be turned off.

you’ll have to make sure first that there is an available input device in that tab.

If you use a cheap soundcard (typically, any built in soundcard is not very good!), 
you may have to increase the buffer size of the pyo’s Server in order to avoid glitches in the audio streams.
```

### Server initialization examples
```
# sampling rate = 44100 Hz, buffer size = 256, channels = 2, full duplex, host = DIRECTSOUND
s = Server()

# sampling rate = 48000 Hz, buffer size = 1024, channels = 2, full duplex, host = DIRECTSOUND
s = Server(sr=48000, buffersize=1024)

# sampling rate = 48000 Hz, buffer size = 512, channels = 2, full duplex, host = WASAPI
s = Server(sr=48000, buffersize=512, winhost="wasapi")

# sampling rate = 48000 Hz, buffer size = 512, channels = 2, output only, host = ASIO
s = Server(sr=48000, buffersize=512, duplex=0, winhost="asio")

# sampling rate = 96000 Hz, buffer size = 128, channels = 1, full duplex, host = ASIO
s = Server(sr=96000, nchnls=1, buffersize=128, duplex=1, winhost="asio")
```

### Choosing a specific device  
```
A single host API can target more than one available devices.

There is some useful functions that can help you in the choice of the audio device:

    pa_list_host_apis(): Prints the list of audio host APIs.

    pa_list_devices(): Prints the list of audio devices. The first column if the index of the device.

    pa_get_default_input(): Returns the index of the default input device.

    pa_get_default_output(): Returns the index of the default output device.

    pa_get_default_devices_from_host(host): Returns the default input and output devices for a given audio host.

Run this code to see the current state of your audio setup:
```

```
from pyo import *

print("Audio host APIS:")
pa_list_host_apis()
pa_list_devices()
print("Default input device: %i" % pa_get_default_input())
print("Default output device: %i" % pa_get_default_output())
```

```
If the default device for the desired host is not the one you want, 
you can tell the Server which device you want to use with the setInputDevice(x) and setOutputDevice(x) methods. These methods take the index of the desired device and must be called before booting the Server. 
Ex:
```

```
from pyo import *

s = Server(duplex=0)
s.setOutputDevice(0)
s.boot()
```

## Getting started  
```
Here is quick introduction to Pyo. 
It assumes you already know Python and basics about OOP (Object-Oriented Programming).
```

### The Pyo Server and GUI  
```
>>> from pyo import *
>>> s = Server().boot()
>>> s.start()
>>> a = Sine(mul=0.01).out()
```

```
The s variable holds the Server instance, which has been booted, using the boot function. 
Booting the server includes opening audio and MIDI interfaces, and setting up the sample rate and number of channels, but the server will not be processing audio until its start() method is called. 

Then we create a Sine object, and store it in variable a, after calling its out method. 
The Sine class defines a Sine wave oscillator. 
The out method from this class connects the output of the oscillator to the server audio outputs. 
I have set the mul attribute of the Sine object to make sure you don’t blow your ears when you play this, 
as the default amplitude multiplier is 1, i.e. a sine wave at the maximum amplitude before clipping! 
(But I’ll talk about attributes later…) You can stop the server with:

>>> s.stop()
```

### To interact or not to interact  
```
from pyo import *
s = Server().boot()
s.start()
a = Sine(mul=0.01).out()
s.gui(locals())
```

### Changing Object Characteristics  
```
The Sine class constructor is defined as:

Sine(self, freq=1000, phase=0, mul=1, add=0)
```

```
So you can give it a frequency, starting phase, multiplier and DC offset value when you create it. 
Also, if you want to do without the server gui, you can use the server method start() from your script, 
but you might need to use the sleep function from the time module to have your script run the server 
for a while if you are running Python non-interactively:
```

```
from pyo import *
import time
s = Server().boot()
a = Sine(440, 0, 0.1).out()
s.start()
time.sleep(1)
s.stop()
```

### Chaining objects  
```
Oscillators like the Sine class can be used as inputs to other classes, 
for example for frequency modulation:
```

```
from pyo import *
s = Server().boot()
mod = Sine(freq=6, mul=50)
a = Sine(freq=mod + 440, mul=0.1).out()
s.gui(locals())
```

```
You can create an envelope for a sine wave like this:
```

```
from pyo import *
s = Server().boot()
f = Adsr(attack=.01, decay=.2, sustain=.5, release=.1, dur=5, mul=.5)
a = Sine(mul=f).out()
f.play()
s.gui(locals())
```

### Class example  

```
All Classes in Pyo come with an example which shows how it can be used. 
To execute the example you can do:
```

```
>>> from pyo import *
>>> example(Harmonizer)
```

## How to improve performance of your pyo programs 
[How to improve performance of your pyo programs](http://ajaxsoundstudio.com/pyodoc/perftips.html#avoid-memory-allocation-after-initialization)  

### Use the subprocess or multiprocessing modules  
```
You can use the subprocess or multiprocessing modules to spawn your processes on multiple processors. 
From the python docs:

    The multiprocessing package offers both local and remote concurrency, 
    effectively side-stepping the Global Interpreter Lock by using subprocesses instead of threads. 
    Due to this, the multiprocessing module allows the programmer to fully leverage multiple processors on a given machine. 
    It runs on both Unix and Windows.
```

```
Here is a little example of using the multiprocessing module to spawn a lot of sine wave computations to multiple processors.
```

```
#!/usr/bin/env python
# encoding: utf-8
"""
Spawning lot of sine waves to multiple processes.
From the command line, run the script with -i flag.

Call quit() to stop the workers and quit the program.

"""
import time
import multiprocessing
from random import uniform
from pyo import Server, SineLoop

class Group(multiprocessing.Process):
    def __init__(self, num_of_sines):
        super(Group, self).__init__()
        self.daemon = True
        self._terminated = False
        self.num_of_sines = num_of_sines

    def run(self):
        # All code that should run on a separated
        # core must be created in the run() method.
        self.server = Server()
        self.server.deactivateMidi()
        self.server.boot().start()

        freqs = [uniform(400,800) for i in range(self.num_of_sines)]
        self.oscs = SineLoop(freq=freqs, feedback=0.1, mul=.005).out()

        # Keeps the process alive...
        while not self._terminated:
            time.sleep(0.001)

        self.server.stop()

    def stop(self):
        self._terminated = True

if __name__ == '__main__':
    # Starts four processes playing 500 oscillators each.
    jobs = [Group(500) for i in range(4)]
    [job.start() for job in jobs]

    def quit():
        "Stops the workers and quit the program."
        [job.stop() for job in jobs]
        exit()
```

### Avoid memory allocation after initialization  
```
Dynamic memory allocation (malloc/calloc/realloc) tends to be nondeterministic; 
the time taken to allocate memory may not be predictable, making it inappropriate for real time systems. 
To be sure that the audio callback will run smoothly all the time, 
it is better to create all audio objects at the program’s initialization and call their stop(), play(), out() methods when needed.

Be aware that a simple arithmetic operation involving an audio object will create a Dummy object (to hold the modified signal), 
thus will allocate memory for its audio stream AND add a processing task on the CPU. 
Run this simple example and watch the process’s CPU growing:
```

### Don’t do anything that can trigger the garbage collector  
```
The garbage collector of python is another nondeterministic process. 
You should avoid doing anything that can trigger it. 
So, instead of deleting an audio object, which can turn out to delete many stream objects, 
you should just call its stop() method to remove it from the server’s processing loop.
```

### Pyo tips_Stop your unused audio objects  
```
Whenever you don’t use an audio object (but you want to keep it for future uses), call its stop() method. 
This will inform the server to remove it from the computation loop. 
Setting the volume to 0 does not save CPU (everything is computed then multiplied by 0), the stop() method does. 
My own synth classes often looks like something like this:
```

```
class Glitchy:
    def __init__(self):
        self.feed = Lorenz(0.002, 0.8, True, 0.49, 0.5)
        self.amp = Sine(0.2).range(0.01, 0.3)
        self.src = SineLoop(1, self.feed, mul=self.amp)
        self.filt = ButLP(self.src, 10000)

    def play(self, chnl=0):
        self.feed.play()
        self.amp.play()
        self.src.play()
        self.filt.out(chnl)
        return self

    def stop(self):
        self.feed.stop()
        self.amp.stop()
        self.src.stop()
        self.filt.stop()
        return self
```

### Pyo tips_Control attribute with numbers instead of PyoObjects 
```
Objects internal processing functions are optimized when plain numbers are given to their attributes. 
Unless you really need audio control over some parameters, don’t waste CPU cycles and give fixed numbers to every attribute that don’t need to change over time. 
See this comparison:
```

```
n = Noise(.2)

# ~5% CPU
p1 = Phaser(n, freq=[100,105], spread=1.2, q=10,
            feedback=0.9, num=48).out()

# ~14% CPU
p2 = Phaser(n, freq=[100,105], spread=Sig(1.2), q=10,
            feedback=0.9, num=48).out()
```

### Pyo tips_Use a PyoObject when available  
```
Always look first if a PyoObject does what you want, 
it will always be more efficient than the same process written from scratch.

This construct, although pedagogically valid, will never be more efficient, 
in term of CPU and memory usage, than a native PyoObject (Phaser) written in C.
```

```
a = BrownNoise(.02).mix(2).out()

lfo = Sine(.25).range(.75, 1.25)
filters = []
for i in range(24):
    freq = rescale(i, xmin=0, xmax=24, ymin=100, ymax=10000)
    filter = Allpass2(a, freq=lfo*freq, bw=freq/2, mul=0.2).out()
    filters.append(filter)
```

```
It is also more efficient to use Biquadx(stages=4) than a cascade of four Biquad objects with identical arguments.
```

### Pyo tips_Avoid trigonometric computation
```
Avoid trigonometric functions computed at audio rate (Sin, Cos, Tan, Atan2, etc.), use simple approximations instead. 
For example, you can replace a clean Sin/Cos panning function with a cheaper one based on Sqrt:
```

### Pyo tips_Re-use your generators
```
Some times it possible to use the same signal for parallel purposes. 
Let’s study the next process:
```

```
# single white noise
noise = Noise()

# denormal signal
denorm = noise * 1e-24
# little jitter around 1 used to modulate frequency
jitter = noise * 0.0007 + 1.0
# excitation signal of the waveguide
source = noise * 0.7

env = Fader(fadein=0.001, fadeout=0.01, dur=0.015).play()
src = ButLP(source, freq=1000, mul=env)
wg = Waveguide(src+denorm, freq=100*jitter, dur=30).out()
```

```
Here the same white noise is used for three purposes at the same time. 
First, it is used to generate a denormal signal. 
Then, it is used to generate a little jitter applied to the frequency of the waveguide (that adds a little buzz to the string sound) and 
finally, we use it as the excitation of the waveguide. 
This is surely cheaper than generating three different white noises without noticeable difference in the sound.
```

### Pyo tips_Leave ‘mul’ and ‘add’ attributes to their defaults when possible  
```
There is an internal condition that bypass the object “post-processing” function when mul=1 and add=0. 
It is a good practice to apply amplitude control in one place instead of messing with the mul attribute of each objects.
```

```
# wrong
n = Noise(mul=0.7)
bp1 = ButBP(n, freq=500, q=10, mul=0.5)
bp2 = ButBP(n, freq=1500, q=10, mul=0.5)
bp3 = ButBP(n, freq=2500, q=10, mul=0.5)
rev = Freeverb(bp1+bp2+bp3, size=0.9, bal=0.3, mul=0.7).out()

# good
n = Noise(mul=0.25)
bp1 = ButBP(n, freq=500, q=10)
bp2 = ButBP(n, freq=1500, q=10)
bp3 = ButBP(n, freq=2500, q=10)
rev = Freeverb(bp1+bp2+bp3, size=0.9, bal=0.3).out()
```

### Pyo tips_Avoid graphical updates
```

```

### Pyo tips_List of CPU intensive objects
```
Here is a non-exhaustive list of the most CPU intensive objects of the library.

    Analysis

            Yin
            Centroid
            Spectrum
            Scope

    Arithmetic

            Sin
            Cos
            Tan
            Tanh
            Atan2

    Dynamic

            Compress
            Gate

    Special Effects

            Convolve

    Prefix Expression Evaluator

            Expr

    Filters

            Phaser
            Vocoder
            IRWinSinc
            IRAverage
            IRPulse
            IRFM

    Fast Fourier Transform

            CvlVerb

    Phase Vocoder

            Almost every objects!

    Signal Generators

            LFO

    Matrix Processing

            MatrixMorph

    Table Processing

            Granulator
            Granule
            Particule
            OscBank

    Utilities

            Resample
```


# Pyo scripts collection  
[ tiagovaz /pyo-collection](https://github.com/tiagovaz/pyo-collection)


## 
関数  | 説明
------------------------------------ | ---------------------------------------------


# WASAPI 
## ベストのオーディオインターフェイスはどれ？  
[ベストのオーディオインターフェイスはどれ？](https://pcde24bit192khz.blogspot.com/2010/04/blog-post_17.html)  

<img src="https://3.bp.blogspot.com/_G-bpb_5A1Qo/S8mvicbaRjI/AAAAAAAAAYs/PXQ39HBbeWI/s1600/20100417_windows_audio_interfaces.png" width="800" height="500">  

## Working with WasapiOut  
[Working with WasapiOut](https://github.com/naudio/NAudio/blob/master/Docs/WasapiOut.md)  

### Configuring WasapiOut  
[Configuring WasapiOut](https://github.com/naudio/NAudio/blob/master/Docs/WasapiOut.md#configuring-wasapiout)
```
When you create an instance of WasapiOut you can choose an output device. 
This is discussed in the enumerating output devices article.

There are a number of other options you can specify with WASAPI.

First of all, you can choose the "share mode". This is normally set to AudioClientShareMode.Shared 
which means you are happy to share the sound card with other audio applications in Windows. 
This however does mean that the sound card will continue to operate at whatever sample rate it is currently set to, 
irrespective of the sample rate of audio you want to play, and this is why the ResamplerDmoStream may be required.

If you choose AudioClientShareMode.Exclusive then you are requesting exclusive access to the sound card. 
The benefits of this approach are that you can specify the exact sample rate you want 
(has to be supported by the sound card and usually cannot be less than 44.1kHz), 
and you can often work at lower latencies. Obviously this mode impacts on other programs wanting to use the soundcard.

You can choose whether to use eventSync or not. 
This governs the behaviour of the background thread that is supplying audio to WASAPI. With event sync, 
you listen on an event for when WASAPI wants more audio. 
Without, you simply sleep for a short period of time and then provide more audio. Event sync is the default and generally is fine for most use cases.

You can also request the latency you want. This is only a request, and depending on the share mode may not have any effect. 
The lower the latency, the shorter the period of time between supplying audio to the soundcard and hearing it.

This can be very useful for real-time monitoring effects, 
but comes at the cost of higher CPU usage and potential for dropouts causing pops and clicks. 
So take care when adjusting this setting. The default is currently set to a fairly conservative 200ms.
```

### Record Soundcard Output with WasapiLoopbackCapture  
[Record Soundcard Output with WasapiLoopbackCapture](https://github.com/naudio/NAudio/blob/master/Docs/WasapiLoopbackCapture.md)

```
Lots of people ask how they can use NAudio to record the audio being played by another program. 
The answer is that unfortunately Windows does not provide an API that lets you target the output of one specific program to record. 
However, with WASAPI loopback capture, you can record all the audio that is being played out of a specific output device.

The audio has to be captured at the WaveFormat the device is already using. 
This will typically be stereo 44.1kHz (sometimes 48kHz) IEEE floating point. 
Obviously you can manually manipulate the audio after capturing it into another format, 
but for this example, we'll pass it straight onto the WAV file unchanged.

Let's start off by selecting a path to record to, creating an instance of WasapiLoopbackCapture (uses the default system device, 
but we can pass any rendering MMDevice that we want which we can find with MMDeviceEnumerator). 
We'll also create a WaveFileWriter using the capture WaveFormat.
```

```
var outputFolder = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "NAudio");
Directory.CreateDirectory(outputFolder);
var outputFilePath = Path.Combine(outputFolder, "recorded.wav");
var capture = new WasapiLoopbackCapture();
var writer = new WaveFileWriter(outputFilePath, capture.WaveFormat);
```

```
We need to handle the DataAvailable event, and it's very much the same approach here as recording to a WAV file from a regular WaveIn device. 
We just write BytesRecorded bytes from the Buffer into the WaveFileWriter. 
And in this example, I am stopping recording when we've captured 20 seconds worth of audio, by calling StopRecording.
```

```
capture.DataAvailable += (s, a) =>
{
    writer.Write(a.Buffer, 0, a.BytesRecorded);
    if (writer.Position > capture.WaveFormat.AverageBytesPerSecond * 20)
    {
        capture.StopRecording();
    }
};
```

```
When the RecordingStopped event fires, we Dispose our WaveFileWriter so we create a valid WAV file, 
and we're done recording so we'll Dispose our capture device as well.
```

```
capture.RecordingStopped += (s, a) =>
{
    writer.Dispose();
    writer = null;
    capture.Dispose();
};
```

```
All that remains is for us to start recording with StartRecording and wait for recording to finish by monitoring the CaptureState.
```

```
capture.StartRecording();
while (capture.CaptureState != NAudio.CoreAudioApi.CaptureState.Stopped)
{
    Thread.Sleep(500);
}
```
```

Now there is one gotcha with WasapiLoopbackCapture. If no audio is playing whatsoever, 
then the DataAvailable event won't fire. 
So if you want to record "silence", one simple trick is to simply use an NAudio playback device 
to play silence through that device for the duration of time you're recording. 
Alternatively, you could insert silence yourself when you detect gaps in the incoming audio.
```

* []()  

![alt tag]()
<img src="" width="" height="">  

# h1 size

## h2 size

### h3 size

#### h4 size

##### h5 size

*strong*strong  
**strong**strong  

> quote  
> quote

- [ ] checklist1
- [x] checklist2

* 1
* 2
* 3

- 1
- 2
- 3



