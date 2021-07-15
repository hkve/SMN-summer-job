import numpy as np
from band_gap_generator import Band
from plots import plot_bands, plot_JDOS

def JDOS_new(con_k, con_E, val_k, val_E, q_init, delE_init):
	q_min, q_max, n_q = q_init
	delE_min, delE_max, n_delE = delE_init

	dq = (q_max-q_min)/n_q
	dE = (delE_max-delE_min)/n_delE
	n_q_half = n_q//2

	q_lin = np.linspace(q_min, q_max, n_q+1)
	E_lin = np.linspace(delE_min, delE_max, n_delE+1)
	q_grid, delE_grid = np.meshgrid(q_lin, E_lin)
	J_grid = np.zeros_like(q_grid)

	con_n = len(con_k)
	val_n = len(val_k)

	print(q_min, q_max, dq)
	print(delE_min, delE_max, dE)
	#exit()

	for i in range(val_n):
		for j in range(con_n):
			q = con_k[j] - val_k[i]
			delE = con_E[j] - val_E[i]
			
			if not q_min < q < q_max or not delE_min < delE < delE_max:
				continue
			else:
				q_idx = (q-q_min)/dq 
				delE_idx = (delE-delE_min)/dE 

				q_idx = int(round(q_idx, 0))
				delE_idx = int(round(delE_idx, 0)) 

				J_grid[delE_idx, q_idx] += 1

	return q_grid, delE_grid, J_grid


c = Band("c")
v = Band("v")

c.parabolic(E0=1, k_init=(-1,1,500))
v.parabolic(E0=0, k_init=(-1,1,500))


E, Q, J = JDOS_new(c.k,c.E,v.k,v.E,(-2,2,100), (0,4,100))

#plot_JDOS(E, Q, J, options={"smooth": 1})
