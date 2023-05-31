from code.Molecule import Molecule

import code.constants as c
import code.functions as f

def main():

    #Ask if user want to load smiles strings from .txt file while answer != YES or NO#
    print(c.LOAD_SOURCE)
    answer = input(c.PROMPT)
    while answer.upper() != c.YES and answer.upper() != c.NO:
        print(c.INVALID_ANSWER)
        answer = input(c.PROMPT)

    #If answer == YES ask for file name and, if it is possible, read only valid smiles from the file#
    if answer.upper() == c.YES:
        print(c.INPUT_FILE_NAME)
        file_name = input(c.PROMPT)
        f.read_molecules_from_file(file_name)
        if not Molecule.all:
            print(c.LIST_IS_EMPTY)

    #Print help message#
    f.print_help_message()

    #Ask for command to execute#
    command = input(c.PROMPT)
    while command.upper() != c.QUIT:

        if command.upper() == c.LIST:
            f.list_smiles()
            f.print_help_message()
        elif command.upper() == c.INPUT:
            f.input_molecule()
            f.print_help_message()
        elif command.upper() == c.MOLECULAR_FORMULA:
            f.list_molecular_formulas()
            f.print_help_message()
        elif command.upper() == c.CONNECTION_TABLE:
            f.connection_table()
            f.print_help_message()
        elif command.upper() == c.LIST_MOLECULAR_WEIGHTS:
            f.list_molecular_weights()
            f.print_help_message()
        elif command.upper() == c.COUNT_SUBSTRINGS:
            f.count_substrings()
            f.print_help_message()
        elif command.upper() == c.DISSIMILARITY:
            f.dissimilarity()
            f.print_help_message()
        else:
            print(c.INVALID_COMMAND)
        command = input(c.PROMPT)

    #Asks if user want to save smiles list to file .txt#
    print(c.SAVE_SMILES)
    answer = input(c.PROMPT)
    while answer.upper() != c.YES and answer.upper() != c.NO:
        print(c.INVALID_ANSWER)
        answer = input(c.PROMPT)

    if answer.upper() == c.YES:
        file_name = input(c.PROMPT)
        f.write_to_file(file_name)

    #Print Goodbye message#
    print(c.GOODBYE)


main()
