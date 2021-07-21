from get_structure import load_structure
from get_bands import get_bands, make_band_objects
from plot_structure import plot_brillouin, plot_bandstructure
import numpy as np
import matplotlib.pyplot as plt

"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from JDOS import JDOS
from plots import plot_bands, plot_JDOS, plot_bands_and_JDOS, plot_integrated_density, plot_waterfall


def jdos(bs, run=False):
	direction = "\Gamma-A"
	k, v, c = get_bands(bs, direction, n_val=3,n_con=1)
	bands = make_band_objects(k,v,c, interpolate=False, n_points=1500)

	filename = "SnO_GA"
	jdos = JDOS()

	if run:
		jdos.set_bands(bands)
		jdos.run(E_init=(2.5,10), q_init=(-0.6,0.6), n_E=500, n_q=500)
		jdos.save_data(filename)

	else:
		jdos.load_data(filename)
	
	print(jdos)
	
	plot_bands(bands)
	exit()
	d = direction.replace("-", " ")
	title = rf"${d}$ direction"
	Q, E, J = jdos.get_data()
	plot_JDOS(Q, E, J, JDOS_options={"smooth": 2.5, "title": title})
	#plot_bands_and_JDOS(Q, E, J, bands, JDOS_options={"smooth": 3})
	

"""
if __name__ == "__main__":
	print("not stuck")
	bs = load_structure("data/SnO2.json")
	bs = bs.apply_scissor(3.4505739)

	k, v, c = get_bands(bs, "\Gamma-Z", 1,1)
	
	n_k = len(k)
	
	k_mids = np.array([0.05,0.15,0.25,0.35,0.55,0.75,0.95])
	mids_idx = []
	for mids in k_mids:
		mids_idx.append(np.argmin(abs(k-mids)))
	
	E_dft = []
	E_exp = np.array([3.5005739,3.83, 4.47391524, 4.71, 5.91432263, 7.20, 7.44])
	for i in mids_idx:
		E_dft.append(c[0,i]-v[0,i])

	E_dft = np.array(E_dft)

	plt.scatter(k_mids, E_dft, label="dft")
	plt.scatter(k_mids, E_exp, label="exp")	
	plt.legend()
	plt.show()
