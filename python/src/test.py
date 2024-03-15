import unittest
import crypto
import config
import json
from web3 import Web3

HSS_ABI_FILE = "./python/contract/SemaphoreHSS.json"

# Answers
CorrectUncompressedPub = "c6b754b20826eb925e052ee2c25285b162b51fdca732bcf67e39d647fb6830aeb651944a574a362082a77e3f2b5d9223eb54d7f2f76846522bf75f3bedb8178e"
CorrectHashedUCPub = "0xe8b0087eec10090b15f4fc4bc96aaa54e2d44c299564da76e1cd3184a2386b8d"
CorrectEthereumAddress = "0xc96aaa54e2d44c299564da76e1cd3184a2386b8d"

class TestCryptoUtils(unittest.TestCase):
    def setUp(self):
        self.conf = config.getConfig()
        self.a = True

        HSS_ABI = open(HSS_ABI_FILE)
        self.hssContractABI = json.load(HSS_ABI)
        self.web3 = Web3(Web3.HTTPProvider(self.conf["rpc_url"]))
        self.hssContract = self.web3.eth.contract(address=self.conf["hss_address"], abi=self.hssContractABI["abi"])

        self.crypto = crypto.CryptoUtils()

    def test_get_uncompressedPub(self):
        print("Running: ", self._testMethodName)

        account = self.web3.eth.account.from_key(self.conf["hss_private_key"][2:])
        privTen = self.crypto.keyToBaseTen(account.key)
        pub = privTen * self.crypto.curve.g

        uncompressedPub = hex(pub.x)+hex(pub.y)[2:]
        print(hex(pub.x), len(hex(pub.x)),  hex(pub.y), len(hex(pub.y)))
        print("Uncompressed pub key: ", uncompressedPub)

        hashedUncompressedPub = Web3.keccak(hexstr=uncompressedPub[2:])
        print("Hashed uncompressed key: ", hashedUncompressedPub.hex())
        
        # TODO: show how got 26
        print("Ethereum address: ", "0x"+hashedUncompressedPub.hex()[26:])

        self.assertEqual("0x"+hashedUncompressedPub.hex()[26:], CorrectEthereumAddress)
        self.assertEqual(hashedUncompressedPub.hex(), CorrectHashedUCPub)
        self.assertEqual(uncompressedPub[2:], CorrectUncompressedPub)

    def test_decompress_pubKey(self):
        x_cord = CorrectUncompressedPub[:64]
        y_cord = CorrectUncompressedPub[64:]
        print("x-cord", x_cord, "y-cord", y_cord)

        mockPub = lambda: None

        mockPub.x = int(x_cord, 16)
        mockPub.y = int(y_cord,16)
        compressed = self.crypto.compress(mockPub)
        print("Compressed pub: ", compressed )

        print("Decompressed pub: ", hex(self.crypto.decompress_publicKey("0x"+compressed)))

if __name__ == "__main__":
    unittest.main()
