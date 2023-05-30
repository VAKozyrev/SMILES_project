import numpy as np

from Bond import Bond
from Atom import Atom

class Structure:

    def __init__(self, atoms={}, bonds={}):
        self.atoms = atoms
        self.bonds = bonds

    def __str__(self):
        string = f'Structure: {self.atoms}, {self.bonds}'
        return string

    def get_atoms(self):
        return list(self.atoms.values())

    def get_bonds(self):
        return list(self.bonds.values())

    def get_atom(self, atom_number):
        return self.atoms[atom_number]

    def get_bond(self, bond_number):
        return self.bonds[bond_number]

    def add_atom(self, atom: Atom):
        self.atoms[atom.number] = atom

    def add_bond(self, bond: Bond):
        self.bonds[bond.number] = bond
        self.get_atom(bond.atom1).add_bond(bond.atom2, bond.bond_order)
        self.get_atom(bond.atom2).add_bond(bond.atom1, bond.bond_order)

    def set_hydrogens(self):
        for atom_nr in self.atoms:
            self.atoms[atom_nr].set_valency()
            self.atoms[atom_nr].set_hydrogens()

    def get_connection_table(self):
        a = [i for i in range(0, len(self.atoms) + 1, 1)]
        matrix = np.zeros((len(self.atoms) + 1, len(self.atoms) + 1))
        array = np.array(a)
        matrix[0] += array
        matrix[:, 0] += array
        for atom in self.get_atoms():
            for i in atom.bonds:
                matrix[atom.number][i] = atom.bonds[i]

        return matrix

