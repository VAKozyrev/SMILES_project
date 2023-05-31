from code.errors import StructureError

class Atom:

    molecular_weights = {'H': 1.00797, 'B': 10.81, 'C': 12.011, 'N': 14.0067,
                         'O': 15.9994, 'F': 19.00, 'Si': 28.09, 'P': 30.97,
                         'S': 32.06, 'Cl': 35.5, 'Br': 79.90, 'I': 126.90,
                         'Se': 78.96, 'Te': 127.60, 'As': 74.9216}

    atoms_valencies = {'C': [4], 'N': [3], 'O': [2], 'B': [3], 'H': [1], 'S': [2, 4, 6],
                       'P': [3, 5], 'Br': [1], 'I': [1], 'Cl': [1], 'F': [1],
                       'Se': [2, 4], 'Si': [4], 'Te': [2, 4], 'As': [3]}

    def __init__(self, symbol: str, atom_number: int, chiral_mark='', charge=0, explicit_hydrogens=-1, explicit_mass=0):
        self.bonds = {}  # Dictionary of bonded atoms {atom_number: bond_order}
        self.number_of_bonds = 0

        self.number = atom_number
        self.symbol = symbol
        self.chiral_mark = chiral_mark
        self.charge = charge
        self.explicit_hydrogens = explicit_hydrogens
        self.explicit_mass = explicit_mass
        self.aromaticity = False           # Aromaticity is checked in self.get_element

        self.element = self.get_element()
        self.mass = self.get_mass()
        self.hydrogens = 0                 # Hydrogens are set after building the whole molecule
        self.valency = 0

    def __repr__(self):
        string = f"Atom('{self.symbol}', {self.number}, chiral_mark='{self.chiral_mark}', charge={self.charge}, " \
                 f"expliсit_hydrogens={self.explicit_hydrogens})"
        return string

    def __str__(self):
        string = f'{self.number}:{self.symbol}, charge: {self.charge}, valency: {self.valency}, hydrogens: {self.hydrogens}'
        return string

    def __eq__(self, atom):
        if type(atom) == Atom:
            return self.number == atom.number
        else:
            return False

    def __hash__(self):
        return self.number

    def get_element(self):
        if self.symbol.islower():
            self.aromaticity = True
            self.symbol = self.symbol.upper()
        return self.symbol

    def get_mass(self):
        if self.explicit_mass:
            return self.explicit_mass
        else:
            return Atom.molecular_weights[self.element]

    def set_hydrogens(self):
        if self.explicit_hydrogens != -1:
            self.hydrogens = self.explicit_hydrogens
            for i in Atom.atoms_valencies[self.element]:
                if i == self.hydrogens + self.number_of_bonds - self.charge and self.element != 'B':
                    self.valency = i
                if i == self.hydrogens + self.number_of_bonds + self.charge and self.element == 'B':
                    self.valency = i
            if self.valency == 0:
                raise StructureError('wrong_valency', atom=self.element)
        else:
            for i in Atom.atoms_valencies[self.element]:
                if i >= self.number_of_bonds - self.charge:
                    self.valency = i
                    break
            if self.valency == 0:
                raise StructureError('wrong_valency', atom=self.element)
            self.hydrogens = self.valency - self.number_of_bonds + self.charge
            if self.hydrogens < 0:
                raise StructureError('wrong_valency', atom=self.element)

    def add_bond(self, atom_number, bond_order):
        self.bonds[atom_number] = bond_order
        self.number_of_bonds += bond_order
