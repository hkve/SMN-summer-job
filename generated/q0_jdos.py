import matplotlib.pyplot as plt
import numpy as np 
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from JDOS import JDOS
from band import Band
from plots import plot_bands_and_JDOS

def func(E, bandgap, A):
	return A*(E-bandgap)**(-0.5)

def plot_func(E, bandgap, A):
	intensity = np.zeros_like(E)

	intensity[(E-bandgap)>0] = A*np.sqrt(E[(E-bandgap)>0]-bandgap)

	return intensity

def trim_data(trim, E, intensity):
	start = np.argmin(abs(trim[0]-E))
	end = np.argmin(abs(trim[1]-E))

	return E[start:end+1], intensity[start:end+1], (start, end)

def normalize(intensity):
	return (intensity-np.min(intensity))/(np.max(intensity)-np.min(intensity))


def preform_jdos(run=False):
	jdos = JDOS()

	filename = "test_dos"

	if run:
		c = Band("c")
		v = Band("v")

		k_init = (-0.5,1.5,3000)
		c.parabolic(effective_mass=0.5, E0=1, k_init=k_init, k0=0.5)
		v.parabolic(effective_mass=0.5, E0=0, k_init=k_init, k0=0.5)

		bands = [c,v]

		jdos.set_bands(bands)
		jdos.run(E_init=(0,7), q_init=(-1,1), n_E=1000, n_q=1000)

		jdos.save_data(filename, bands=True)

	else:
		jdos.load_data(filename, bands=True)

	return jdos

def preform_fit(jdos):
	jdos.map_to_abs()
	#jdos.J_grid = JDOS_preprocessing(jdos.J_grid, {"smooth": 2})
	Q, E, J = jdos.get_data()
	E, J = E[:,0], J[:,0]
	J[0] *= 2

	print(jdos)
	J = normalize(J)
	J = gaussian_filter(J, sigma=1.3)

	fig, ax = plt.subplots()

	dE = E[1]-E[0]
	E_trim, J_trim, trim_idx = trim_data((1+dE, 7-dE), E, J)
	fit_opt, fit_cov = curve_fit(func, E_trim, J_trim)

	print(fit_opt, np.diag(fit_cov))

	ax.plot(E, J, lw=3, c="gray", label="Smoothed spectrum")
	ax.plot(E_trim, func(E_trim, *fit_opt), c="r", lw=2, label="1D JDOS")
	ax.set(ylim=(0,np.max(J)+0.05))
	ax.set_xlabel("Energy difference [eV]", fontsize=12)
	ax.set_ylabel("Normalized intensity [arb. units]", fontsize=12)
	ax.legend(fontsize=12)
	plt.show()

jdos = preform_jdos(False)
preform_fit(jdos)