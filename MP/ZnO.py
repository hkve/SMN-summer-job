import sys, os
from get_structure import load_structure
from get_bands import get_bands, make_band_objects

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from JDOS import JDOS
from band import Band
from plots import plot_bands, plot_bands_and_JDOS, plot_integrated_density, plot_waterfall

def plot(run=False):
	bs_ZnO = load_structure("data/ZnO.json")
	bs_ZnO = bs_ZnO.apply_scissor(3)

	k, v, c = get_bands(bs_ZnO, "\Gamma-A", n_val=5,n_con=3)
	bands = make_band_objects(k,v,c, interpolate=True, n_points=500)

	filename = "ZnO"
	jdos = JDOS()

	if run:
		jdos.set_bands(bands)
		jdos.run(E_init=(2,13), q_init=(-0.3,0.3), n_E=250, n_q=10)
		jdos.save_data(filename)

	else:
		jdos.load_data(filename)

	print(jdos)
	jdos.map_to_abs()
	plot_integrated_density(*jdos.integrated_density())

	#Q, E, J = jdos.get_data()
	#plot_bands_and_JDOS(Q, E, J, bands, JDOS_options={"smooth": 1})

plot(run=False)