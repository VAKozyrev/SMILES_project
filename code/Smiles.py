from code.Atom import Atom
from code.Bond import Bond
from code.Structure import Structure

from code.errors import StructureError, InvalidSymbol

def make_components_dict():
    """
    :return: components_dict: dict{symbol: label}
    create dictionary of possible symbols in the SMILES and label them according to their type
    """
    components_dict = {}
    atoms = ['B', 'C', 'N', 'O', 'S', 'P', 'F', 'Cl', 'Br', 'I', 'b', 'c', 'n', 'o', 's', 'p']

    for atom in atoms:
        components_dict[atom] = 'atom'
    for i in range(1, 100):
        components_dict[str(i)] = 'cycle_marker'

    components_dict["="] = "double_bond"
    components_dict["("] = "branch_start"
    components_dict[")"] = "branch_end"
    components_dict['\\'] = 'chiral_double_bond'
    components_dict['/'] = 'chiral_double_bond'
    components_dict['#'] = 'triple_bond'
    components_dict['$'] = 'quadruple_bond'
    components_dict['.'] = 'split'
    components_dict['-'] = 'single_bond'
    components_dict[':'] = 'aromatic_bond'
    return components_dict

class Smiles:
    components_dict = make_components_dict()
    two_atom_dict = {'B': {'r'}, 'C': {'l'}}

    def __init__(self, smiles_string: str):
        self.smiles = smiles_string
        self.components = []
        self.get_components()

    def __str__(self):
        return f'{self.smiles}'

    def __repr__(self):
        return f'Smiles({self.smiles})'

    def __eq__(self, smiles):
        if type(smiles) == Smiles and self.smiles == smiles.smiles:
            return True
        return False

    def get_components(self):
        """
        :return: self.components: list
        break SMILES string into components and append them to the list self.components
        """
        if self.smiles == '':
            raise StructureError('empty_SMILES')

        component = ''
        skip = False
        square_brackets = False
        double_digits = False

        for i, character in enumerate(self.smiles):
            if skip:
                skip = False
                continue

            if square_brackets:
                component += character
                if character == ']':
                    square_brackets = False
                    self.components.append(component)
                    component = ''

            elif double_digits:
                if character not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    raise InvalidSymbol(self.smiles, i)
                component += character
                if len(component) == 2:
                    self.components.append(component)
                    double_digits = False
                    component = ''
            else:

                if character in self.two_atom_dict:
                    try:
                        next_character = self.smiles[i + 1]
                        if next_character in self.two_atom_dict[character]:
                            self.components.append(character + next_character)
                            skip = True
                        else:
                            self.components.append(character)
                    except IndexError:
                        self.components.append(character)

                elif character == '[':
                    square_brackets = True
                    component = character
                elif character == '%':
                    double_digits = True
                    component = ''
                elif character not in self.components_dict:
                    raise InvalidSymbol(self.smiles, i)
                else:
                    self.components.append(character)

    def get_structure(self):

        structure = Structure(atoms={}, bonds={})

        bonds = {'single_bond': 1,
                 'double_bond': 2,
                 'triple_bond': 3,
                 'quadruple_bond': 4,
                 'aromatic_bond': 1.5}

        #Track opening and closing branches#
        branch_starts = {}
        branch_ends = {}
        splits = []
        #Track current branch level#
        branch_level = 0

        bond_order = 1
        explicit_bond_order = 0

        atom_counter = 0
        bond_counter = 0

        #Tracking starts of cycles#
        cycle_starts = {}
        explicit_bond_order_cycles = {}

        square_brackets = False

        for i, component in enumerate(self.components):

            #C heck type of the component
            if component[0] == '[':
                component_type = 'atom'
                square_brackets = True
            else:
                component_type = self.components_dict[component]

            if i == 0 and component_type != 'atom':
                raise InvalidSymbol(self.smiles, i)

            #Check type of the next component#
            try:
                if self.components[i+1][0] == '[':
                    next_component_type = 'atom'
                else:
                    next_component_type = self.components_dict[self.components[i+1]]
            except IndexError:
                next_component_type = None

            if component_type == 'split':
                branch_starts = {}
                branch_ends = {}
                branch_level = 0
                bond_order = 1
                explicit_bond_order = 0
                splits.append(atom_counter)
            #Dealing with bonds#
            if component_type in bonds:
                explicit_bond_order = bonds[component_type]

                if next_component_type not in ['atom', 'cycle_marker']:
                    raise StructureError('bond')

            #Dealing with branch starts#
            if component_type == 'branch_start':
                if atom_counter not in branch_ends:
                    branch_starts[atom_counter] = branch_level
                branch_level += 1

                if next_component_type not in ['atom', 'chiral_double_bond'] and next_component_type not in bonds:
                    raise StructureError('branch_start')

            #Dealing with branch ends#
            if component_type == 'branch_end':
                branch_ends[atom_counter] = branch_level
                branch_level += -1

                if next_component_type not in ['branch_end', 'atom', 'branch_start', 'chiral_double_bond'] and \
                        next_component_type not in bonds:
                    raise StructureError('branch_end')

            #Prevent closing branch without opening#
            if branch_level < 0:
                raise StructureError('branch_end')

            #Dealing with atoms#
            if component_type == 'atom':
                atom_counter += 1

                if square_brackets:
                    element, hydrogens, chiral_mark, charge, mass = Smiles.parse_square_brackets(component)
                    atom = Atom(element, atom_counter, chiral_mark, charge, hydrogens, mass)
                    square_brackets = False
                else:
                    atom = Atom(component, atom_counter)

                structure.add_atom(atom)

                #Saving bond in structure.bonds and in atoms.bonds#
                if atom_counter != 1:
                    previous_atom = self.get_previous_atom(atom_counter, branch_starts, branch_ends, branch_level, splits)
                    if previous_atom:
                        if explicit_bond_order:
                            bond_order = explicit_bond_order
                        else:
                            if structure.get_atom(atom_counter).aromaticity \
                                    and structure.get_atom(previous_atom).aromaticity:
                                bond_order = 1.5

                        bond_counter += 1
                        bond = Bond(bond_counter, atom_counter, previous_atom, bond_order)

                        structure.add_bond(bond)

                        bond_order = 1
                        explicit_bond_order = 0

            #Dealind with cycles#
            if component_type == 'cycle_marker':

                if component not in cycle_starts:
                    cycle_starts[component] = atom_counter
                    if explicit_bond_order:
                        explicit_bond_order_cycles[component] = explicit_bond_order
                        explicit_bond_order = 0
                else:
                    if explicit_bond_order != 0:
                        bond_order = explicit_bond_order
                    else:
                        if structure.atoms[atom_counter].aromaticity \
                                and structure.atoms[cycle_starts[component]].aromaticity:
                            bond_order = 1.5
                        if component in explicit_bond_order_cycles:
                            bond_order = explicit_bond_order_cycles[component]

                    bond_counter += 1
                    bond = Bond(bond_counter, atom_counter, cycle_starts[component], bond_order)
                    structure.add_bond(bond)

                    cycle_starts.pop(component)

                    bond_order = 1
                    explicit_bond_order = 0

        else:
            if branch_level:
                raise StructureError('branch_not_closed')
            if cycle_starts:
                raise StructureError('cycle_not_closed')

        structure.set_hydrogens()

        return structure

    @staticmethod
    def parse_square_brackets(component: str):
        """
        :param component: str
        :return: element_symbol: str, explicit_hydrogens: int, chiral_mark: str, charge: int, explicit_mass: int
        for given SMILES component into square brackets return symbol of the element, number of explicitly shown
        hydrogens atoms, chiral mark (@ or @@), charge and explicitly shown mass of the atom.
        """
        elements = ['B', 'C', 'N', 'O', 'S', 'P', 'F', 'Cl', 'Br', 'I', 'As', 'Si', 'Te', 'Se', 'H',
                    'b', 'c', 'n', 'o', 's', 'p', 'as', 'se', 'te', 'si']
        not_alowed_elements = ['Bi', 'Fe', 'Ho', 'Zn', 'Cu', 'Ag', 'Au', 'Hg']

        chiral_mark = ''
        charge = 0
        explicit_hydrogens = 0
        explicit_mass = ''

        #Deleting the first bracket#
        component = component[1:]

        #Dealing with isotopes#
        for character in component:
            if character in '0123456789':
                explicit_mass += character
            else:
                break
        #Deleting isotopes numbers from the beginning of the  component#
        component = component[len(explicit_mass):]
        if explicit_mass:
            explicit_mass = int(explicit_mass)
        else:
            explicit_mass = 0

        #Dealing with element symbol#
        if component[0:2] in elements:
            element_symbol = component[0:2]
            component = component[2:]      # Deleting element symbol from the component#
        elif component[0:2] in not_alowed_elements:
            raise StructureError('invalid_element')
        elif component[0] in elements:
            element_symbol = component[0]
            component = component[1:]      # Deleting element symbol from the component#
        else:
            raise StructureError('invalid_element')  # Invalid element symbol#

        #Dealing with chirality#
        chiral_mark = '@' * component.count('@')
        if len(chiral_mark) > 2:
            raise StructureError('chiral_mark')  # More than 2 @ symbols#

        # Dealing with explicit hydrogens#
        hydrogens_count = component.count('H')
        if hydrogens_count > 1:
            explicit_hydrogens = hydrogens_count
        elif hydrogens_count == 1:
            if component[component.find('H') + 1] in '123456789':
                explicit_hydrogens = int(component[component.find('H') + 1])
            else:
                explicit_hydrogens = 1
        else:
            explicit_hydrogens = 0

        # Dealing with charge#
        positive_count = component.count('+')
        negative_count = component.count('-')

        if positive_count > 1:
            charge = positive_count
        elif positive_count == 1:
            if component[component.find('+') + 1] in '123456789':
                charge = int(component[component.find('+') + 1])
            else:
                charge = positive_count

        if negative_count > 1:
            charge = -1 * negative_count
        elif negative_count == 1:
            if component[component.find('-') + 1] in '123456789':
                charge = -1 * int(component[component.find('-') + 1])
            else:
                charge = -1 * negative_count

        return element_symbol, explicit_hydrogens, chiral_mark, charge, explicit_mass

    @staticmethod
    def get_previous_atom(atom_counter, branch_starts, branch_ends, branch_level, splits):
        if atom_counter - 1 in splits:
            return None
        elif atom_counter - 1 not in branch_ends:
            return atom_counter - 1
        else:
            if branch_ends[atom_counter - 1] == branch_level:
                for i in list(branch_starts.keys())[::-1]:
                    if branch_starts[i] < branch_level:
                        return i
            else:
                for i in list(branch_starts.keys())[::-1]:
                    if branch_starts[i] <= branch_level:
                        return i
