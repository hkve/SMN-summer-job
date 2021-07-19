import sys, os
import numpy as np
from pymatgen.electronic_structure.core import Spin
from get_structure import load_structure

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from band import Band

def check_valid_params(bs, branch, n_val, n_con, n_kpoints):
	branches = set()

	for i in range(n_kpoints):
		branches.add(bs.get_branch(i)[0]["name"])

	if not branch in branches:
		print(f"{branch = } is not a symmetry line in bs object, choose one of:")
		for available_branch in branches:
			print(f"{available_branch},", end="")
		exit()

	if n_val < 1:
		print(f"{n_val = } is not valid. Need at leaste 1 valence band")
		exit()
	if n_con < 1:
		print(f"{n_con = } is not valid. Need at leaste 1 conduction band")
		exit()

def get_branch_index(bs, branch, n_kpoints):
	for i in range(n_kpoints):
		branch_info = bs.get_branch(i)[0]

		if branch in branch_info["name"]:
			return (branch_info["start_index"], branch_info["end_index"])
	
def frac_to_cart(k, abc, angles):
	a, b, c = abc

	alpha, beta, gamma = np.deg2rad(angles)

	omega = a*b*c * np.sqrt(1-np.cos(alpha)**2 - np.cos(beta)**2 - np.cos(gamma)**2 + 2*np.cos(alpha)*np.cos(beta)*np.cos(gamma))
	
	M = np.array([
				[a, b*np.cos(gamma), c*np.cos(beta)],
				[0, b*np.sin(gamma), c*(np.cos(alpha-np.cos(beta)*np.cos(gamma))/np.cos(gamma))],
				[0,0,omega/(a*b*np.sin(gamma))]
				])

	for i in range(k.shape[0]):
		k[i] = np.dot(M,k[i])
	
	return k

def get_bands(bs, branch, n_val, n_con):
	"""	
	Extract a chosen number of bands from BandStructureSymmLine object 
	along a chosen symmetry line. 
	"""	
	n_kpoints = len(bs.kpoints)

	check_valid_params(bs, branch, n_val, n_con, n_kpoints)
	k_start, k_end = get_branch_index(bs, branch, n_kpoints)


	VBM_idx = bs.get_vbm()["band_index"][Spin.up]
	CBM_idx = bs.get_cbm()["band_index"][Spin.up]

	n_VBM, n_CBM = len(VBM_idx), len(CBM_idx)

	v_start, v_end, c_start, c_end = 0,0,0,0

	if not n_val == n_VBM:
		v_end = VBM_idx[-1]
		v_start = v_end - n_val + 1
	else:
		v_start, v_end = VBM_idx[0], VBM_idx[-1]
	
	if not n_con == n_CBM:
		c_start = CBM_idx[0]
		c_end = c_start + n_con - 1
	else:
		c_start, c_end = CBM_idx[-1], CBM_idx[0]

	kpoint_coords = np.zeros((k_end-k_start+1,3))
	#kpoint_degeneracy = np.zeros(k_end-k_start,dtype=int)


	val_energies = bs.bands[Spin.up][v_start:v_end+1,k_start:k_end+1]
	con_energies = bs.bands[Spin.up][c_start:c_end+1,k_start:k_end+1]

	for i, kpoint in enumerate(bs.kpoints[k_start:k_end+1]):
		kpoint_coords[i,:] = kpoint.frac_coords
		#kpoint_degeneracy[i] = bs.get_kpoint_degeneracy(kpoint.frac_coords) 

	abc = bs.lattice_rec.abc
	angles = bs.lattice_rec.angles
		
	kpoint_coords = frac_to_cart(kpoint_coords, abc, angles)
	

	kpoint_coords = kpoint_coords - kpoint_coords[0] 
	kpoint_coords = np.linalg.norm(kpoint_coords, axis=1)
	return kpoint_coords, val_energies, con_energies

def make_band_objects(k, v, c, interpolate=True, n_points=1000):
	n_v, n_c = v.shape[0], c.shape[0]
	bands = []

	for i in range(n_v):
		band = Band("v")
		band.E = v[i,:]
		band.k = k

		bands.append(band)

	for i in range(n_c):
		band = Band("c")
		band.E = c[i,:]
		band.k = k

		bands.append(band)

	for band in bands:
		band.interpolate(n_points)

	return bands


if __name__ == "__main__":
	bs = load_structure("data/ZnO.json")

	k,v,c = get_bands(bs, "\Gamma-A", 1,1)

	print(k)