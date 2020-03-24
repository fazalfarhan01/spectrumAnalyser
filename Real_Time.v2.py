import numpy as np #importing numpy with alias np
import pyaudio as pa
import struct
import matplotlib.pyplot as plt
import tkinter as tk
from time import time

previous_time = time()

chunk_size = int(input("Enter Buffer Size:\n"))


_chunk = 1024 * chunk_size
_format = pa.paInt16
_channels = 1
_rate = 44100    #in Hz
print("Started")

p = pa.PyAudio()

for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    if "Microphone" in device["name"]:
        print(device["name"],device["index"])

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

fig, ax = plt.subplots()
x = np.arange(0, 2*_chunk, 2)
line, = ax.plot(x, np.random.rand(_chunk),"r")
ax.set_ylim(-66536,66535)
ax.set_xlim(0,_chunk)
fig.show()

while True:
    current_time = time()
    print(int(1/(current_time-previous_time)))
    previous_time=current_time
    data = stream.read(_chunk)
    dataInt = np.array(struct.unpack(str(_chunk) + 'h', data))
    line.set_ydata(dataInt)
    fig.canvas.draw()
    fig.canvas.flush_events()