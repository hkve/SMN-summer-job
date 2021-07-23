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
	show = []

	bg = []
	bg_std = []

	for i in range(len(filenames)):

		if not i in show:
			E, intensity = fit_spectrum.load_data(filenames[i])

			intensity = fit_spectrum.normalize(intensity)
			intensity_smooth = fit_spectrum.savgol_smooth(intensity, bin_windows[i])

			E_trim, intensity_trim, trim_idx = fit_spectrum.trim_data(trim_Es[i], E, intensity_smooth)
			fit_opt, fit_cov = curve_fit(fit_spectrum.fit_1_2, E_trim, intensity_trim)
			
			bg.append(fit_opt[0])
			bg_std.append(fit_cov[0,0])

			if plot:
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

if __name__ == "__main__":
	# 001
	"""
	filenames, bin_windows, trim_Es = read_config("spectrum_configs_001.txt")
	bg, bg_std = fit_spectrums(filenames, bin_windows, trim_Es, plot=False)
	save("001.txt", bg, bg_std)
	"""

	filenames, bin_windows, trim_Es = read_config("spectrum_configs_100.txt")
	bg, bg_std = fit_spectrums(filenames, bin_windows, trim_Es, plot=False)
	save("100.txt", bg, bg_std)
