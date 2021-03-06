from get_structure import load_structure
from get_bands import get_bands

import numpy as np
import matplotlib.pyplot as plt

from get_bands import get_bands
from plot_structure import plot_brillouin, plot_bandstructure
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from JDOS import JDOS
from band import make_band_objects
from plots import plot_bands, plot_JDOS, plot_bands_and_JDOS


def jdos(bs, run=False):
	direction = "\Gamma-Z"
	k, v, c = get_bands(bs, direction, n_val=8,n_con=1)
	bands = make_band_objects(k,v,c, interpolate=True, n_points=3000)

	filename = "SnO_GZ"
	jdos = JDOS()

	if run:
		k_max = np.max(k)
		jdos.set_bands(bands)
		jdos.run(E_init=(2.5,10), q_init=(-k_max,k_max), n_E=500, n_q=500)
		jdos.save_data(filename)

	else:
		jdos.load_data(filename)
	
	print(jdos)
	
	d = direction.replace("-", " ")
	title = rf"${d}$ direction"
	Q, E, J = jdos.get_data()
	plot_JDOS(Q, E, J, JDOS_options={"smooth": 2.5, "title": title})
	#plot_bands_and_JDOS(Q, E, J, bands, JDOS_options={"smooth": 3})


def plot_with_experimental(bs, direction, q_ranges,run=False): 
	bg_exp, bg_std = np.loadtxt(f"sno_bg/{direction}.txt", delimiter=",", unpack=True)

	bs = bs.apply_scissor(bg_exp[0])

	filename = ""
	sym_dir = ""
	q_max = 0
	if direction == "001":
		filename = f"sno2_dft_{direction}"
		sym_dir = "\Gamma-Z"
		q_max = 1 # Dosent really matter
	elif direction == "100":
		filename = f"sno2_dft_{direction}"
		sym_dir = "\Gamma-X"
		q_max = 0.6501188356086567 # Does matter
	else:
		print("Wrong direction, 001 or 100")
		exit()

	jdos = JDOS()
	
	if run:
		bs = bs.apply_scissor(bg_exp[0])
		k, v, c = get_bands(bs, sym_dir, 1,1)
		
		bands = make_band_objects(k,v,c,interpolate=True, n_points=3000)
		jdos.set_bands(bands)
		jdos.run(E_init=(2.5,10), q_init=(0,q_max), n_E=1000, n_q=500)

		jdos.save_data(filename)
	else:
		jdos.load_data(filename)

	jdos.mirror_bz()
	E, intesities = jdos.integrate_q(q_ranges)


	bg_dft = np.zeros_like(bg_exp)
	k = 0
	for i in range(intesities.shape[0]):
		non_zero_idx = 0
		for j in range(1, len(intesities[i,:])-1):
			if intesities[i,j] != 0 and intesities[i,j-1] == 0:
				bg_dft[k] = E[j]
				k += 1
				break



	k_mids = [r[0]+0.5*(r[1]-r[0]) for r in q_ranges]
	fig, ax = plt.subplots()
	
	ax.scatter(k_mids, bg_dft, label="Fitted DFT energies")
	ax.scatter(k_mids, bg_exp, label="Fitted EELS energies")	
	
	ax.set_xlabel(r"q " + r"$[??^{-1}]$", fontsize=14)
	ax.set_xticks(np.arange(0,k_mids[-1]+0.15,0.1))
	ax.tick_params(axis='x', labelsize=13)
	
	ax.set_ylabel(r"Energy difference [eV]", fontsize=14)
	ax.tick_params(axis='y', labelsize=13)
	
	sym_dir = sym_dir.replace("-", " ")
	ax.set_title(rf"{direction} direction (${sym_dir}$)", fontsize=15)
	ax.legend(fontsize=13)
	plt.tight_layout()
	plt.show()


if __name__ == "__main__":
	print("not stuck")
	bs = load_structure("data/SnO2.json")
	
	""" 001
	bs = bs.apply_scissor(3.6286753818126023)
	q_ranges = [(0,0.1),(0.1,0.2),(0.2,0.3),(0.3,0.4),(0.5,0.6),(0.7,0.8),(0.9,1.0)]
	plot_with_experimental(bs, "001", q_ranges, False)
	"""

	q_ranges = [(0,0.1),(0.1,0.2),(0.2,0.3),(0.4,0.5),(0.7,0.8),(0.9,1.0),(1.2,1.3)]
	plot_with_experimental(bs, "100", q_ranges, run=False)
	""" 100
	"""

	""" bs
	plot_bandstructure(bs, title=r"r-SnO$_2$ band structure")	
	"""

	#jdos(bs, run=False)