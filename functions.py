import csv

import constants as c

from errors import StructureError
from Smiles import Smiles
from Molecule import Molecule

def read_strings_from_file(file_name):
    with open(file_name, 'r') as file:
        strings = file.read().splitlines()
    return strings

def read_molecules_from_file(file_name):
    """
    :param file_name: str
    read all strings from txt file and try
    """
    try:
        strings = read_strings_from_file(file_name)
        for string in strings:
            try:
                molecule = Molecule(string)
            except StructureError as e:
                print(f'SMILES invalid: {string}', e.message)
    except FileNotFoundError:
        print(c.FAILED_READING + file_name)

def list_smiles():
    for molecule in Molecule.all:
        print(molecule.smiles)

def input_molecule():
    string = input(c.INPUT_SMILES)

    try:
        smiles = Smiles(string)
        molecule = Molecule(smiles)
    except StructureError as e:
        print(f'SMILES invalid: {string}', e.message)

def list_molecular_formulas():
    for molecule in Molecule.all:
        molecule.get_molecular_formula()
        print(f'{molecule.smiles}: {molecule.molecular_formula}')

def connection_table():
    string = input('enter SMILES string:')
    smiles = Smiles(string)
    molecule = Molecule(smiles)
    print(molecule.structure.get_connection_table())

def list_molecular_weights():
    for molecule in Molecule.all:
        molecule.get_molecular_weight()
        print(f'{molecule.smiles}: {molecule.molecular_weight}')

def count_substrings():
    substrings_list = []

    answer = input(c.INPUT_SOURCE)
    while answer.upper() != c.FILE and answer.upper() != c.TERMINAL:
        print(c.INVALID_INPUT)
        answer = input(c.INPUT_SOURCE)

    if answer.upper() == c.FILE:
        file_name = input(c.PROMPT)
        try:
            with open('file_name', 'r') as file:
                substrings_list = file.read().splitlines()
        except FileNotFoundError:
            print(c.FAILED_READING + str(file_name))

        if not substrings_list:
            print(c.LIST_IS_EMPTY)

    if answer.upper() == c.TERMINAL:
        num_of_strings = int(input('enter number of substrings: '))
        for i in range(num_of_strings):
            substring = input()
            substrings_list.append(substring)
    print(substrings_list)
    for molecule in Molecule.all:
        res = f'{molecule.smiles}  contains'
        for substring in substrings_list:
            number = molecule.smiles.smiles.count(substring)
            molecule.descriptors[substring] = number
            res += f' {substring} {number} times'

        print(res)

def count_dissimilarity(str1, str2, substrings_list):
    dissimilarity = 0
    for substring in substrings_list:
        number1 = str1.count(substring)
        number2 = str2.count(substring)
        dissimilarity += (number1 - number2) ** 2
    return dissimilarity

def dissimilarity():
    structure1 = input('Give SMILES 1:')
    structure2 = input('Give SMILES 2:')
    number_of_substrings = int(input('enter number of substrings: '))
    substrings_list = []
    for i in range(number_of_substrings):
        substring = input()
        substrings_list.append(substring)
    dissimilarity = count_dissimilarity(structure1, structure2, substrings_list)
    print('dissimilarity =  ', dissimilarity)

def write_to_file(file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        header = ['SMILES'] + list(Molecule.all[0].descriptors.keys())
        writer.writerow(header)
        for molecule in Molecule.all:
            row = [str(molecule.smiles)] + list(molecule.descriptors.values())
            writer.writerow(row)

def print_help_message():
    help_message = ['C: count the number of times each sub-string from an external list (given file) occurs in the SMILES strings of the list.',
                    'M: Count the number of times each atomic element occurs in the strings in the list and obtain the molecular formula (number of atoms of each element, e.g., C8NO2). The output of the command should appear in the terminal and be in lexicographic order.',
                    'D: compare a given pair of molecules from their SMILES representation (calculate their dissimilarity, i.e., sum of squared differences between the number of occurrences of the sub-strings in two SMILES).',
                    "I: input a new SMILES string to be added to the current list, if valid (if not, the application reports it found a problem and waits for the user's to input a new command).",
                    'L: list all loaded SMILES',
                    'LMW: list molecular weights of all loaded molecules'
                    'H: help - list all commands.',
                    'Q: quit - quit the application.']
    for i in help_message:
        print(i)