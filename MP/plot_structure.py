from pymatgen.electronic_structure.plotter import BSPlotter
from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine
from get_structure import load_structure

def plot_brillouin(bs):
	BSPlotter(bs).plot_brillouin()

def plot_bandstructure(bs):
	BSPlotter(bs).get_plot().show() 

if __name__ == "__main__":
	#BandStructureSymmLine object: https://pymatgen.org/pymatgen.electronic_structure.bandstructure.html
	bs_ZnO = load_structure("data/ZnO.json")

	#bs_SnO2 = load_structure("data/SnO2.json")
	#bs_SnO2 = bs_SnO2.apply_scissor(new_band_gap=3) # Move CBM
	
	plot_brillouin(bs_ZnO)

	#plot_bandstructure(bs_SnO2)