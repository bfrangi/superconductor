 
import re
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

def get_data(filename):
	f = open(filename, 'r', encoding='latin-1')
	lines = f.read().strip()
	f.close()

	lines = re.sub(',', '.', lines)
	#h = re.findall(r'[^\=]{0,5}\=[^\n]+\n', lines)
	#h = h[4].split('\t')

	lines = re.sub(r'[^\=]{0,5}\=[^\n]+\n', r'', lines)
	data = {
		"time": [],
		"voltage temperature": [],
		"voltage superconductor": [],
		"temperature": []
	}
	d = []
	for line in lines.split('\n'):
		d.append(line.split('\t'))
	for row in d:
		data["time"].append(float(row[0]))
		data["voltage temperature"].append(float(row[1]))
		data["voltage superconductor"].append(float(row[2]))
		data["temperature"].append(float(row[4]))
	return data


import matplotlib.ticker as ticker

def plot_data(x, y, headers, title):
	fig, ax = plt.subplots()
	#ax.scatter(x,y,color='b',linewidths=1)
	ax.plot(x,y,color='b')
	ax.set_xlabel(headers["x"])
	ax.set_ylabel(headers["y"])
	ax.set_title(title)

	figManager = plt.get_current_fig_manager()
	figManager.window.showMaximized()

	figure_filename = title + '.pdf'
	plt.savefig(figure_filename, bbox_inches='tight')
	f = os.path.dirname(os.path.realpath(__file__)) + "/" + figure_filename
	print("Saved figure to", f)

	plt.show()

# DETECT HORIZONTAL ASYMPTOTE APPROACHED FROM BELOW
def critical_temperature(data):
	freq = 1
	x = data["temperature"]#[ data["temperature"][i] for i in range(len(data["temperature"])) if i%freq == 0]
	y = data["voltage superconductor"]#[ data["voltage superconductor"][i] for i in range(len(data["voltage superconductor"])) if i%freq == 0]
	time = data["time"]
	asymptote = 10000
	for value in y:
		asymptote = min(asymptote, value)

	i = y.index(asymptote)

	Tc = x[i]
	tc = time[i]
	return Tc, tc

if __name__ == "__main__":
	filename = str(sys.argv[1])
	data = get_data(filename)

	plot_data(
		data["temperature"], 
		data["voltage superconductor"], 
		{
			"x":"Temperature (ºC)",
			"y":"Superconductor Voltage (V)"
		},
		"Superconductor Voltage VS Temperature",
		)
	plot_data(
		data["time"], 
		data["temperature"], 
		{
			"x":"Time (s)",
			"y":"Temperature (ºC)"
		},
		"Temperature VS Time",
		)
	plot_data(
		data["time"], 
		data["voltage superconductor"], 
		{
			"x":"Time (s)",
			"y":"Superconductor Voltage (V)"
		},
		"Superconductor Voltage VS Time",
		)
	Tc, tc = critical_temperature(data)
	print("The transition temperature Tc is:", Tc, "ºC, at t =", tc, "s")



