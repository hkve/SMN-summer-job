from pymatgen.electronic_structure.plotter import BSPlotter
from pymatgen.electronic_structure.bandstructure import BandStructure, BandStructureSymmLine
from get_structure import load_structure

def plot_brillouin(bs):
	BSPlotter(bs).plot_brillouin()

def plot_bandstructure(bs):
	BSPlotter(bs).get_plot().show() 

if __name__ == "__main__":
	#bs_ZnO is BandStructure object: https://pymatgen.org/pymatgen.electronic_structure.bandstructure.html
	#bs_ZnO = load_structure("data/ZnO.json", sym=True)
	bs_SnO2 = load_structure("data/SnO2.json", sym=True)

	plot_brillouin(bs_SnO2)