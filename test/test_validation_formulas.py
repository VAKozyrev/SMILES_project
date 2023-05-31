import csv

from code.Molecule import Molecule
from rdkit import Chem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

def validate_smiles_rdkit(smiles):
    try:
        molecule = Chem.MolFromSmiles(smiles)
        if molecule is None:
            return False
        return True
    except:
        return False

def validate_smiles_my(smiles):
    try:
        molecule = Molecule(smiles)
        return True
    except:
        return False

def write_strings_to_txt(file_name, strings):
    with open(file_name, 'w') as file:
        for string in strings:
            file.write(string +'\n')

def validate_smiles_file(file_name):
    with open(file_name, 'r') as file:
        rdkit_valid = []
        rdkit_invalid = []
        my_valid = []
        my_invalid = []
        smiles_list = file.read().splitlines()
        for smiles in smiles_list:
            if validate_smiles_rdkit(smiles):
                rdkit_valid.append(smiles)
            else:
                rdkit_invalid.append(smiles)
            if validate_smiles_my(smiles):
                my_valid.append(smiles)
            else:
                my_invalid.append(smiles)

    write_strings_to_txt(file_name + '_rdkit_valid.txt', rdkit_valid)
    write_strings_to_txt(file_name + '_rdkit_invalid.txt', rdkit_invalid)
    write_strings_to_txt(file_name + '_my_valid.txt', my_valid)
    write_strings_to_txt(file_name + '_my_invalid.txt', my_invalid)

    print('rdkit valid:', len(rdkit_valid))
    print('rdkit invalid:', len(rdkit_invalid))
    print('my valid: ', len(my_valid))
    print('my invalid: ', len(my_invalid))

def compare_molecular_formulas(file_name):
    not_the_same = {}
    formulas = {}
    with open(file_name, 'r') as file:
        smiles_list = file.read().splitlines()
        for smiles in smiles_list:
            molecule_my = Molecule(smiles)
            molecule_my.get_molecular_formula()
            my_formula = molecule_my.molecular_formula
            molecule_rdkit = Chem.MolFromSmiles(smiles)
            rdkit_formula = CalcMolFormula(molecule_rdkit)
            formulas[smiles] = [rdkit_formula, my_formula]
            if my_formula != rdkit_formula:
                not_the_same[smiles] = [rdkit_formula, my_formula]
    return formulas, not_the_same

def write_dict_to_file(file_name, formulas_dict):
    with open(file_name, 'w') as file:
        for smiles in formulas_dict:
            string = f'{smiles}, {formulas_dict[smiles][0]}, {formulas_dict[smiles][1]}'
            file.write(string + '\n')

def write_formulas_to_csv(file_name, formulas_dict):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        header = ['SMILES', 'rdkit', 'my']
        writer.writerow(header)
        for smiles in formulas_dict:
            writer.writerow([smiles, formulas_dict[smiles][0], formulas_dict[smiles][1]])

def main():
    validate_smiles_file('chebi_NPatlas.smiles.txt')
    all_formulas, not_the_same_formulas = compare_molecular_formulas('chebi_NPatlas.smiles.txt_my_valid.txt')
    write_dict_to_file('not_the_same_formulas.txt', not_the_same_formulas)
    write_formulas_to_csv('formulas.csv', all_formulas)


main()
