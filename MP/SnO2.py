from get_structure import load_structure
from get_bands import get_bands

import numpy as np
import matplotlib.pyplot as plt

"""
from get_bands import get_bands
from plot_structure import plot_brillouin, plot_bandstructure
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from JDOS import JDOS
from Band import make_band_objects
from plots import plot_bands, plot_JDOS, plot_bands_and_JDOS


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


def plot_with_experimental(bs, direction): 
	bg, bg_std = np.loadtxt(f"sno_bg/{direction}.txt", delimiter=",", unpack=True)
	
	bs = bs.apply_scissor(bg[0])

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

	fig, ax = plt.subplots()
	ax.scatter(k_mids, E_dft, label="dft")
	ax.scatter(k_mids, E_exp, label="exp")	
	ax.set_xticks(np.linspace(0,1,11))
	ax.legend()
	plt.show()


if __name__ == "__main__":
	bs = load_structure("data/SnO2.json")

	plot_with_experimental(bs, "001")

