from get_structure import load_structure
from get_bands import get_bands, make_band_objects
from plot_structure import plot_brillouin, plot_bandstructure
import numpy as np
import matplotlib.pyplot as plt


import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from JDOS import JDOS
from band import Band
from plots import plot_bands, plot_JDOS, plot_bands_and_JDOS, plot_integrated_density, plot_waterfall

print("not stuck")

if __name__ == "__main__":
	print("not stuck")
	bs = load_structure("data/SnO2.json")
	bs = bs.apply_scissor(3.7)

	k, v, c = get_bands(bs, "\Gamma-Z", 1,1)
	
	n_k = len(k)
	
	k_mids = np.array([0.05,0.15,0.25,0.35,0.55,0.75,0.95])
	mids_idx = []
	for mids in k_mids:
		mids_idx.append(np.argmin(abs(k-mids)))
	
	E_dft = []
	E_exp = np.array([3.5005739,3.56703504, 4.47391524, 5.66235156, 5.91432263, 7.5108972, 10.52755403])
	for i in mids_idx:
		E_dft.append(c[0,i]-v[0,i])

	E_dft = np.array(E_dft)

	plt.plot(E_dft)
	plt.plot(E_exp)	
	plt.show()