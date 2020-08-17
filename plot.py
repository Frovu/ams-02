import time
import matplotlib.pyplot as plt
from matplotlib.ticker import (FixedLocator, MultipleLocator)
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['figure.facecolor'] = 'darkgrey'

import numpy as np

import sqlite3
conn = sqlite3.connect("ssdc.db")
cursor = conn.cursor()

def read_txt(path):
	data = list()
	with open(path) as file:
		lines = file.readlines()
		rigidity = lines[1].split()[1:]
		for line in lines[3:]:
			raw = line.split()
			for i in range(2, len(raw)):
				raw[i] = float(raw[i])
			data.append([time.strptime(raw[0], "%Y-%m-%d")]+raw[2:])
	return rigidity, data

def plot_old(data):
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
		ax.semilogy(R, line[1:], colors[i%len(colors)]+'.')
		#ax.set_xticks([10,20,30])
		ax.xaxis.set_major_locator(MultipleLocator(base=10))
		ax.grid()
	plt.show()

def select_data():
	cursor.execute("SELECT * FROM AMS02 WHERE particle='p'")
	data = cursor.fetchall()
	data.sort(key=lambda l: l[1])
	#print("\n".join(str(i).replace(',','\t') for i in data))
	return data

def get_spectrum(data, time):
	lines = [l for l in data if time in l[1]]
	flux = [l[5] for l in lines]
	rigidity = [(l[3]+l[4])/2 for l in lines]
	return flux, rigidity

fig, ax = plt.subplots()
def plot_one(flux, rigidity, color):
	ax.set_ylabel('flux')
	ax.set_xlabel('R, GV')
	#ax.plot(rigidity, flux, f'{color}.')
	ax.loglog(rigidity, flux, f'{color}.')
	#ax.xaxis.set_major_locator(MultipleLocator(base=10))
	ax.grid()

def get_and_plot(data, time, color):
	f, r = get_spectrum(data, time)
	plot_one(f, r, color)

data = select_data()
get_and_plot(data, '2011-05-19', 'r')
#get_and_plot(data, '2015-04', 'c')
#get_and_plot(data, '2017-04', 'y')


plt.show()