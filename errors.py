class StructureError(Exception):

    def __init__(self, error_type):
        error_message = {'invalid_symbol': 'SMILES contains invalid symbol.',
                         'invalid_SMILES': 'SMILES invalid.',
                         'unknown_element': 'SMILES contains unknown chemical element.',
                         'close_but_not_opened': 'Branch closing detected, but no branch opening before.',
                         'branch_not_closed': 'Branch was opened but not closed.',
                         'cycle_not_closed': 'cycle opened but not closed.',
                         'empty_SMILES': 'SMILES string is empty'}
        self.message = error_message[error_type]

    def __str__(self):
        return self.message
