import time
import matplotlib.pyplot as plt
from matplotlib.ticker import (FixedLocator, MultipleLocator)
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['figure.facecolor'] = 'darkgrey'
import numpy as np
 
def read_txt(path):
    data = list()
    with open(path) as file:
        lines = file.readlines()
        rigidity = [float(i) for i in lines[1].split()[1:]]
        for line in lines[3:]:
            raw = line.split()
            for i in range(2, len(raw)):
                raw[i] = float(raw[i])
            data.append([time.strptime(raw[0], "%Y-%m-%d")]+raw[2:])
    return rigidity, data
 
R, d = read_txt('./p_spectra_ams02.txt')
colors = ['r','g','b','c','m','w']
i = 0
fig, ax = plt.subplots()
ax.set_ylabel(r'$p/\;(m^2\;s\;sr\;GV)$')
print(len(d))
for line in d[:79:15]:
    i+=1
    print(f'{colors[i%len(colors)]} - {time.strftime("%Y-%m-%d %H:%M:%S", line[0])}')
    ax.set_xlabel('R, GV')
    print(R)
    print(line[1:])
    ax.loglog(R, line[1:], colors[i%len(colors)]+'.')
    #ax.set_xticks([10,20,30])
    ax.xaxis.set_major_locator(MultipleLocator(base=10))
    ax.grid()
plt.show()