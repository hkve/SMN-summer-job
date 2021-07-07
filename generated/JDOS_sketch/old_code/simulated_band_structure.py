# Generate real space crystal model
from pyeels import Crystal
import numpy as np
from pyeels.atom import Atom
from pyeels.orbital import Orbital
from pyeels.eels import EELS

myCrystal = Crystal(lattice=np.eye(3))
myAtom = Atom(number=0,position=[0,0,0])
myAtom.add_orbital(Orbital(label="s", onsite=0))
myCrystal.add_atom(atom=myAtom)

# Create parabolic bands in reciprocal space
from pyeels import ParabolicBand
reci = ParabolicBand(myCrystal)

reci.set_grid(mesh=31) # Number of k-points in each dimension

# Parabolic valence band
reci.set_parabolic(effective_mass=[-0.5, -0.5, -0.5], 
                   energy_offset=0, 
                   k_center=[0,0,0], 
                   wave=np.array([0,0.02])
                  )
		 
# Parabolic conduction band
reci.set_parabolic(effective_mass=[ 0.5,  0.5,  0.5], 
                   energy_offset=1, 
                   k_center=[0,0,0],
                   wave=np.array([0,1])
                  )

# Calculate EELS on the parabolic bands
from pyeels import EELS

mySystem = EELS(myCrystal)
mySystem.temperature = 0    # Absolute zero
mySystem.fermienergy = 0.5  # Placing the fermi level at center of the band gap


mySystem.set_meta(
	name="My test sample", 
	authors=["Author1", "Author2"], 
	title="myCrystal", 
	notes="This model is just an example." 
	)

# The q-resolution of the scattering cross section
# no argument correspond to the density of the k-grid in Brillouin Zone
mySystem.set_diffractionzone()

mySignal = mySystem.calculate_eels_multiproc(energyBins=np.linspace(0,4,200), smearing=0.05, max_cpu=4)
					    
#HyperSpy visuailzation
mySignal.plot()
