from pymatgen.electronic_structure.core import Spin

from get_structure import load_structure


bs_ZnO = load_structure("data/ZnO.json")


print(bs_ZnO.bands[Spin.up].shape)
print(bs_ZnO.kpoints[0])