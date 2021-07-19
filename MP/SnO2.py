import sys, os
from get_structure import load_structure
from get_bands import get_bands, make_band_objects
from plot_structure import plot_brillouin, plot_bandstructure

"""
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("not stuck")
from JDOS import JDOS
from band import Band
from plots import plot_bands, plot_JDOS, plot_bands_and_JDOS, plot_integrated_density, plot_waterfall
"""
if __name__ == "__main__":
	bs = load_structure("data/SnO2.json")

	k, v, c = get_bands(bs, "\Gamma-Z", 1,1)

	print(k)

	#plot_brillouin(bs)