from pymatgen.electronic_structure.plotter import BSPlotter
from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine
from get_structure import load_structure
import matplotlib.pyplot as plt

def plot_brillouin(bs):
	BSPlotter(bs).plot_brillouin()

def plot_bandstructure(bs, title=""):
	bsplot = BSPlotter(bs)
	bsplot.get_plot()

	ax = plt.gca()
	ax.set_title(title, fontsize=24)
	ax.set_xlabel("")
	ax.set_ylabel("Energy (eV)", fontsize=24)

	#ax.plot((), (), c="r", lw=4)

	ax.get_legend().remove()

	plt.show()

if __name__ == "__main__":
	#BandStructureSymmLine object: https://pymatgen.org/pymatgen.electronic_structure.bandstructure.html
	bs_ZnO = load_structure("data/ZnO.json")

	#bs_SnO2 = load_structure("data/SnO2.json")
	#bs_SnO2 = bs_SnO2.apply_scissor(new_band_gap=3) # Move CBM
	#print(bs_ZnO.structure)
	
	#plot_brillouin(bs_ZnO)
	#plot_bandstructure(bs_SnO2)