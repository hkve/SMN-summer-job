import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from band import Band
from JDOS import JDOS
from plots import plot_bands_and_JDOS, plot_bands, plot_integrated_density, plot_waterfall

def symmetric_parabolic_direct_gap(run=False):
	"""
	Direct band gap of 1eV
	Parabolic CB and CV, effective mass can be given as an argument of .parabolic 
	"""
	jdos = JDOS()

	filename = "direct_parabolic_1eV"

	if run:
		c = Band("c")
		v = Band("v")
		c.parabolic(effective_mass=0.5, E0=1, k_init=(0,1,3000), k0=0.5)
		v.parabolic(effective_mass=0.5, E0=0, k_init=(0,1,3000), k0=0.5)

		bands = [c,v]
		jdos.set_bands(bands)
		jdos.run(E_init=(0,7), q_init=(-1,1), n_E=1000, n_q=1000)
		jdos.save_data(filename, bands=True)

	else:		
		jdos.load_data(filename, bands=True)
		
	#jdos.map_to_abs()
	#plot_integrated_density(*jdos.integrated_density())
	Q, E, J = jdos.get_data()
	plot_integrated_density(*jdos.integrated_density())
	#plot_bands_and_JDOS(Q, E, J, jdos.get_bands(), JDOS_options={"smooth": 1})

def symmetric_indirect_gap(run=False):
	"""
	Same as above but now a indirect gap of 
	"""
	jdos = JDOS()

	filename = "indirect_parabolic_1eV"

	if run:
		c1 = Band("c")
		v1 = Band("v")

		c1.parabolic(effective_mass=0.5, E0=1, k_init=(0,1.5,1000), k0=0.8)
		v1.parabolic(effective_mass=0.5, E0=0, k_init=(0,1.5,1000), k0=0.4)

		bands = [c1, v1]

		jdos.set_bands(bands)
		jdos.run(E_init=(0,5), n_E = 100, n_q = 100)

		jdos.save_data(filename, bands=True)
	else: 
		jdos.load_data(filename, bands=True)

	print(jdos)
	#jdos.map_to_abs()
	Q, E, J = jdos.get_data()
	
	plot_bands_and_JDOS(Q, E, J, jdos.get_bands(), JDOS_options={"smooth": 1}, band_options={"ylim": (-2,2)})

def non_parabolic_direct_gap(run=False):
	"""
	Same as above but now a indirect gap of 
	"""
	jdos = JDOS()

	filename = "direct_non_parabolic_1eV"


	if run:
		c1 = Band("c")
		v1 = Band("v")

		c1.non_parabolic(alpha=0.7, effective_mass=0.5, E0=1, k_init=(0,1.5,1000), k0=0.8)
		v1.parabolic(effective_mass=0.5, E0=0, k_init=(0,1.5,1000), k0=0.4)

		bands = [c1, v1]

		jdos.set_bands(bands)
		jdos.run(E_init=(0,7), n_E = 500, n_q = 500, q_init=(-1.5,1.5))

		jdos.save_data(filename, bands=True)
	else: 
		jdos.load_data(filename, bands=True)

	print(jdos)

	Q, E, J = jdos.get_data()
	plot_bands_and_JDOS(Q, E, J, jdos.get_bands(), band_options={"smooth": 0.7, "ylim": (-2,2)})

def multiple_bands(run=False):
	jdos = JDOS()
	
	filename = "multiple_bands_low_res"

	if run:
		c1 = Band("c")
		c2 = Band("c")
		v1 = Band("v")	

		c1.parabolic(effective_mass=0.5, E0=1, k_init=(0,1.5,1000), k0=0.8)
		c2.parabolic(effective_mass=0.5, E0=1, k_init=(0,1.5,1000), k0=0.6)
		v1.parabolic(effective_mass=0.5, E0=0, k_init=(0,1.5,1000), k0=0.4)

		bands = [c1, c2,v1]

		jdos.set_bands(bands)
		jdos.run(E_init=(0,5), q_init=(-1.5,1.5), n_E=500, n_q=500)

		jdos.save_data(filename, bands=True)
	else:
		jdos.load_data(filename, bands=True)

	Q, E, J = jdos.get_data()
	
	print(jdos)
	plot_bands_and_JDOS(Q, E, J, jdos.get_bands(), JDOS_options={"smooth": 1}, band_options={"ylim": (-2,2)})
	


symmetric_parabolic_direct_gap(run=False)
#symmetric_indirect_gap(True)
#non_parabolic_direct_gap(run=True)
#multiple_bands(run=False)