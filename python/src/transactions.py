from web3 import Web3
import json
import config

# Class for on-chain interactions with the deployed HSS contract.
class SemaphoreTransactions:
    def __init__(self, semaphore_account):
        f = open("config.json")
        data = json.load(f)

        self.SEPOLIA_RPC = data["rpc_url"]
        self.SEPOLIA_HSS_ADDRESS = data["hss_address"]
    
        self.HSS_ABI = open("./python/contract/SemaphoreNetworkHSS.json")
        
        self.HssContractAbi = json.load(self.HSS_ABI)
        self.web3 = Web3(Web3.HTTPProvider(self.SEPOLIA_RPC))
        self.HssContract = self.web3.eth.contract(address=self.SEPOLIA_HSS_ADDRESS, abi=self.HssContractAbi["abi"])
        
        self.s_account = semaphore_account

        self.web3_account = self.s_account.getWeb3Account()
    
    # Add subscriber and uncompressed pubkey for them.
    def add_sub_and_key(self, uncompressedPubToAdd):
        nonce = self.web3.eth.get_transaction_count(self.web3_account.address)

        add_pubkey_tx = self.HssContract.functions.addSubscriberAndKey(self.web3_account.address, uncompressedPubToAdd).build_transaction({
            "chainId": 11155111,
            "gas": 700000,
            "maxFeePerGas": self.web3.toWei("2", "gwei"),
            "maxPriorityFeePerGas": self.web3.toWei("1", "gwei"),
            "nonce": nonce,
        })

        signed_tx = self.web3.eth.account.sign_transaction(add_pubkey_tx, private_key=self.web3_account.key)

        return self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
       
    # Helper fn to query the Subscribers network ID (SNID). 
    def get_subscriber_pubkey(self, subscriberId):
        return self.HssContract.functions.getSubscriberKey(subscriberId).call()

    