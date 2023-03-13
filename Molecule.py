from Smiles import Smiles

def make_atom_counter_dict():
    atom_counter_dict = {}
    elements = ['carbon', 'hydrogen', 'lithium', 'boron', 'nitrogen', 'oxygen', 'fluorine', 'sodium',
                'silicon', 'phosphorus', 'sulfur', 'chlorine', 'arsenic', 'selenium', 'bromine', 'iodine']

    for element in elements:
        atom_counter_dict[element] = 0

    return atom_counter_dict

class Molecule:

    element_symbols = {'hydrogen': 'H', 'lithium': 'Li', 'boron': 'B', 'carbon': 'C', 'nitrogen': 'N',
                       'oxygen': 'O', 'fluorine': 'F', 'sodium': 'Na', 'silicon': 'Si', 'phosphorus': 'P',
                       'sulfur': 'S', 'chlorine': 'Cl', 'arsenic': 'As', 'selenium': 'Se', 'bromine': 'Br',
                       'iodine': 'I'}

    all = []

    def __init__(self, smiles: Smiles):
        self.smiles = smiles
        self.structure = smiles.get_structure()
        self.get_molecular_formula()
        if self not in Molecule.all:
            Molecule.all.append(self)
        else:
            print(f'{self.smiles} is already loaded.')

    def __eq__(self, other_molecule):
        if self.smiles == other_molecule.smiles:
            return True

    def get_molecular_formula(self):
        atom_counter_dict = make_atom_counter_dict()

        molecular_formula = ""

        for atom_number in self.structure.atoms:
            element = self.structure.atoms[atom_number].element
            atom_counter_dict[element] += 1
            atom_counter_dict['hydrogen'] += self.structure.atoms[atom_number].hydrogens

        if isinstance(atom_counter_dict['hydrogen'], float):
            if atom_counter_dict['hydrogen'].is_integer:
                atom_counter_dict['hydrogen'] = int(atom_counter_dict['hydrogen'])

        for element in atom_counter_dict:
            if atom_counter_dict[element] > 0:
                molecular_formula += self.element_symbols[element]
                if atom_counter_dict[element] > 1:
                    molecular_formula += str(atom_counter_dict[element])

        self.molecular_formula = molecular_formula

    def get_molecular_weight(self):

        molecular_weight = 0
        for atom in self.structure.get_atoms():
            molecular_weight += atom.mass + atom.hydrogens

        self.molecular_weight = round(molecular_weight, 2)
