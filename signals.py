import numpy as np #importing numpy with alias np
import pyaudio as pa
import struct
import matplotlib.pyplot as plt
import tkinter as tk
import time as t


_chunk = 1024 * 4
_format = pa.paInt16
_channels = 1
_rate = 44100    #in Hz
print("Started")
t.sleep(1)

p = pa.PyAudio()

stream = p.open(
    format = _format,
    channels = _channels,
    rate = _rate,
    input = 1,
    output = 1,
    frames_per_buffer = _chunk,
)

print("Loaded")

fig, ax = plt.subplots()
x = np.arange(0, 2*_chunk, 2)
line, = ax.plot(x, np.random.rand(_chunk))
ax.set_ylim(0,255)
ax.set_xlim(0,_chunk)
fig.show()

while True:
    data = stream.read(_chunk)
    dataInt = np.array(struct.unpack(str(2*_chunk) + 'B', data)[::2], dtype = 'b') + 128
    line.set_ydata(dataInt)
    fig.canvas.draw()
    fig.canvas.flush_events()