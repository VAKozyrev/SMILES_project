class Bond:

    def __init__(self, bond_number: int, atom1: int, atom2: int, bond_order: int, chirality=''):
        self.number = bond_number
        self.atom1 = atom1
        self.atom2 = atom2
        self.bond_order = bond_order

    def __str__(self):
        return f'{self.atom1}-{self.atom2}:{self.bond_order}'
