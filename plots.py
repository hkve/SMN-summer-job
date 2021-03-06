from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np

def ax_options(ax, options):
	if "xlim" in options.keys():
		ax.set(xlim=options["xlim"])
	if "ylim" in options.keys():
		ax.set(ylim=options["ylim"])
	if "dx" in options.keys():
		start, end = ax.get_xlim()
		ax.xaxis.set_ticks(np.arange(start, end, options["dx"]))
	if "dy" in options.keys():
		start, end = ax.get_ylim()
		ax.xaxis.set_ticks(np.arange(start, end, options["dy"]))
	if "title" in options.keys():
		ax.set_title(options["title"], fontsize=16)

def JDOS_preprocessing(J, options):
	if "smooth" in options.keys():
		J = gaussian_filter(J, options["smooth"])

	return J

def get_levels(J):
	J_max, J_min = np.max(J), np.min(J)
	n_levels = J_max-J_min + 1
	if n_levels > 200:
		n_levels = 200

	return J_max, J_min, n_levels

def plot_bands(bands, scatter=False, options={}):
	if not hasattr(bands, '__iter__'):
		bands = [bands]

	fig, ax = plt.subplots()

	for band in bands:
		if scatter:
			ax.scatter(band.k, band.E, c="b")
		else:
			ax.plot(band.k, band.E, c="b")

	ax_options(ax, options)

	ax.set(xlabel=r"$\vec{k}$"+" "+r"$[Å^{-1}]}$", ylabel=r"$E(\vec{k})$"+" "+r"$eV$")
	
	plt.show()

def plot_JDOS(Q, E, J, JDOS_options={}):
	fig, ax = plt.subplots()
	fig.set_size_inches(10,8)

	J = JDOS_preprocessing(J, JDOS_options)

	xlab = "q"
	if np.min(Q) > 0:
		xlab = "|q| "

	J_max, J_min, n_levels = get_levels(J)

	cf = ax.contourf(Q, E, J, levels=np.linspace(J_min, J_max, n_levels, dtype=np.int))
	cbar = fig.colorbar(cf, ax=ax)

	ax_options(ax, JDOS_options)

	cbar.ax.tick_params(labelsize=14) 
	ax.set_xlabel(rf"${xlab}$"+" "+r"$[Å^{-1}]$", fontsize=16)
	ax.set_ylabel(r"Energy difference E [eV]", fontsize=16)
	for tick in ax.xaxis.get_major_ticks(): tick.label.set_fontsize(14) 
	for tick in ax.yaxis.get_major_ticks(): tick.label.set_fontsize(14) 

	fig.tight_layout()
	plt.show()

def plot_bands_and_JDOS(Q, E, J, bands, JDOS_options={}, band_options={}):
	if not hasattr(bands, '__iter__'):
		bands = [bands]
	
	J = JDOS_preprocessing(J, JDOS_options)

	xlab = "|q| "
	if np.min(Q) < 0:
		xlab = "q "

	J_max, J_min, n_levels = get_levels(J)

	fig = plt.figure(constrained_layout=True, figsize=(10,6))
	spec = gridspec.GridSpec(nrows=1, ncols=2, width_ratios=[1,0.4], figure=fig)
	ax1 = fig.add_subplot(spec[0])
	ax2 = fig.add_subplot(spec[1])

	cf = ax1.contourf(Q, E, J, levels=np.linspace(J_min, J_max+1, n_levels, dtype=np.int))
	cbar = fig.colorbar(cf, ax=ax1)
	cbar.ax.tick_params(labelsize=12) 

	ax1.set_xlabel(rf"${xlab}$"+" "+r"$[Å^{-1}]$", fontsize=20)
	ax1.set_ylabel(r"Energy difference [eV]", fontsize=20)
	ax1.tick_params(axis='x', labelsize=14)
	ax1.tick_params(axis='y', labelsize=14)

	for band in bands:
		ax2.plot(band.k, band.E, c="b")

	ax2.set_xlabel(r"$k$"+" "+r"$[Å^{-1}]}$", fontsize=20)
	ax2.set_ylabel(r"$\epsilon(k)$"+" "+"[eV]", fontsize=20)
	ax2.tick_params(axis='x', labelsize=14)
	ax2.tick_params(axis='y', labelsize=14)

	ax2.grid()


	ax_options(ax1, JDOS_options)
	ax_options(ax2, band_options)

	plt.show()

def plot_integrated_density(q_lin, q_hits, E_lin, E_hits, q_options={}, E_options={}):
	fig, ax = plt.subplots(nrows=1, ncols=2)

	ax[0].plot(q_lin, q_hits)
	ax[1].plot(E_lin, E_hits)

	ax[0].set_title("Momentum transfere")
	ax[0].set_xlabel(r"$q [Å]^{-1}$", fontsize=12)
	ax[0].set_ylabel("Intensity (a.u.)", fontsize=12)

	ax[1].set_title("Energy transfere")
	ax[1].set_xlabel(r"E [eV]$", fontsize=12)

	ax[0].ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
	ax[1].ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
	ax_options(ax[0], q_options)
	ax_options(ax[1], E_options)

	plt.show()


def plot_waterfall(Q, E, J, q_points=np.arange(0, 1, 0.1), dq_lines=0.05):
	# !!!! split at halfway points!!!

	q_points = np.array(q_points)
	q_points = np.append(q_points, [q_points[-1]+q_points[1]])

	n_q, n_E = Q.shape[1], E.shape[0]
	n_lines = q_points.shape[0]
	
	dq_lines_idx = np.argmin(abs(Q[0]-dq_lines))
	q_points_idx = np.zeros_like(q_points, dtype=int)

	#J = JDOS_preprocessing(J, options={"smooth": 1})

	for i, q_point in enumerate(q_points):
		q_points_idx[i] = np.argmin(abs(Q[0]-q_point))


	instensities = np.zeros(shape=(n_lines-1, n_E), dtype=int) 

	for i in range(n_lines-1):
		start, end = q_points_idx[i], q_points_idx[i+1]
		if start > dq_lines:
			start -= dq_lines_idx
		if not i == n_lines-2:
			end -= dq_lines_idx
			
		instensities[i] = np.sum(J[:,start:end], axis=1)

	E = E[:,0]
	
	fig, ax = plt.subplots()
	for i in range(n_lines-1):
		non_zero_idx = instensities[i]!=0
		ax.plot(E[non_zero_idx], instensities[i, non_zero_idx], label=f"q = {q_points[i]:.1f}")

	ax.set_xlabel(r"E [eV]", fontsize=12)
	ax.set_ylabel("Intensity", fontsize=12)
	plt.legend()
	plt.show()
if __name__ == "__main__":
	pass