from get_structure import load_structure
from get_bands import get_bands, make_band_objects
from plot_structure import plot_brillouin, plot_bandstructure
import numpy as np
import matplotlib.pyplot as plt

"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from JDOS import JDOS
from band import Band
from plots import plot_bands, plot_JDOS, plot_bands_and_JDOS, plot_integrated_density, plot_waterfall
"""

def jdos(bs, run=False):
	direction = "\Gamma-A"
	k, v, c = get_bands(bs, direction, n_val=3,n_con=1)
	bands = make_band_objects(k,v,c, interpolate=False, n_points=1500)

	filename = "SiC_GA"
	jdos = JDOS()

	if run:
		jdos.set_bands(bands)
		jdos.run(E_init=(2.5,10), q_init=(-0.6,0.6), n_E=500, n_q=500)# <- \Gamma-A
		#jdos.run(E_init=(2.5,10), q_init=(-1.3,1.3), n_E=500, n_q=500) #<- K-\Gamma
		jdos.save_data(filename)

	else:
		jdos.load_data(filename)
	
	print(jdos)
	
	plot_bands(bands)
	exit()
	d = direction.replace("-", " ")
	title = rf"${d}$ direction"
	Q, E, J = jdos.get_data()
	plot_JDOS(Q, E, J, JDOS_options={"smooth": 2.5, "title": title})
	#plot_bands_and_JDOS(Q, E, J, bands, JDOS_options={"smooth": 3})
	


if __name__ == "__main__":
	bs = load_structure("data/SiC.json")
	#bs = bs.apply_scissor(3.37)
	
	#jdos(bs, run=False)

	#plot_brillouin(bs)
	plot_bandstructure(bs, title="ZnO band structure")