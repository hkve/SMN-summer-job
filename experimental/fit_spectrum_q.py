import fit_spectrum
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def read_config(filename):
	filenames = []
	bin_windows = []
	trim_Es = []

	direction = filename.replace(".txt", "")
	direction = direction[-3:]
	with open(filename, "r") as f:
		
		f.readline()

		for line in f.readlines():
			line = line.split()
			filenames.append(f"SnO2_data/Text files for {direction} direction/{line[0]}")
			bin_windows.append(int(line[1]))
			trim_Es.append((float(line[2]), float(line[3])))

	return filenames, bin_windows, trim_Es

filenames, bin_windows, trim_Es = read_config("spectrum_configs_001.txt")

skips = [0,1,2]

for i in range(len(filenames)):

	if i in skips:
		E, intensity = fit_spectrum.load_data(filenames[i])

		intensity = fit_spectrum.normalize(intensity)
		intensity_smooth = fit_spectrum.savgol_smooth(intensity, bin_windows[i])

		E_trim, intensity_trim, trim_idx = fit_spectrum.trim_data(trim_Es[i], E, intensity_smooth)
		fit_opt, fit_cov = curve_fit(fit_spectrum.fit_1_2, E_trim, intensity_trim)

		print(filenames[i])
		fig, ax = plt.subplots()
		ax.plot(E, intensity, c="gray")
		ax.plot(E, intensity_smooth, c="r")
		fit_spectrum.plot_fit(ax, fit_spectrum.plot_1_2, E, fit_opt, fit_cov, trim_idx, color="green")
		plt.show()
