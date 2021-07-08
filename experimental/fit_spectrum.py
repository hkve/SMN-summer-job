import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, lfilter
from scipy.optimize import curve_fit

def load_data(filename):
	E, intensity = [], []
	with open(filename, "r") as f: 	
		for line in f.readlines():
			line = line.replace(",", ".")
			line = line.split()
			E.append(float(line[0]))
			intensity.append(float(line[1]))

	return np.array(E), np.array(intensity)

def func(E, bandgap, A):
	return A*np.sqrt(E-bandgap)

def func_plot(E, bandgap, A):
	intensity = np.zeros_like(E)

	intensity[(E-bandgap)>0] = A*np.sqrt(E[(E-bandgap)>0]-bandgap)

	return intensity

def trim_data(trim, E, intensity):
	start = np.argmin(abs(trim[0]-E))
	end = np.argmin(abs(trim[1]-E))

	return E[start:end+1], intensity[start:end+1], (start, end)


def plot_fit(ax, E, fit_opt, fit_cov, trim_idx, color):
	bandgap, bandgap_coef = fit_opt[0], fit_cov[0,0]
	print(f"bandgap = {bandgap:.2f} eV, bangap coef = {bandgap_coef:.2e} eV")
	intensity = func_plot(E, *fit_opt)

	start, end = trim_idx
	zero = np.argmin(abs(fit_opt[0]-E))

	ax.plot(E[:zero], intensity[:zero], c="gray", ls="--", lw=2)
	ax.plot(E[zero:start+1], intensity[zero:start+1], c=color, ls="--", lw=2)
	ax.plot(E[start:end+1], intensity[start:end+1], c=color, lw=2)
	ax.plot(E[end:], intensity[end:], c=color, ls="--", lw=2)

def plot_data(E, intensity_smooth, fit_opt, fit_cov, trim_idx):
	fig, ax = plt.subplots()
	ax.plot(E, intensity_smooth, c="r")	

	plot_fit(ax, E, fit_opt, fit_cov, trim_idx, "green")
	
	ax.set_xlabel("Energy difference (eV)", fontsize=12)
	ax.set_ylabel("Norm intensity", fontsize=12)
	plt.show()

def normalize(intensity):
	return (intensity-np.min(intensity))/(np.max(intensity)-np.min(intensity))

#E, intensity = load_data("SnO2_data/Text files for 001 direction/0.1-0.2.msa")


smoothing_window = 31
order = 2

intensity_smooth = savgol_filter(intensity, window_length=smoothing_window, polyorder=order)
intensity_smooth = normalize(intensity_smooth)

E_trim, intensity_smooth_trim, trim_idx = trim_data((3,4), E, intensity_smooth)


fit_opt, fit_cov = curve_fit(func, E_trim, intensity_smooth_trim)

plot_data(E, intensity_smooth, fit_opt, fit_cov, trim_idx)

if __name__ == "__main__":
	E, intensity = load_data("SnO2_data/Text files for 001 direction/0-0.1 A.msa")
	