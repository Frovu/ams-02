import time
import matplotlib.pyplot as plt
from matplotlib.ticker import (FixedLocator, MultipleLocator)
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['figure.facecolor'] = 'darkgrey'

import numpy as np

import sqlite3
conn = sqlite3.connect("ssdc.db")
cursor = conn.cursor()

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
	errors = [(l[6]+l[7]+l[8]+l[9])/2 for l in lines]
	errors = np.array(errors) * 3
	return flux, rigidity, errors

fig, ax = plt.subplots()
ax.set_ylabel('flux')
ax.set_xlabel('R, GV')
def plot_one(flux, rigidity, errors, color, label):
	#ax.plot(rigidity, flux, f'{color}.', label=label)
	ax.set_xscale('log')
	ax.set_yscale('log')
	ax.errorbar(rigidity, flux, fmt=f'{color}.', yerr=errors, label=label)
	#ax.xaxis.set_major_locator(MultipleLocator(base=10))
	#ax.grid()

def g(r, param):
	return 10000 * (r ** (param))

def plot_model(data, time, param, c):
	f, rigidity, e = get_spectrum(data, time)
	flux = [g(r, param) for r in rigidity]
	ax.loglog(rigidity[1:], flux[1:], c, label='model')
	#ax.loglog(rigidity, flux, 'w', label='model')

def get_and_plot(data, time, color, label):
	f, r, e = get_spectrum(data, time)
	plot_one(f, r, e, color, label)

def find_date(data, date):
	for r in data:
		if date > r[1] and date < r[2]:
			return r[1]
	return False

data = select_data()

print(f'''Enter dates separated by \',\' within range from {data[0][1].split("T")[0]} to {data[-1][1].split("T")[0]}
i.e. \'2015-04, 2015-06\':''')
user_dates = [a.strip() for a in input().split(',')]
user_dates = ['2014', '2015', '2016', '2017-04']
dates = []
# find date periods
for d in user_dates:
	date = find_date(data, d)
	if date:
		dates.append(date)
	else:
		print(f"Failed to resolve date: {d}")
		exit(1)

def plot_dates(data, dates):
	colors = ['r','y','c','m','w','b']
	for i, d in enumerate(dates):
		get_and_plot(data, d, colors[i % len(colors)], d.split("T")[0])

#get_and_plot(data, '2015-04', 'c')
#get_and_plot(data, '2017-04', 'y')
plot_model(data, dates[0], -2.65, 'w')
plot_dates(data, dates)
ax.grid()
legend = plt.legend()
plt.setp(legend.get_texts(), color='grey')
plt.show()
