from band_gap_sketch import generate_band_gap, plot_J

import numpy as np
import matplotlib.pyplot as plt


def q_resolved_JDOS(k, valence, conducting, q_init=(0,5,100), E_init=(0,4,100)):
	tol = 0.1
	n_k = len(k)
	Q = np.linspace(*q_init)
	E = np.linspace(*E_init)

	Q_grid, E_grid = np.meshgrid(Q,E)
	J_grid = np.zeros_like(Q_grid, dtype=int)

	for i in range(n_k):
		for j in range(n_k):
			
			del_E = conducting[j]-valence[i]
			q = abs(k[j]-k[i])

			if np.min(abs(E-del_E)) < tol:
				E_idx = np.argmin(abs(E-del_E))
				Q_idx = np.argmin(abs(k-q))

				J_grid[E_idx, Q_idx] += 1

	return Q_grid, E_grid, J_grid


k, valence, conducting = generate_band_gap()
Q, E, J = q_resolved_JDOS(k, valence, conducting)

plot_J(Q, E, J)