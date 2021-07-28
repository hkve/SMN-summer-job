from get_structure import load_structure
from get_bands import get_bands
from plot_structure import plot_brillouin, plot_bandstructure
import numpy as np

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from JDOS import JDOS
from band import Band, make_band_objects
from plots import plot_bands, plot_JDOS, plot_bands_and_JDOS

def jdos(bs, run=False):
	print("Not stuck")
	direction = "K-\Gamma"
	k, v, c = get_bands(bs, direction, n_val=8,n_con=1)
	bands = make_band_objects(k,v,c, interpolate=True, n_points=3000)

	filename = "ZnO_KG"
	jdos = JDOS()

	if run:
		k_max = np.max(k)
		jdos.set_bands(bands)
		jdos.run(E_init=(2.5,10), q_init=(-k_max,k_max), n_E=500, n_q=500)# <- \Gamma-A
		#jdos.run(E_init=(2.5,10), q_init=(-1.3,1.3), n_E=500, n_q=500) #<- K-\Gamma
		jdos.save_data(filename)

	else:
		jdos.load_data(filename)
	
	print(jdos)
	
	d = direction.replace("-", " ")
	title = rf"${d}$ direction"
	Q, E, J = jdos.get_data()
	plot_JDOS(Q, E, J, JDOS_options={"smooth": 2.5, "title": title})
	#plot_bands_and_JDOS(Q, E, J, bands, JDOS_options={"smooth": 3})
	


if __name__ == "__main__":
	bs = load_structure("data/ZnO.json")
	bs = bs.apply_scissor(3.37)
	

	jdos(bs, run=True)
	#plot_brillouin(bs)
	#plot_bandstructure(bs, title="ZnO band structure")