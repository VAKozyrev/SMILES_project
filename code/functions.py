import csv
import sys

import constants as c

from errors import StructureError, InvalidSymbol
from Smiles import Smiles
from Molecule import Molecule

def select_input_source():
    print(c.INPUT_SOURCE)
    input_source = input(c.PROMPT)
    while input_source.upper() != c.FILE and input_source.upper() != c.TERMINAL:
        print(c.INVALID_INPUT)
        input_source = input(c.PROMPT)
    return input_source.upper()

def read_strings_from_file(file_name):
    """
    :param file_name: str
    :return: strings: list of str
    read all string from .txt file and return list of strings
    """
    with open(file_name, 'r') as file:
        strings = file.read().splitlines()
    return strings

def read_molecules_from_file(file_name):
    try:
        strings = read_strings_from_file(file_name)
        for i, string in enumerate(strings):
            try:
                molecule = Molecule(string)
                if molecule not in Molecule.all:
                    Molecule.all.append(molecule)
                #else:
                    #print(f'{molecule.smiles} is already loaded.')
            except StructureError as e:
                print(f'\rSMILES {string} invalid ' + e.message)
            except InvalidSymbol as e:
                print('\r'+e.message)
            sys.stdout.write(f"\r{i} SMILES processed")
            sys.stdout.flush()
        print(f'\n{len(Molecule.all)} SMILES loaded')
    except FileNotFoundError:
        print(c.FAILED_READING + f' "{file_name}"')

def list_smiles():
    if Molecule.all:
        for molecule in Molecule.all:
            print(molecule.smiles)
    else:
        print(c.LIST_IS_EMPTY)

def input_molecule():
    print(c.INPUT_SOURCE)
    answer = input(c.PROMPT)

    while answer.upper() != c.TERMINAL and answer.upper() != c.FILE:
        print(c.INVALID_ANSWER)
        answer = input(c.PROMPT)

    if answer.upper() == c.FILE:
        print(c.INPUT_FILE_NAME)
        file_name = input(c.PROMPT)
        read_molecules_from_file(file_name)

    else:
        print(c.INPUT_SMILES)
        string = input(c.PROMPT)
        try:
            molecule = Molecule(string)
            if molecule not in Molecule.all:
                Molecule.all.append(molecule)
                print(f'SMILES {string} was loaded')
                print(f'{len(Molecule.all)} SMILES loaded')
            else:
                print(f'{molecule.smiles} is already loaded.')
        except StructureError as e:
            print(f'SMILES {string} invalid ' + e.message)
        except InvalidSymbol as e:
            print(e.message)


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

    input_source = select_input_source()

    if input_source == c.FILE:
        print(c.INPUT_FILE_NAME)
        file_name = input(c.PROMPT)
        try:
            substrings_list = read_strings_from_file(file_name)
        except FileNotFoundError:
            print(c.FAILED_READING + ' ' + file_name)

    if input_source == c.TERMINAL:
        print('Enter number of substrings:')
        num_of_strings = int(input(c.PROMPT))
        for i in range(num_of_strings):
            substring = input(c.PROMPT)
            substrings_list.append(substring)

    if not substrings_list:
        print('Substrings list is empty')
    else:
        print('Specify output file .csv file name:')
        out_file_name = input(c.PROMPT)
        with open(out_file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            header = ['SMILES'] + substrings_list
            writer.writerow(header)
            for molecule in Molecule.all:
                for substring in substrings_list:
                    molecule.substrings[substring] = molecule.smiles.smiles.count(substring)
                row = [str(molecule.smiles)] + list(molecule.substrings.values())
                writer.writerow(row)

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
    with open(file_name, 'w') as file:
        for molecule in Molecule.all:
            file.write(str(molecule.smiles)+'\n')

def print_help_message():
    help_message = ['>',
                    'L: list all loaded SMILES',
                    'I: input a new SMILES strings',
                    'C: count the number of times each sub-string from an external list occurs in the SMILES',
                    'M: obtain the molecular formula',
                    'D: compare a given pair of molecules from their SMILES (calculate their dissimilarity)',
                    'MW: obtain molecular weights of all loaded molecules',
                    'Q: quit the application']
    for i in help_message:
        print(i)
