import sys, os
from get_structure import load_structure
from get_bands import get_bands, make_band_objects
from plot_structure import plot_brillouin, plot_bandstructure

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("not stuck")
from JDOS import JDOS
from band import Band
from plots import plot_bands, plot_JDOS, plot_bands_and_JDOS, plot_integrated_density, plot_waterfall

def jdos(bs, run=False):
	direction = "\Gamma-A"
	k, v, c = get_bands(bs, direction, n_val=7,n_con=2)
	bands = make_band_objects(k,v,c, interpolate=False, n_points=1500)

	filename = "ZnO_GA"
	jdos = JDOS()

	
	if run:
		jdos.set_bands(bands)
		jdos.run(E_init=(2.5,10), q_init=(-0.6,0.6), n_E=500, n_q=500)
		#jdos.run(E_init=(2.5,10), q_init=(-1.3,1.3), n_E=500, n_q=500) <- K-\Gamma
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
	bs_ZnO = load_structure("data/ZnO.json")
	bs_ZnO = bs_ZnO.apply_scissor(3.37)
	
	jdos(bs_ZnO, run=False)

	#plot_brillouin(bs_ZnO)
	#plot_bandstructure(bs_ZnO, title="ZnO band structure")