import numpy as np
import matplotlib.pyplot as plt

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from get_structure import load_structure
from plot_structure import plot_brillouin, plot_bandstructure
from JDOS import JDOS




if __name__ == "__main__":
	bs = load_structure("data/SiC.json")
	
	plot_brillouin(bs)
	plot_bandstructure(bs, title="")