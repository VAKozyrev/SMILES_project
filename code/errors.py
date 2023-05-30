class StructureError(Exception):

    def __init__(self, error_type, atom=None):
        error_message = {'empty_SMILES': 'SMILES string is empty',
                         'invalid_SMILES': 'SMILES invalid',
                         'bond': 'Incorrect bond placement',
                         'branch_start': 'Incorrect branch opening',
                         'branch_end': 'Incorrect branch closing',
                         'unknown_element': 'SMILES contains unknown chemical element',
                         'branch_not_closed': 'Branch is not closed',
                         'cycle_not_closed': 'Incorrect cycle placement',
                         'wrong_valency': f'wrong valency of {atom} atom',
                         'invalid_element': 'Invalid element symbol',
                         'chiral_mark': 'Incorrect chiral mark placement'}
        self.message = error_message[error_type]

class InvalidSymbol(Exception):
    def __init__(self, smiles_string, position):
        self.message = f'{smiles_string} invalid: invalid symbol in position {position}'
