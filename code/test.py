from code.Molecule import Molecule
from code.errors import StructureError
from Smiles import Smiles


molecule = Molecule('S=1(=NC2=C(C(=O)N1)S(=O)(=O)C3=CC=CC=C23)(C)C')
print(molecule.structure.atoms[1].valency)
print(molecule.structure.atoms[1].explicit_hydrogens)
print(molecule.structure.atoms[1].number_of_bonds)
print(molecule.get_bonds())

#print(Smiles.parse_square_brackets('[N+]'))
