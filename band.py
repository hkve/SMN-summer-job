import numpy as np
from scipy.constants import physical_constants
from scipy.interpolate import CubicSpline

# Placks constant times c
hbar_c = (197.326979 * 10) # [eV Å]

# Electron mass
m0 = physical_constants["electron mass energy equivalent in MeV"][0]
m0 *= 1e6 # [eV/c^2]

class Band:
	def __init__(self, band_type):
		
		if band_type == "valence" or band_type == "val" or band_type == "v":
			self.band_prefactor = -1
			self.band_type = "valence"
		elif band_type == "conducting" or band_type == "con" or band_type == "c":
			self.band_prefactor = 1
			self.band_type = "conducting"
		else:
			print(f"'{band_type}', is not a valid band type. Choose 'valence' or 'conducting'")
			exit()

		self.k = None
		self.E = None
		self.alpha = None
		self.effective_mass = None


	def parabolic(self, effective_mass=0.5, E0=0, k0=0, k_init=(-0.5,0.5,1000)):
		# Get wave vector linspace
		self.effective_mass = effective_mass
		self.k = np.linspace(*k_init) # [Å^-1]
		m = m0 * effective_mass 

		self.E = self.band_prefactor*(hbar_c*(self.k-k0))**2 / (2*m) + E0 # [eV]

	def non_parabolic(self, effective_mass=0.5, E0=0, k0=0, alpha=0.5, k_init=(-0.5,0.5,1000)):
		self.effective_mass = effective_mass
		self.k = np.linspace(*k_init)
		m = m0 * effective_mass 
		self.alpha = alpha

		nominator = np.sqrt(1+(2*self.alpha)*(hbar_c*(self.k-k0))**2 / m) 
		denominator = 2*self.alpha

		self.E = self.band_prefactor*(nominator-1)/denominator + E0

	def load_single_file(self, filename):
		data = np.loadtxt(filename, delimiter=",", dtype=np.float)

		self.k = data[:,0]
		self.E = data[:,1]

	def interpolate(self, n, random=False):
		cs = CubicSpline(self.k, self.E)

		if random:
			self.k = np.random.uniform(self.k[0], self.k[-1], n)
			self.k = np.sort(self.k)
		else:
			self.k = np.linspace(self.k[0], self.k[-1], n)
		
		self.E = cs(self.k)

	def add_gaussian_noice(self, sigma):
		noise = np.random.normal(0, sigma, self.E.shape)
		self.E += noise

if __name__ == "__main__":
	band1 = Band("val")
	band1.parabolic(effective_mass=0.1, E0 = 1)

def make_band_objects(k, v, c, interpolate=True, n_points=1000):
	n_v, n_c = v.shape[0], c.shape[0]
	bands = []

	for i in range(n_v):
		band = Band("v")
		band.E = v[i,:]
		band.k = k

		bands.append(band)

	for i in range(n_c):
		band = Band("c")
		band.E = c[i,:]
		band.k = k

		bands.append(band)

	for band in bands:
		band.interpolate(n_points)

	return bands
