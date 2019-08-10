TYPES = ['INT', 'FLOAT', 'STRING']
INT = 0
FLOAT = 1
STRING = 2


def calculate_type(token):
    if isinstance(token, int):
        return INT
    elif isinstance(token, float):
        return FLOAT
    elif isinstance(token, str):
        return STRING
    else:
        raise Exception('No such type: %s') % token


def process_token(input_list):
    """
    input_list is list. Do not have children list.
    """
    for token in input_list:
        print('<' + TYPES[calculate_type(token)] + '>' + str(token))