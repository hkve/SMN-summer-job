import fit_spectrum
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
np.seterr(invalid="ignore")

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

def fit_spectrums(filenames, bin_windows, trim_Es, plot=True):
	skips = [10]

	bg = []
	bg_std = []

	for i in range(len(filenames)):

		if not i in skips:
			E, intensity = fit_spectrum.load_data(filenames[i])

			intensity = fit_spectrum.normalize(intensity)
			intensity_smooth = fit_spectrum.savgol_smooth(intensity, bin_windows[i])

			E_trim, intensity_trim, trim_idx = fit_spectrum.trim_data(trim_Es[i], E, intensity_smooth)
			fit_opt, fit_cov = curve_fit(fit_spectrum.fit_1_2, E_trim, intensity_trim)
			
			bg.append(fit_opt[0])
			bg_std.append(fit_cov[0,0])

			if plot:
				print(filenames[i])
				fig, ax = plt.subplots()
				ax.plot(E, intensity, c="gray")
				ax.plot(E, intensity_smooth, c="r")
				fit_spectrum.plot_fit(ax, fit_spectrum.plot_1_2, E, fit_opt, fit_cov, trim_idx, color="green")
				plt.show()

	if not plot:
		return np.array(bg), np.array(bg_std)

filenames, bin_windows, trim_Es = read_config("spectrum_configs_001.txt")
bg, bg_std = fit_spectrums(filenames, bin_windows, trim_Es, plot=False)



fig, ax = plt.subplots()
ax.plot(bg, c="r")
ax.set(ylim=(0,5))
plt.show()
"""
E, intensity = fit_spectrum.load_data("SnO2_data/Text files for 001 direction/0.5-0.6.msa")
intensity = fit_spectrum.normalize(intensity)
intensity = fit_spectrum.savgol_filter(intensity, 101, 2)
#4.4,5.2
E_trim, intensity_trim, trim_idx = fit_spectrum.trim_data((8.8,10), E, intensity)
fit_opt, fit_cov = fit_spectrum.curve_fit(fit_spectrum.fit_3_2, E_trim, intensity_trim)

fig, ax = plt.subplots()
fit_spectrum.plot_fit(ax, fit_spectrum.plot_3_2, E, fit_opt, fit_cov, trim_idx, color="green")
ax.plot(E,intensity)
ax.set(ylim=(0,1))
plt.show()
#E_trim, intensity_trim, trim_idx = trim_data(())

"""