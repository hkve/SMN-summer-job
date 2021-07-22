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
	k, v, c = get_bands(bs, direction, n_val=1,n_con=1)
	bands = make_band_objects(k,v,c, interpolate=True, n_points=1500)

	filename = "SnO_GZ"
	jdos = JDOS()

	if run:
		jdos.set_bands(bands)
		jdos.run(E_init=(2.5,10), q_init=(0,1.3), n_E=500, n_q=500)
		jdos.save_data(filename)

	else:
		jdos.load_data(filename)
	
	print(jdos)
	
	d = direction.replace("-", " ")
	title = rf"${d}$ direction"
	Q, E, J = jdos.get_data()
	#plot_JDOS(Q, E, J, JDOS_options={"smooth": 2.5, "title": title})
	plot_bands_and_JDOS(Q, E, J, bands, JDOS_options={"smooth": 3})

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

"""
def plot_with_experimental(bs, direction, run=False): 
	bg_exp, bg_std = np.loadtxt(f"sno_bg/{direction}.txt", delimiter=",", unpack=True)
	bg_dft = np.zeros_like(bg_exp)

	bs = bs.apply_scissor(bg_exp[0])

	filename = ""
	sym_dir = ""
	if direction == "001":
		filename = f"sno2_dft_{direction}"
		sym_dir = "\Gamma-Z"
	elif direction == "100":
		filename = f"sno2_dft_{direction}"
		sym_dir = "\Gamma-X"
	else:
		print("Wrong direction, 001 or 100")
		exit()

	jdos = JDOS()
	
	if run:
		bs = bs.apply_scissor(bg_exp[0])
		k, v, c = get_bands(bs, sym_dir, 1,1)
		bands = make_band_objects(k,v,c,interpolate=True, n_points=3000)
		jdos.set_bands(bands)
		jdos.run(E_init=(2,12), q_init=(0,1.3), n_E=1000, n_q=500)

		jdos.save_data(filename)
	else:
		jdos.load_data(filename)

	q_ranges = [(0,0.1),(0.1,0.2),(0.2,0.3),(0.3,0.4),(0.5,0.6),(0.7,0.8),(0.9,1.0)]
	E, intesities = jdos.integrate_q(q_ranges)

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
	ax.scatter(k_mids, bg_dft, label="dft")
	ax.scatter(k_mids, bg_exp, label="exp")	
	ax.set_xticks(np.linspace(0,1,11))
	ax.legend()
	plt.show()


if __name__ == "__main__":
	print("not stuck")
	bs = load_structure("data/SnO2.json")
	
	""" 001
	q_ranges = [(0,0.1),(0.1,0.2),(0.2,0.3),(0.3,0.4),(0.5,0.6),(0.7,0.8),(0.9,1.0)]
	plot_with_experimental(bs, "001", False)
	"""

	q_ranges = [(0,0.1),(0.1,0.2),(0.2,0.3),(0.3,0.4),(0.5,0.6)]
	plot_with_experimental(bs, "100", True)
	k, v, c = get_bands(bs, "\Gamma-X",1,1)
	print(k[0], k[-1], k.shape)


