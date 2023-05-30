from Smiles import Smiles

def make_atom_counter():
    return {'C': 0, 'H': 0, 'B': 0, 'Br': 0, 'Cl': 0, 'F': 0, 'I': 0, 'N': 0, 'O': 0, 'P': 0, 'S': 0}
class Molecule:

    all = []

    def __init__(self, smiles: str):
        self.smiles = Smiles(smiles)
        self.structure = self.smiles.get_structure()
        self.substrings = {}

        self.molecular_formula = ''
        self.molecular_weight = 0

    def __eq__(self, other_molecule):
        if type(other_molecule) == Molecule and self.smiles == other_molecule.smiles:
            return True
        return False

    def get_molecular_formula(self):

        atom_counter = make_atom_counter()

        for atom in self.structure.get_atoms():
            atom_counter[atom.element] += 1
            atom_counter['H'] += atom.hydrogens

        if isinstance(atom_counter['H'], float):
            if atom_counter['H'].is_integer:
                atom_counter['H'] = int(atom_counter['H'])

        for element in atom_counter:
            if atom_counter[element] > 0:
                self.molecular_formula += element
                if atom_counter[element] > 1:
                    self.molecular_formula += str(atom_counter[element])

    def get_molecular_weight(self):

        for atom in self.structure.get_atoms():
            self.molecular_weight += atom.mass + atom.hydrogens

    def get_atoms(self):
        for atom in self.structure.get_atoms():
            print(atom)

    def get_bonds(self):
        for bond in self.structure.get_bonds():
            print(str(bond.number) + ':', bond)
