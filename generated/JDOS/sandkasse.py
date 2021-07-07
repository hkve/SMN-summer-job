from JDOS import JDOS
from plots import plot_JDOS, get_levels, JDOS_preprocessing

import matplotlib.pyplot as plt
import numpy as np

img = plt.imread("figures/schusterJDOS.png")
fig, ax = plt.subplots()
ax.imshow(img, extent=[0,1,0,1], interpolation="nearest")


#filename = "schuster_M_K_deg_test" 
filename = "schuster_M_K_low_res_test"
jdos = JDOS()
jdos.load_data(filename, bands=True)

jdos.map_to_abs()
Q, E, J = jdos.get_data()

q = np.linspace(0,1,Q.shape[1])
e = np.linspace(0,1,Q.shape[0])
Q, E = np.meshgrid(q,e)


J = JDOS_preprocessing(J, options={"smooth": 1})
J_max, J_min, n_levels = get_levels(J)

tol = 140
J[J<tol] = 0

cf = ax.contourf(Q, E, J, cmap="Greys", levels=np.linspace(J_min, J_max+1, n_levels, dtype=int), alpha=0.15)
#cb = fig.colorbar(cf, ax=ax)
ax.set_xlabel(rf"$|q|$"+" "+r"$[Å^{-1}]$", fontsize=12)
ax.set_ylabel(r"Energy difference $\Delta$E [eV]", fontsize=12)

x_ticks_loc = np.linspace(0,1,10)
x_ticks_vals = [str(round(i*0.1, 1)) for i in range(10)]

y_ticks_loc = np.linspace(0,1,11)
y_ticks_vals = [str(round(5.9+i*0.2, 1)) for i in range(11)]

ax.set_xticks(x_ticks_loc)
ax.set_xticklabels(x_ticks_vals)
ax.set_yticks(y_ticks_loc)
ax.set_yticklabels(y_ticks_vals)
#fig.savefig(fname="test.png", bbox_inches='tight', pad_inches=0, transparent=True)

plt.show()