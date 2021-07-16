from get_bands import get_bands
from get_structure import load_structure
import numpy as np
import matplotlib.pyplot as plt


from plots import plot_JDOS

class JDOS:
	def __init__(self, E_int, q_int, dE, dq):
		self.E_min, self.E_max = E_int
		self.q_min, self.q_max = q_int

		self.dE = dE
		self.dq = dq

		n_E = int((self.E_max-self.E_min)/self.dE)
		n_q = int((self.q_max-self.q_min)/self.dq)
			
		E = np.linspace(self.E_min, self.E_max, n_E+1)
		q = np.linspace(self.q_min, self.q_max, n_q+1)

		self.q_grid, self.E_grid = np.meshgrid(q,E)
		self.J_grid = np.zeros_like(self.q_grid, dtype=int)

	def run(self, kpoints,deg, con, val):
		kpoints = kpoints - kpoints[0]
		kpoints = np.linalg.norm(kpoints, axis=1)

		n_points = kpoints.shape[0]
		n_con, n_val = con.shape[0], val.shape[0]

		for i in range(n_val):
			for j in range(n_con):
				for k in range(n_points):
					for l in range(n_points):
						E_ = con[j,l]-val[i,k]
						q_ = kpoints[l] - kpoints[k]
						if not self.q_min < q_ < self.q_max or not self.E_min < E_ < self.E_max:
							continue
						else:
							q_idx = (q_ - self.q_min)/self.dq
							E_idx = (E_ - self.E_min)/self.dE

							q_idx = int(round(q_idx, 0))
							E_idx = int(round(E_idx, 0))
							self.J_grid[E_idx, q_idx] += deg[k]*deg[l]

		return self.q_grid, self.E_grid, self.J_grid
bs_ZnO = load_structure("data/ZnO.json")
bs_ZnO = bs_ZnO.apply_scissor(3)
k,k_deg, v, c = get_bands(bs_ZnO, "\Gamma-M", n_val=5,n_con=5)
	
jdos = JDOS(E_int=(1,10), q_int=(-1,1), dE=0.1, dq=0.1)
Q, E, J = jdos.run(k,k_deg,c,v)

plot_JDOS(Q, E, J, JDOS_options={"smooth": 0.1})