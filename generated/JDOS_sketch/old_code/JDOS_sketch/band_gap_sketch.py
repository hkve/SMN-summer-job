import numpy as np
import matplotlib.pyplot as plt

def band(k, a, k0, E0):
    return a*(k-k0)**2 + E0

def generate_band_gap(k_init=(0,5,100),valence_init=(-1,1,1), conducting_init=(1,1,3)):
    k = np.linspace(*k_init)
    k_start, k_end = k_init[0], k_init[1]

    valence = band(k, *valence_init)
    conducting = band(k, *conducting_init)

    min_E = conducting_init[2] - valence_init[2]
    min_q = conducting_init[1]-valence_init[1]

    indirect = True
    info_str = ""

    if min_q == 0:
        indirect = False

    if indirect:
        info_str += f"Indirect band gap\nEnergy displacement = {min_E}, Momentum displacement = {min_q}"
    else:
        info_str += f"Direct band gap\nEnergy displacement = {min_E}" 

    print(info_str)

    return k, valence, conducting

def q_resolved_JDOS(k, valence, conducting, q_init=(0,5,100), E_init=(0,4,100), tol=0.1):
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
                Q_idx = np.argmin(abs(Q-q))

                J_grid[E_idx, Q_idx] += 1

    return Q_grid, E_grid, J_grid

def plot_band_gap(k, valence, conducting):
    y_max = 2*np.min(conducting-valence)        

    val_min_idx = np.argmax(valence)
    con_max_idx = np.argmin(conducting)
    arr_start = np.array([k[val_min_idx], valence[val_min_idx]])
    arr_diff = np.array([k[con_max_idx], conducting[con_max_idx]]) - arr_start

    fig, ax = plt.subplots()
    ax.plot(k, valence, c="k")
    ax.plot(k, conducting, c="k")
    
    ax.set(xlim=(k[0], k[-1]), ylim=(0,y_max), xlabel="k", ylabel="E")
    ax.grid()   

    ax.arrow(arr_start[0], arr_start[1], arr_diff[0], arr_diff[1], color="r",  head_width=0.1, length_includes_head=True)

    plt.show()


def plot_J(Q, E, J):
    fig, ax = plt.subplots()
    cf = ax.contourf(Q, E, J, cmap="jet")
    fig.colorbar(cf, ax=ax)

    ax.set(xlabel=r"$|q|=|k_1-k_0|$", ylabel="E")

    plt.show()



if __name__ == "__main__":
    # Direct band gap with E = 2
    """
    k, valence, conducting = generate_band_gap()   

    plot_band_gap(k, valence, conducting)

    Q, E, J = q_resolved_JDOS(k, valence, conducting)
    plot_J(Q, E, J)
    """

    # Indirect band gap

    # steepness, centering, constant
    conducting_init = (1,3,4)  
    valence_init = (-1.5,1,1)

    # k_min, k_max, n_k
    k_init = (0,5,1000)

    k, valence, conducting = generate_band_gap(k_init=k_init, valence_init=valence_init, conducting_init=conducting_init)

    #plot_band_gap(k, valence, conducting)

    Q, E, J = q_resolved_JDOS(k, valence, conducting, E_init=(0,10,500), tol=0.1)
    #plot_J(Q, E, J)