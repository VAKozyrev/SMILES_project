import time
from matplotlib import pyplot as plt
from code.Molecule import Molecule
from rdkit import Chem

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

def test_speed_my(smiles_list):
    start_time = time.time()
    for smiles in smiles_list:
        validate_smiles_my(smiles)
    end_time = time.time()

    execution_time = end_time - start_time
    average_time = execution_time / len(smiles_list)
    average_per_1000 = average_time * 1000
    print("Execution Time:", execution_time)
    print("Average Time:", average_time)
    print("Average Time per 1000", average_per_1000)

def test_speed_rdkit(smiles_list):
    start_time = time.time()
    for smiles in smiles_list:
        validate_smiles_rdkit(smiles)
    end_time = time.time()

    execution_time = end_time - start_time
    average_time = execution_time / len(smiles_list)
    average_per_1000 = average_time * 1000
    print("Execution Time:", execution_time)
    print("Average Time:", average_time)
    print("Average Time per 1000", average_per_1000)


with open('chebi_NPatlas.smiles.txt', 'r') as file:
    smiles_list = file.read().splitlines()

    test_speed_rdkit(smiles_list)
    test_speed_my(smiles_list)
