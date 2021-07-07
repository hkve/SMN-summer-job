import numpy as np


def q_resolved_JDOS(k, valence, conducting, E_init=(0,25,100)):
    n_E, n_k = E_init[-1], len(k)
    E = np.linspace(*E_init)

    J_grid = np.zeros((n_E, n_k), dtype=int)
    Q_grid = np.tile(k, (n_k, 1))
    E_grid = np.tile(E.T, (n_E, 1)).T

    E_grid = E_grid[::-1,:]


    for i in range(n_k):
        for j in range(n_k):
            del_E = conducting[j] - valence[i]
            q = abs(k[j] - k[i])
                
            E_idx = np.argmin(abs(E-del_E))
            Q_idx = np.argmin(abs(k-q))

            J_grid[-E_idx, Q_idx] += 1

    return Q_grid, E_grid, J_grid
