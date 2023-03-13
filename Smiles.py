from Atom import Atom
from Bond import Bond
from Structure import Structure

from errors import StructureError

def make_components_dict():
    components_dict = {}
    organic_subset = ['B', 'C', 'N', 'O', 'S', 'P', 'F', 'Cl', 'Br', 'I']
    organic_aromatic = ['b', 'c', 'n', 'o', 's', 'p']

    for atom in organic_subset:
        components_dict[atom] = 'atom'
    for atom in organic_aromatic:
        components_dict[atom] = 'atom'
    for i in range(1, 100):
        components_dict[str(i)] = 'cycle_marker'

    components_dict['-'] = 'single_bond'
    components_dict["="] = 'double_bond'
    components_dict['\\'] = 'chiral_double_bond'
    components_dict['/'] = 'chiral_double_bond'
    components_dict['#'] = 'triple_bond'
    components_dict['$'] = 'quadruple_bond'
    components_dict[':'] = 'aromatic_bond'
    components_dict["("] = 'branch_start'
    components_dict[")"] = 'branch_end'
    components_dict['%'] = 'cycle_bond'
    return components_dict

def parse_square_brackets(component, atom_counter):
    elements = ['B', 'C', 'N', 'O', 'S', 'P', 'F', 'Cl', 'Br', 'I', 'As', 'Si', 'Te', 'Se', 'H',
                'b', 'c', 'n', 'o', 's', 'p', 'as', 'se', 'te', 'si']

    chiral_mark = ''
    charge = 0
    explicit_hydrogens = 0
    explicit_mass = ''

    #Deleting first bracket#
    component = component[1:]

    #Dealing with isotopes#
    for i in component:
        if i in '0123456789':
            explicit_mass += i
        else:
            break
    component = component[len(explicit_mass):]
    if explicit_mass == '':
        explicit_mass = 0
    else:
        explicit_mass = int(explicit_mass)

    #Dealing with element symbol#
    if component[0:2] in elements:
        element = component[0:2]
        component = component[2:]
    elif component[0] in elements:
        element = component[0]
        component = component[1:]
    else:
        raise StructureError('invalid_SMILES')

    #Dealing with chirality#
    chiral_marks_count = component.count('@')
    chiral_mark = '@' * chiral_marks_count
    if chiral_marks_count > 2:
        raise StructureError('invalid_SMILES')

    #Dealing with explicit hydrogens#
    hydrogens_count = component.count('H')
    if hydrogens_count > 1:
        explicit_hydrogens = hydrogens_count
    elif hydrogens_count == 1:
        if component[component.find('H')+1] in '123456789':
            explicit_hydrogens = int(component[component.find('H')+1])

    #Dealing with charge#
    positive_count = component.count('+')
    negative_count = component.count('-')

    if positive_count > 1:
        charge = positive_count
    elif positive_count == 1:
        if component[component.find('+')+1] in '123456789':
            charge = int(component[component.find('+')+1])
        else:
            charge = positive_count

    if negative_count > 1:
        charge = -1 * negative_count
    elif negative_count == 1:
        if component[component.find('-')+1] in '123456789':
            charge = -1 * int(component[component.find('-')+1])
        else:
            charge = -1 * negative_count

    return Atom(element, atom_counter, chiral_mark, charge, explicit_hydrogens, explicit_mass)

def get_previous_atom(atom_counter, branch_starts, branch_ends, branch_level):
    previous_atom = 0
    if atom_counter - 1 not in branch_ends:
        previous_atom = atom_counter - 1
    else:
        for i in branch_starts:
            if branch_starts[i] <= branch_level:
                previous_atom = i
    return previous_atom

class Smiles:
    def __init__(self, smiles: str):
        if smiles == '':
            raise StructureError('empty_SMILES')

        self.smiles = smiles
        self.get_components()

    def __str__(self):
        string = f'{self.smiles}'
        return string

    def __eq__(self, smiles):
        if type(smiles) == Smiles:
            if self.smiles == smiles.smiles:
                return True
        else:
            return False

    def get_components(self):
        components_dict = make_components_dict()
        component = ''
        components = []

        skip = False
        square_brackets = False
        double_digits = False

        for i, character in enumerate(self.smiles):
            if skip:
                skip = False
            else:
                if character == '[':
                    square_brackets = True

                if not square_brackets:

                    if character not in components_dict:
                        raise StructureError('invalid_symbol')

                    if double_digits:
                        components.append(self.smiles[i: i+2])
                        skip = True
                        double_digits = False
                    else:

                        if self.smiles[i: i+2] in components_dict and \
                                components_dict[self.smiles[i: i+2]] != 'cycle_marker':
                            components.append(self.smiles[i: i+2])
                            skip = True
                        else:
                            components.append(character)
                else:
                    component += character

                if character == ']':
                    square_brackets = False
                    components.append(component)
                    component = ''

                if character == '%':
                    double_digits = True

        self.components = components

    def get_structure(self):
        components_dict = make_components_dict()

        structure = Structure(atoms={}, bonds={})

        bonds = {   'single_bond': 1,
                    'double_bond': 2,
                    'triple_bond': 3,
                    'quadruple_bond': 4,
                    'chiral_double_bond': 2,
                    'aromatic_bond': 1.5}

        branch_starts = {}
        branch_ends = {}
        branch_level = 0

        bond_order = 1
        explicit_bond_order = 0
        bond_chirality = ''

        atom_counter = 0
        bond_counter = 0

        cycle_starts = {}

        square_brackets = False

        for i, component in enumerate(self.components):

            #Check type of the component
            if component[0] == '[':
                component_type = 'atom'
                square_brackets = True
            else:
                component_type = components_dict[component]

            if i == 0 and component_type != 'atom':
                raise StructureError('invalid_SMILES')

            #Check type of the next component, except the last one
            if i != len(self.components) - 1:
                if self.components[i+1][0] == '[':
                    next_component_type = 'atom'
                else:
                    next_component_type = components_dict[self.components[i+1]]
            else:
                next_component_type = None

            #Dealing with bonds#
            if component_type in bonds:
                explicit_bond_order = bonds[component_type]
                if component_type == 'chiral_double_bond':
                    bond_chirality = component

                if next_component_type not in ['cycle', 'atom', 'branch_start', 'cycle_marker']:
                    raise StructureError('invalid_SMILES')

            #Dealing with branch starts#
            if component_type == 'branch_start':
                if atom_counter not in branch_ends:
                    branch_starts[atom_counter] = branch_level
                branch_level += 1

                if next_component_type != 'atom' and next_component_type not in bonds:
                    raise StructureError('invalid_SMILES')

            #Dealing with branch ends#
            if component_type == 'branch_end':
                branch_ends[atom_counter] = branch_level
                branch_level += -1

                if next_component_type not in ['branch_end', 'atom', 'branch_start'] and \
                        next_component_type not in bonds:
                    raise StructureError('invalid_SMILES')

            #Prevent closing branch without opening#
            if branch_level < 0:
                raise StructureError('close_but_not_opened')

            #Dealing with atoms#
            if component_type == 'atom':
                atom_counter += 1

                if square_brackets:
                    atom = parse_square_brackets(component, atom_counter)
                    square_brackets = False
                else:
                    atom = Atom(component, atom_counter)

                structure.add_atom(atom)

                #Saving bond in structure.bonds and in atoms.bonds#
                if atom_counter != 1:
                    previous_atom = get_previous_atom(atom_counter, branch_starts, branch_ends, branch_level)

                    if explicit_bond_order != 0:
                        bond_order = explicit_bond_order
                    else:
                        if structure.get_atom(atom_counter).aromaticity \
                                and structure.get_atom(previous_atom).aromaticity:
                            bond_order = 1.5

                    bond_counter += 1
                    bond = Bond(bond_counter, atom_counter, previous_atom, bond_order, bond_chirality)

                    structure.add_bond(bond)

                    bond_order = 1
                    explicit_bond_order = 0
                    bond_chirality = ''

            #Dealind with cycles#
            if component_type == 'cycle_marker':

                if component not in cycle_starts:
                    cycle_starts[component] = atom_counter
                else:
                    if explicit_bond_order != 0:
                        bond_order = explicit_bond_order
                    else:
                        if structure.atoms[atom_counter].aromaticity \
                                and structure.atoms[cycle_starts[component]].aromaticity:
                            bond_order = 1.5

                    bond_counter += 1
                    bond = Bond(bond_counter, atom_counter, cycle_starts[component], bond_order, bond_chirality)
                    structure.add_bond(bond)

                    cycle_starts.pop(component)

                    bond_order = 1
                    explicit_bond_order = 0
                    bond_chirality = ''

        else:
            if branch_level != 0:
                raise StructureError('branch_not_closed')
            if cycle_starts:
                raise StructureError('cycle_not_closed')

        return structure
