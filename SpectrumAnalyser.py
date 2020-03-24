import numpy as np #importing numpy with alias np
import pyaudio as pa
import struct
import matplotlib.pyplot as plt
import tkinter as tk
from time import time
from scipy.fftpack import fft


previous_time = time()

chunk_size = int(input("Enter Buffer Size:\n"))

_chunk = 1024 * chunk_size
_format = pa.paInt16
_channels = 1
_rate = 44100    #in Hz
print("Started")

p = pa.PyAudio()
print("Device Name \t\t\t\t\t Index")

for i in range(5):
    device = p.get_device_info_by_index(i)
    if "Microphone" in device["name"]:
        _name = device["name"]
        _index = device["index"]
        if len(_name) > 37:
            string = "\t"
        elif len(_name) < 31:
            string = "\t\t\t"
        elif len(_name) == 31:
            string = "\t\t"
        else:
            string = "\t"
        print(_name,string,_index)

index_of_mic = int(input("Enter The Device Index:\n"))


stream = p.open(
    format = _format,
    channels = _channels,
    rate = _rate,
    input = 1,
    output = 1,
    frames_per_buffer = _chunk,
    input_device_index= index_of_mic
)


print("Loaded")

fig, (ax,ax2) = plt.subplots(2)

x_fft = np.linspace(0,_rate,_chunk)
x = np.arange(0, 2*_chunk, 2)

line, = ax.plot(x, np.random.rand(_chunk),"-")
line_fft, = ax2.semilogx(x_fft, np.random.rand(_chunk),'r')

ax.set_ylim(-60000,60000)
ax.set_xlim(0,_chunk)
ax2.set_xlim(20,_rate/2)
ax2.set_ylim(0,1)

fig.show()

while True:
    current_time = time()
    print(int(1/(current_time-previous_time)))
    previous_time=current_time

    data = stream.read(_chunk)

    dataInt = np.array(struct.unpack(str(_chunk) + 'h', data))
    y_fft = np.fft.fft(dataInt)
    line_fft.set_ydata(np.abs(y_fft)*2/(33000*_chunk))
    line.set_ydata(dataInt)
    fig.canvas.draw()
    fig.canvas.flush_events()