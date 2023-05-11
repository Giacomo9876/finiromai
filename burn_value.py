from solcx import compile_source
from web3 import Web3
import api_lol_function

class BurnValue:
    
    def __init__(self, contract_address, web3):
        with open("take_value.sol", "r") as f:
            source = f.read()
        compiled = compile_source(source)
        contract_interface = compiled['<stdin>:PythonOperations']
        self.contract = web3.eth.contract(abi=contract_interface['abi'], address=contract_address)
    
    def get_token_to_burn_from_lol(self, amount_to_burn):
        amount = amount_to_burn
        return self.contract.functions.burn(amount).call()