import fit_spectrum
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
np.seterr(invalid="ignore")

def read_config(filename):
	filenames = []
	bin_windows = []
	trim_Es = []

	direction = 0
	temp = filename.replace(".", "_")
	for d in temp.split("_"):
		if d.isdigit():
			direction = d
	"""
	direction = filename.replace(".txt", "")
	direction = direction[-3:]
	"""

	with open(filename, "r") as f:
		
		f.readline()

		for line in f.readlines():
			line = line.split()
			filenames.append(f"SnO2_data/Text files for {direction} direction/{line[0]}")
			bin_windows.append(int(line[1]))
			trim_Es.append((float(line[2]), float(line[3])))

	return filenames, bin_windows, trim_Es

def fit_spectrums(filenames, bin_windows, trim_Es, plot=True):
	show = [10]

	bg = []
	bg_std = []

	for i in range(len(filenames)):
		E, intensity = fit_spectrum.load_data(filenames[i])

		intensity = fit_spectrum.normalize(intensity)
		intensity_smooth = fit_spectrum.savgol_smooth(intensity, bin_windows[i])

		E_trim, intensity_trim, trim_idx = fit_spectrum.trim_data(trim_Es[i], E, intensity_smooth)
		fit_opt, fit_cov = curve_fit(fit_spectrum.fit_1_2, E_trim, intensity_trim)
		
		bg.append(fit_opt[0])
		bg_std.append(fit_cov[0,0])

		if plot and i in show:
			print(f"{filenames[i]} ---> IDX = {i}")
			fig, ax = plt.subplots()
			ax.plot(E, intensity, c="gray")
			ax.plot(E, intensity_smooth, c="r")
			fit_spectrum.plot_fit(ax, fit_spectrum.plot_1_2, E, fit_opt, fit_cov, trim_idx, color="green")
			plt.show()

	if not plot:
		return np.array(bg), np.array(bg_std)
	else: 
		return (None,None)

def save(filename, bgs, stds):
	with open(f"{filename}", "w+") as file:
		for bg, std in zip(bgs, stds):
			file.write(f"{bg},{std}\n")

def plot_spectrums():

	directions = ["001", "100"]
	bz_direction = ["\Gamma Z", "\Gamma X"]
	d = -0.35

	fig, ax = plt.subplots(nrows=1, ncols=2)
	ax[0].set_ylabel("Intensity [arb. units]", fontsize=14)
	for i, direction in enumerate(directions):
		filenames, bin_windows, trim_Es = read_config(f"spectrum_configs_{direction}.txt")

		for j in range(len(filenames)):
			E, intensity = fit_spectrum.load_data(filenames[j])

			intensity = fit_spectrum.normalize(intensity)
			intensity_smooth = fit_spectrum.savgol_smooth(intensity, bin_windows[j])
			
			E_trim, intensity_trim, trim_idx = fit_spectrum.trim_data(trim_Es[j], E, intensity_smooth)
			fit_opt, fit_cov = curve_fit(fit_spectrum.fit_1_2, E_trim, intensity_trim)

			ax[i].plot(E, d*j+intensity, c="gray")
			ax[i].plot(E, d*j+intensity_smooth, c="r")

		ax[i].tick_params(axis='x', labelsize=12)
		ax[i].set_yticklabels([])
		ax[i].set_yticks([])
		ax[i].set_xlabel("Energy loss [eV]", fontsize=14)
		ax[i].set_title(f"{direction} direction " + rf"$({bz_direction[i]})$", fontsize=16)

	fig.tight_layout()
	plt.show()

if __name__ == "__main__":
	plot_spectrums()
	# 001
	"""
	filenames, bin_windows, trim_Es = read_config("spectrum_configs_001.txt")
	bg, bg_std = fit_spectrums(filenames, bin_windows, trim_Es, plot=False)
	save("001.txt", bg, bg_std)
	"""

	""" 100
	filenames, bin_windows, trim_Es = read_config("spectrum_configs_100.txt")
	bg, bg_std = fit_spectrums(filenames, bin_windows, trim_Es, plot=False)
	save("100.txt", bg, bg_std)
	"""