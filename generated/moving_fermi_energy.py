import sys, os
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from band import Band
from JDOS import JDOS
from plots import plot_JDOS

def find_cuts(k):
	tol = 1e-10
	dk = k[1]-k[0]

	idx = []

	for i in range(1, len(k)-1):	
		dk_front = k[i+1] - k[i]
		dk_back = k[i] - k[i-1]
		if abs(dk-dk_front) > tol or abs(dk-dk_back) > tol:
			idx.append(i)

	if len(idx) > 2:
		print("upsi in find_cuts")
		exit()
	else:
		start, end = np.sort(idx)
	return start, end

def plot_bands_move_fermi_energy(bands, efermi):
	fig, ax = plt.subplots()

	for band in bands:
		if band.band_type == "conducting":
			start, end = find_cuts(band.k)
			ax.plot(band.k[:start], band.E[:start], c="b")
			ax.plot(band.k[end:], band.E[end:], c="b")
		else:		
			ax.plot(band.k, band.E, c="b")

	plt.show()

def move_fermi_energy(efermi, bands):
	for band in bands:
		if band.band_type == "conducting":
			move_idx = np.where(band.E < efermi)
			
			E_move = band.E[move_idx]
			k_move = band.k[move_idx]

			band.E = np.delete(band.E, move_idx)
			band.k = np.delete(band.k, move_idx)

			band_move = Band("v")
			band_move.E = E_move
			band_move.k = k_move

			bands.append(band_move)				

	return bands, efermi

c1 = Band("c")
c2 = Band("c")
v1 = Band("v")	

c1.parabolic(effective_mass=0.5, E0=1, k_init=(0,1.5,1000), k0=0.8)
c2.parabolic(effective_mass=0.5, E0=1, k_init=(0,1.5,1000), k0=0.6)
v1.parabolic(effective_mass=0.5, E0=0, k_init=(0,1.5,1000), k0=0.4)

bands = [c1, v1]

bands, efermi = move_fermi_energy(1.1, bands)

plot_bands_move_fermi_energy(bands, efermi)
"""
jdos = JDOS()
jdos.set_bands(bands)
jdos.run(E_init=(0,5), q_init=(-1.1,1.1), n_E=250, n_q=250)

Q, E, J = jdos.get_data()


plot_JDOS(Q,E,J, JDOS_options={"smooth": 1})"""