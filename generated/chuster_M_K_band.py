
def load_bands(filename, band_type, n):
	bands = []
	for i in range(1,n+1):
		band = Band(band_type)

		band.load_single_file(f"{filename}_{band_type}{i}.csv")

		bands.append(band)

	return bands

def interpolate_bands(bands, n, random=False):
	for band in bands:
		band.interpolate(n, random)

def add_noise(bands, sigma):
	for band in bands:
		band.add_gaussian_noice(sigma)

def plot_schuster_M_K(run=False):
	filename = "schuster_M_K_random_sample"

	# schuster_M_K_random_sample -> high energy and momentum res with 3000 points for each band
	# schuster_M_K -> 

	jdos = JDOS()
	if run:
		path = "data_from_img/schuster_M_K/schuster_M_K"
		con_bands = load_bands(path, "c", 2)
		val_bands = load_bands(path, "v", 2)

		bands = con_bands + val_bands

		interpolate_bands(bands, 3000, random=True)
		#add_noise(bands, 0.1)

		jdos.set_bands(bands)
		jdos.run(E_init=(5.9, 8), n_E=500, q_init=(-0.9,0.9), n_q = 500)

		jdos.save_data(filename, bands=True)
	else:
		jdos.load_data(filename, bands=True)
		bands = jdos.get_bands()


	jdos.map_to_abs()
	Q, E, J = jdos.get_data()
	
	print(jdos)
	
	#plot_waterfall(Q, E, J, [0.1,0.5,0.7])
	plot_JDOS(Q, E, J,JDOS_options={"smooth": 1})
	#plot_integrated_density(*jdos.integrated_density())


if __name__ == "__main__":
	import sys, os
	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	from band import Band
	from JDOS import JDOS

	from plots import plot_bands_and_JDOS, plot_JDOS, plot_bands, plot_integrated_density, plot_waterfall

	plot_schuster_M_K(run=False) 