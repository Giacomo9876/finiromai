from solcx import compile_source
from solcx import compile_standard, install_solc
import web3
from web3 import Web3
from web3 import HTTPProvider

install_solc("0.8.0")

class BurnValue:
    
    def __init__(self, contract_address, web3):
        with open("take_value.sol", "r") as f:
            source = f.read()
        compiled = compile_source(source)
        contract_interface = compiled['<stdin>:BurnValue']
        web3 = Web3(HTTPProvider('https://goerli.infura.io/v3/eba9e534005045928e460351c954cbf8'))
        print ("Latest Ethereum block number" , web3.eth.get_block_number)
        # contract_address = "0x6117A5F053e65Aa9bcbE064cD186Ed9580353bCa" # azircontract
        contract_address = "0x6e306F0D4280141276bf4fAd4a1c99ddcb155CE5" # takecontract
        #contract_id, contract_interface = contract_interface.popitem()
        # ERC20 0x6e306F0D4280141276bf4fAd4a1c99ddcb155CE5
    #     bytecode = contract_interface['bin']
    #     abi = contract_interface['abi']
    #     w3 = Web3(Web3.EthereumTesterProvider())
    #     w3.eth.default_account = w3.eth.accounts[0]
    #     Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)
    #     tx_hash = Greeter.constructor().transact()
    #     tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #     greeter = w3.eth.contract(
    #     address=tx_receipt.contractAddress,
    #     abi=abi
    # )
        print(contract_interface['abi'])
        self.contract = web3.eth.contract(abi=contract_interface['abi'], address=contract_address)
    
    def get_token_to_burn_from_lol(self, amount_to_burn):
        amount = amount_to_burn
        return self.contract.functions.get_token_to_burn_from_lol(amount).call()