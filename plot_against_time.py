import time
import matplotlib.pyplot as plt
from matplotlib.ticker import (FixedLocator, MultipleLocator)
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['figure.facecolor'] = 'darkgrey'

import numpy as np

import sqlite3
conn = sqlite3.connect("ssdc.db")
cursor = conn.cursor()

def select_data(ranges):
	select = " OR ".join(f"rigidity_min={r[0]}" for r in ranges)
	cursor.execute(f"SELECT * FROM AMS02 WHERE {select}")
	data = cursor.fetchall()
	data.sort(key=lambda l: l[1])
	#print("\n".join(str(i).replace(',','\t') for i in data))
	return data

def get_ranges():
	cursor.execute(f"SELECT * FROM AMS02 LIMIT 1")
	data = cursor.fetchall()
	cursor.execute(f"SELECT * FROM AMS02 WHERE time_min='{data[0][1]}'")
	rows = cursor.fetchall()
	return [(r[3], r[4]) for r in rows]

fig, ax = plt.subplots()
def plot_one(data, rigidity, color):
	lines = [l for l in data if rigidity[0] == l[3]]
	time = [l[1].split('T')[0] for l in lines]
	flux = [l[5] for l in lines]
	ax.set_ylabel('flux')
	ax.set_xlabel('time')
	ax.plot(time, flux, f'{color}--', label=f"{rigidity[0]}-{rigidity[1]} GV")
	#ax.semilogy(time, flux, f'{color}.')
	ax.xaxis.set_major_locator(MultipleLocator(base=24))
	ax.grid()

rigidity_ranges = get_ranges()
ranges = [f"{i}) {r[0]}-{r[1]}" for i, r in enumerate(rigidity_ranges)]
ranges = [f"{ranges[i]}\t\t{ranges[i+len(ranges)//2]}" for i in range(0, len(ranges)//2)]
ranges = "\n".join(ranges)

print(f'''Select rigidity ranges to plot (GV):\n{ranges}
Please enter numbers separated with \",\": ''')
user_ranges = [rigidity_ranges[int(r.strip())] for r in input().split(',')]
print(f"Selected ranges: {user_ranges}")

data = select_data(user_ranges)
colors = ['r','y','c','m','w','b']
for i in range(len(user_ranges)):
	plot_one(data, user_ranges[i], colors[i % len(colors)])

legend = plt.legend()
plt.setp(legend.get_texts(), color='grey')
plt.show()