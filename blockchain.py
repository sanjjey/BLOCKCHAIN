from web3 import Web3
from solcx import compile_source
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class BlockchainManager:
    def __init__(self, network_url, contract_address, contract_type):
        self.w3 = Web3(Web3.HTTPProvider(network_url))
        self.contract_address = contract_address
        self.contract_type = contract_type

        contract_path = Path(__file__).parent.parent.parent.parent / 'contracts' / f'{contract_type}.sol'
        with open(contract_path, 'r') as file:
            contract_source = file.read()

        self.compiled_contract = compile_source(contract_source)
        self.contract = self.w3.eth.contract(
            address=contract_address,
            abi=self.compiled_contract[f'<stdin>:{contract_type}']['abi']
        )

    def register_project(self, project_id, esg_score):
        tx_hash = self.contract.functions.registerProject(project_id, esg_score).transact()
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)