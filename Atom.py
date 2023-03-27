from errors import StructureError

class Atom:
    elements = {'H': 'hydrogen', 'Li': 'lithium', 'B': 'boron', 'C': 'carbon', 'N': 'nitrogen',
                'O': 'oxygen', 'F': 'fluorine', 'Si': 'silicon', 'P': 'phosphorus', 'S': 'sulfur',
                'Cl': 'chlorine', 'As': 'arsenic', 'Se': 'selenium', 'Br': 'bromine', 'I': 'iodine',
                'Te': 'tellurium'}

    elements_aromatic = {'b': 'boron', 'c': 'carbon', 'n': 'nitrogen', 'o': 'oxygen', 'p': 'phosphorus',
                         's': 'sulfur', 'se': 'selenium', 'as': 'arsenic', 'te': 'tellurium', 'si': 'silicon'}

    molecular_weights = {'hydrogen': 1.00797, 'boron': 10.81, 'carbon': 12.011, 'nitrogen': 14.0067,
                         'oxygen': 15.9994, 'fluorine': 19.00, 'silicon': 28.09, 'phosphorus': 30.97,
                         'sulfur': 32.06, 'chlorine': 35.5, 'bromine': 79.90, 'iodine': 126.90,
                         'selenium': 78.96, 'tellurium': 127.60, 'arsenic': 74.9216}

    atoms_valencies = {'carbon': 4, 'nitrogen': 3, 'oxygen': 2, 'boron': 3, 'hydrogen': 1, 'sulfur': 2,
                       'phosphorus': 3, 'bromine': 1, 'iodine': 1, 'chlorine': 1, 'fluorine': 1,
                       'selenium': 2, 'silicon': 4, 'tellurium': 2, 'arsenic': 3}

    def __init__(self, symbol: str, atom_number: int, chiral_mark='', charge=0, explicit_hydrogens=0, explicit_mass=0):
        self.bonds = {}  #Dictionary of bonded atoms {atom_number: bond_order}
        self.number_of_bonds = 0
        self.aromaticity = False

        self.number = atom_number
        self.symbol = symbol
        self.chiral_mark = chiral_mark
        self.charge = charge
        self.explicit_hydrogens = explicit_hydrogens
        self.explicit_mass = explicit_mass

        self.get_element()
        self.get_mass()
        self.get_valency()
        self.get_hydrogens()

    def __repr__(self):
        string = f"Atom('{self.symbol}', {self.number}, chiral_mark='{self.chiral_mark}', charge={self.charge}, " \
                 f"expliсit_hydrogens={self.explicit_hydrogens})"
        return string

    def __str__(self):
        string = f'{self.number}:{self.symbol}{self.chiral_mark}'
        if self.charge > 0:
            charge_string = '+'
            string += charge_string + str(abs(self.charge))
        if self.charge < 0:
            charge_string = '-'
            string += charge_string + str(abs(self.charge))
        return string

    def __eq__(self, atom):
        if type(atom) == Atom:
            return self.number == atom.number
        else:
            return False

    def __hash__(self):
        return self.number

    def get_element(self):
        if self.symbol in Atom.elements:
            self.element = Atom.elements[self.symbol]
        elif self.symbol in Atom.elements_aromatic:
            self.element = Atom.elements_aromatic[self.symbol]
            self.aromaticity = True
        else:
            raise StructureError('unknown_element')

    def get_valency(self):
        if self.element == 'sulfur':
            if self.number_of_bonds == 4:
                self.valency = 4
            elif self.number_of_bonds == 6:
                self.valency = 6
            else:
                self.valency = 2
        else:
            self.valency = Atom.atoms_valencies[self.element]

    def get_mass(self):
        if self.explicit_mass != 0:
            self.mass = self.explicit_mass
        else:
            self.mass = Atom.molecular_weights[self.element]

    def get_hydrogens(self):
        if self.explicit_hydrogens != 0:
            self.hydrogens = self.explicit_hydrogens
        else:
            self.hydrogens = self.valency - self.number_of_bonds + self.charge

    def add_bond(self, atom_number, bond_order):
        self.bonds[atom_number] = bond_order
        self.number_of_bonds += bond_order

        self.get_valency()
        self.get_hydrogens()
