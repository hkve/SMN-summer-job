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

def fit_1_2(E, bandgap, A):
	return A*np.sqrt(E-bandgap)

def fit_3_2(E, bandgap, A):
	return A*(E-bandgap)**1.5

def plot_1_2(E, bandgap, A):
	intensity = np.zeros_like(E)

	intensity[(E-bandgap)>0] = A*np.sqrt(E[(E-bandgap)>0]-bandgap)

	return intensity

def plot_3_2(E, bandgap, A):
	intensity = np.zeros_like(E)

	intensity[(E-bandgap)>0] = A*(E[(E-bandgap)>0]-bandgap)**1.5

	return intensity


def trim_data(trim, E, intensity):
	start = np.argmin(abs(trim[0]-E))
	end = np.argmin(abs(trim[1]-E))

	return E[start:end+1], intensity[start:end+1], (start, end)


def plot_fit(ax, func, E, fit_opt, fit_cov, trim_idx, color):
	bandgap, bandgap_coef = fit_opt[0], fit_cov[0,0]
	intensity = func(E, *fit_opt)

	start, end = trim_idx
	zero = np.argmin(abs(fit_opt[0]-E))

	print(f"bandgap = {bandgap:.2f} eV, bangap coef = {bandgap_coef:.2e} eV, on energy range = ({E[start]:.2f} eV,{E[end]:.2f} eV)")
	ax.plot(E[:zero], intensity[:zero], c="gray", ls="--", lw=2)
	ax.plot(E[zero:start+1], intensity[zero:start+1], c=color, ls="--", lw=2)
	ax.plot(E[start:end+1], intensity[start:end+1], c=color, lw=2, label=f"$E_g=${bandgap:.2f} eV")
	ax.plot(E[end:], intensity[end:], c=color, ls="--", lw=2)

def plot_data(E, intensity_smooth, fit_opt, fit_cov, trim_idx):
	fig, ax = plt.subplots()
	ax.plot(E, intensity_smooth, c="r")	

	
	
	ax.set_xlabel("Energy difference (eV)", fontsize=12)
	ax.set_ylabel("Norm intensity", fontsize=12)
	plt.show()

def normalize(intensity):
	return (intensity-np.min(intensity))/(np.max(intensity)-np.min(intensity))

#E, intensity = load_data("SnO2_data/Text files for 001 direction/0.1-0.2.msa")

def savgol_smooth(intensity, window_length, order=2):
	return savgol_filter(intensity, window_length=window_length, polyorder=order)



if __name__ == "__main__":
	E, intensity = load_data("SnO2_data/Text files for 001 direction/0.0-0.1.msa")
	
	intensity = normalize(intensity)
	intensity_smooth = savgol_smooth(intensity, 21)

	E_trim1, intensity_trim1, trim_idx1 = trim_data((3,4), E, intensity_smooth)
	fit_opt1, fit_cov1 = curve_fit(fit_1_2, E_trim1, intensity_trim1)
	
	E_trim2, intensity_trim2, trim_idx2 = trim_data((4.7,5.5), E, intensity_smooth)
	fit_opt2, fit_cov2 = curve_fit(fit_1_2, E_trim2, intensity_trim2)
	
	fig, ax = plt.subplots(nrows=1, ncols=2)
	
	ax[0].plot(E, intensity, c="r", label="Raw spectrum")
	ax[1].plot(E, intensity_smooth, c="r", label="Smoothed spectrum")	

	plot_fit(ax[1], plot_1_2, E, fit_opt1, fit_cov1, trim_idx1, "green")
	plot_fit(ax[1], plot_1_2, E, fit_opt2, fit_cov2, trim_idx2, "blue")

	ax[1].set_xlabel("Energy difference (eV)", fontsize=12)
	ax[0].set_xlabel("Energy difference (eV)", fontsize=12)
	ax[0].set_ylabel("Normalized intensity", fontsize=12)
	ax[0].legend()
	ax[1].legend(loc=2)
	plt.show()