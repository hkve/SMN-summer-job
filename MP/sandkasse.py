from pymatgen.electronic_structure.core import Spin
from get_structure import load_structure
import numpy as np
import matplotlib.pyplot as plt

bs_ZnO = load_structure("data/ZnO.json")


energies = bs_ZnO.bands[Spin.up] # Get energy bands

cbm_band_idx = bs_ZnO.get_cbm()["band_index"][Spin.up] # Get index of band(s) located at conduction band maximum
vbm_band_idx = bs_ZnO.get_vbm()["band_index"][Spin.up] # Get index of band(s) located at valence band maximum

bs_ZnO.get_kpoint_degeneracy(bs_ZnO.kpoints[10].frac_coords) # check degeneracy of kpoint!!!!

print(bs_ZnO.get_branch(0)) # Can be usefull, takes kpoint index and returns what symmetry line it corresponds to. 
							 # Takes intersections into account (thus belonging to multiple branches)
exit()


coords = np.zeros((169,3))

for i, kpoint in enumerate(bs_ZnO.kpoints):
	coords[i,:] = kpoint.frac_coords

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.scatter(coords[:,0],coords[:,1],coords[:,2], c="b")
ax.scatter(0,0,0, c="r")

plt.show()

"""
m = np.inf
for i in cbm_band_idx:
	for j in vbm_band_idx:
		cb = energies[i,:]
		vb = energies[j,:]
	
		e = np.min(cb-vb)

		if e < m:
			m = e

for kpoint, e in zip(bs_ZnO.kpoints, energies[10,:]):
	kx, ky, kz = kpoint.frac_coords
	print(f"kx = {kx:.2f} ,ky = {ky:.2f}, kz = {kz:.2f}, E = {e}")
"""