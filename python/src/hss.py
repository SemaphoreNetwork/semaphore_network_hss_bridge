import json
import time
from web3 import Web3
import asyncio
import pickledb
import crypto
import account
import config

class SemaphoreNetworkHSS:
    def __init__(self):
        data = config.getConfig()

        self.hss_abi = open("./python/contract/SemaphoreNetworkHSS.json")
        self.rpc = data["rpc_url"]
        
        self.hss_contract_address = data["hss_address"]
        self.hss_priv = data["hss_private_key"]

        self.HssContractAbi = json.load(self.hss_abi)
        self.web3 = Web3(Web3.HTTPProvider(self.rpc))
        self.HssContract = self.web3.eth.contract(address=self.hss_contract_address, abi=self.HssContractAbi["abi"])

    def hss_loop(self):
        default_account = self.web3.eth.account.from_key(self.hss_priv[2:])
        s_account = account.SemaphoreNetworkAccount(default_account)

        b = crypto.CryptoUtils()
        tinyec_pub = b.public_key_from_raw_priv(int(self.hss_priv[2:], 16))
        
        print("HSS Pubkey (uncompressed):", f"{b.decompress_publicKey(tinyec_pub):#x}")
