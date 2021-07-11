from pymatgen.ext.matproj import MPRester
from pymatgen.electronic_structure.bandstructure import BandStructure, BandStructureSymmLine

import json as json

def save_structure(bs, filename):
	"""
	Takes pymatgen BandStructure/BandStructureSymmLine object and save to json
	"""
	if not filename.endswith(".json"):
		print("File must be saved in json format")

	with open(filename, "w+") as f:
		json.dump(bs.as_dict(), f)

def load_structure(filename, sym=False):
	"""
	Load bandstructure from json and return either BandSructure or BandStructureSymmLine  
	"""
	if not filename.endswith(".json"):
		print("File must be saved in json format")

	with open(filename, "r") as f:
		d = json.load(f)

		if sym:
			bs = BandStructureSymmLine.from_dict(d)
		else:
			bs = BandStructure.from_dict(d)
	
	return bs


if __name__ == "__main__":
	with open("api_key.txt") as f: API_KEY = f.readline()

	mpr = MPRester(API_KEY)
	bs_ZnO = mpr.get_bandstructure_by_material_id("mp-2133")
	bs_SnO2 = mpr.get_bandstructure_by_material_id("mp-856")

	save_structure(bs_ZnO, "data/ZnO.json")
	save_structure(bs_SnO2, "data/SnO2.json")





