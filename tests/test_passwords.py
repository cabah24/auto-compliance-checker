from src.collector.passwords_ps import _parse_net_accounts




def test_parse_net_accounts():
    sample = '''
    The command completed successfully.


    Force user logoff how long after time expires?: 0
    Minimum password age (days): 0
    Maximum password age (days): 42
    Minimum password length: 8
    Lockout threshold: 0
    '''


    parsed = _parse_net_accounts(sample)
    assert parsed['Minimum password length'] == '8'
    assert parsed['Maximum password age (days)'] == '42'