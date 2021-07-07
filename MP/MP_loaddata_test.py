from matminer.data_retrieval.retrieve_MP import MPDataRetrieval # Not needed?
from pymatgen.ext.matproj import MPRester
from pymatgen.electronic_structure.plotter import BSPlotter
from pymatgen.electronic_structure.bandstructure import BandStructure, BandStructureSymmLine

import json as json

#df_mp = MPDataRetrieval("QWSjiHanJdjCjxyr").get_dataframe(criteria='Si', properties=['band_structure'])
#print(df_mp)

def plot_brillouin(bs):
	BSPlotter(bs).plot_brillouin()

def plot_bandstructure(bs):
	BSPlotter(bs).get_plot().show() 

def save_structure(bs, filename):
	if not filename.endswith(".json"):
		print("File must be saved in json format")

	with open(filename, "w+") as f:
		json.dump(bs.as_dict(), f)

def load_structure(filename):
	if not filename.endswith(".json"):
		print("File must be saved in json format")

	with open(filename, "r") as f:
		d = json.load(f)
		bs = BandStructureSymmLine.from_dict(d)

	return bs
mpr = MPRester("QWSjiHanJdjCjxyr")
bs = mpr.get_bandstructure_by_material_id("mp-2133")
"""
"""
#save_structure(bs, "test.json")
#bs = load_structure("test.json")


plot_brillouin(bs)
plot_bandstructure(bs)
"""
#bs is BandStructure object: https://pymatgen.org/pymatgen.electronic_structure.bandstructure.html

# reciprocal lattice  primitive wavevectors for the reciprocal lattice? w/ 2*pi coef 
print(bs.lattice_rec) 

# number of bands
print(bs.nb_bands)
"""
"""
kpoints = bs.kpoints
print(kpoints[1].cart_coords)
"""

