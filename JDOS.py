from band import Band

import os as os
import numpy as np

class JDOS:
	def __init__(self):
		self.conducting = []
		self.valence = []

		self.Q_grid = None
		self.E_grid = None
		self.J_grid = None

	def set_bands(self, bands):
		if not hasattr(bands, "__iter__"):
			print("At leaste 2 bands are needed to preform JDOS")
			exit()

		for band in bands:
			if band.band_type == "valence":
				self.valence.append(band)
			else: 
				self.conducting.append(band)
	
	
	def default_q_resolution(self):
		q_min, q_max = 0,0

		for val in self.valence:
			for con in self.conducting:
				q_max_proposal = con.k[-1] - val.k[0]

				if q_max_proposal > q_max:
					q_max = q_max_proposal

		return (-q_max, q_max)

	def default_E_resolution(self):
		E_min, E_max = 0,0 # Change E_min to non-zero value?

		for val in self.valence:
			for con in self.conducting:
				E_max_proposal = np.max(con.E) - np.min(val.E)
				E_min_proposal = np.min(con.E) - np.max(val.E)

				if E_max_proposal > E_max:
					E_max = E_max_proposal
					
				if E_min_proposal < E_min:
					E_min = E_min_proposal

		return (E_min, E_max)
	
	def bin_window(self, val, con, J_dims):
		n_val = len(val.E)
		n_con = len(con.E)

		J_grid = np.zeros(J_dims, dtype=int)

		q_min = self.q_min #- self.dq/2
		q_max = self.q_max #+ self.dq/2
		E_min = self.E_min #- self.dE/2
		E_max = self.E_max #+ self.dE/2


		for i in range(n_val):
			for j in range(n_con):
				
				q = con.k[j] - val.k[i]
				delE = con.E[j] - val.E[i]
				
				if not q_min < q < q_max or not E_min < delE < E_max:
					continue
				else:
					q_idx = (q-self.q_min)/self.dq
					delE_idx = (delE-self.E_min)/self.dE

					q_idx = int(round(q_idx, 0))
					delE_idx = int(round(delE_idx, 0))

					J_grid[delE_idx, q_idx] += 1
		

		return J_grid

	def run(self, q_init=None, E_init=None, n_q=100, n_E=100):
		# q_init=(0,1,500), E_init=(0,5,500)	
		if q_init == None:
			q_init = self.default_q_resolution()
		if E_init == None:
			E_init = self.default_E_resolution()

		self.q_min, self.q_max = q_init
		self.E_min, self.E_max = E_init

		self.n_q = n_q
		self.n_E = n_E

		Q = np.linspace(self.q_min, self.q_max, self.n_q+1)
		E = np.linspace(self.E_min, self.E_max, self.n_E+1)
		
		self.dq = (self.q_max-self.q_min)/self.n_q
		self.dE = (self.E_max-self.E_min)/self.n_E

	
		self.Q_grid, self.E_grid = np.meshgrid(Q, E)
		self.J_grid = np.zeros_like(self.Q_grid, dtype=int)

		for val in self.valence:
			for con in self.conducting:

				J_grid = self.bin_window(val, con, self.J_grid.shape)

				self.J_grid += J_grid


	def integrated_density(self):
		q_lin = np.linspace(self.q_min, self.q_max, self.n_q+1)
		q_hits = np.sum(self.J_grid, axis=0)

		E_lin = np.linspace(self.E_min, self.E_max, self.n_E+1)
		E_hits = np.sum(self.J_grid, axis=1)

		q_hits = q_hits
		E_hits = E_hits

		return q_lin, q_hits, E_lin, E_hits

	def map_to_abs(self):
		if self.Q_grid is None or self.E_grid is None or self.J_grid is None:
			print("No data loaded. Load data or run JDOS")
			exit()

		self.n_q = self.n_q//2
		self.q_min = 0

		negative_J_grid = self.J_grid[:, :self.n_q+1]
		positive_J_grid = self.J_grid[:, self.n_q:]
		
		self.J_grid = positive_J_grid + np.flip(negative_J_grid, axis=1)
				
		Q = np.linspace(self.q_min, self.q_max, self.J_grid.shape[1])
		E = np.linspace(self.E_min, self.E_max, self.J_grid.shape[0])

		self.Q_grid, self.E_grid = np.meshgrid(Q, E)


	def print_bands(self, bands):
		to_print = f"{len(bands)} {bands[0].band_type} bands\n"
		to_print += "\t\tM_eff\tAlpha\n"
		for i, band in enumerate(bands): 
			to_print += f"{i+1}\t\t{band.effective_mass}\t\t{band.alpha}\n" 

		return to_print

	def __str__(self):
		to_print = ""
		to_print += f"Momentum resolution:\tq_min = {self.q_min:.2f}\t\tq_max={self.q_max:.2f}\tdq = {self.dq:.2E} \n"
		to_print += f"Energy resolution:\t\tE_min = {self.E_min:.2f}\t\tE_max={self.E_max:.2f}\tdE = {self.dE:.2E} \n"
		
		if len(self.conducting) > 0 and len(self.valence) > 0:
			to_print += self.print_bands(self.conducting)
			to_print += self.print_bands(self.valence)

		return to_print


	def save_band(self, band, file):
		file.write(f"{band.effective_mass},{band.alpha}\n")
		for e in band.E[:-1]:
			file.write(f"{e},")
		file.write(f"{band.E[-1]}\n")

		for k in band.k[:-1]:
			file.write(f"{k},")
		file.write(f"{band.k[-1]}\n")

	def load_bands(self, bands_type, filename):
		with open(filename+"_"+bands_type+".txt", "r") as file:
			n_bands = int(file.readline())
			
			for i in range(n_bands):
				band = Band(bands_type)
				info_line = file.readline().strip().split(",")
				
				if info_line[0] != "None":
					band.effective_mass = float(info_line[0])
				else:
					band.effective_mass = None
				if info_line[1] != "None":
					band.alpha = float(info_line[1])
				else:
					band.alpha = None

				band.E = np.array(file.readline().strip().split(","), dtype=float)
				band.k = np.array(file.readline().strip().split(","), dtype=float)

				if bands_type == "conducting":
					self.conducting.append(band)
				else:
					self.valence.append(band)


	def save_data(self, filename, bands=False):
		if not "data" in os.listdir():
			os.mkdir("data")
		
		filename = "data/" + filename

		np.savez(filename, Q=self.Q_grid, E=self.E_grid, J=self.J_grid)
		
		if bands:
			with open(filename+"_conducting.txt", "w+") as file:
				file.write(f"{len(self.conducting)}\n")
				for band in self.conducting:
					self.save_band(band, file)

			with open(filename+"_valence.txt", "w+") as file:
				file.write(f"{len(self.valence)}\n")
				for band in self.valence:
					self.save_band(band, file)

	def load_data(self, filename, bands=False):
		filename = "data/" + filename
		
		data = np.load(filename+".npz")
		self.Q_grid = data["Q"]
		self.E_grid = data["E"]
		self.J_grid = data["J"]

		self.q_min, self.q_max, self.n_q = np.min(self.Q_grid), np.max(self.Q_grid), self.Q_grid.shape[1]
		self.E_min, self.E_max, self.n_E = np.min(self.E_grid), np.max(self.E_grid), self.E_grid.shape[0]

		self.n_q -= 1
		self.n_E -= 1

		self.dq = (self.q_max-self.q_min)/(self.n_q-1)
		self.dE = (self.E_max-self.E_min)/(self.n_E-1)
		
		if bands:
			self.conducting = []
			self.valence = []

			self.load_bands("conducting", filename)
			self.load_bands("valence", filename)

	def get_data(self):
		return self.Q_grid, self.E_grid, self.J_grid

	def get_bands(self):
		return self.conducting + self.valence


if __name__ == "__main__":
	c1 = Band("c")
	v1 = Band("v")

	c1.parabolic(E0=1)
	v1.parabolic(E0=0)

	bands = [c1, v1]
	
	from plots import plot_bands_and_JDOS

	jdos = JDOS()
	jdos.set_bands(bands)
	jdos.run(q_init=(-2,2), E_init=(0,4), n_q=100, n_E=100)
	Q, E, J = jdos.get_data()

	plot_bands_and_JDOS(Q, E, J, bands, JDOS_options={"smooth": 1})