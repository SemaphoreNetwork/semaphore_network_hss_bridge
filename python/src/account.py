from eth_account import Account
import crypto
import test
import transactions
import hss

class SemaphoreNetworkAccount:
    def __init__(self, account):
        self.crypto = crypto.CryptoUtils()
        self.account = account
        self.transactions = transactions.SemaphoreTransactions(self)

    def getWeb3Account(self):
        return self.account

    def get_subscriber_pubKey_from_chain(self,subscriberIndex):
        subscriberAccount = account_from_pk(subscriberIndex)
        # Get public key from subscriber.
        # TODO: get this from chain.
        subscriberPub = crypto.get_compressed_pub_from_account(subscriberAccount)[2:]
        return subscriberPub
    

    def get_shared_secret(self, subscriberIndex):
        providerAccount = self.account

        print(
            f"Subscriber SUID index to lookup on chain (RAW) {subscriberIndex}")

        # Query web3 rpc @subscriber index, cast to int.
        # subscriberPub = account.get_subscriber_pubKey_from_chain(int(subscriberIndex))
        s_hss = hss.SemaphoreHSS()
        subscriberPub = self.transactions.get_subscriber_pubkey(subscriberIndex)

        print(
            f"Subscriber @{subscriberIndex}'s (compressed) pubkey is {subscriberPub}")

        # print(f"provider(self) compressed pubkey: {crypto.get_compressed_pub_from_account(providerAccount)[2:]}")

        # Generate shared secret.
        print(int(subscriberPub.hex()[2:], 16))
        shared_secret = self.crypto.gen_shared_secret(providerAccount, int.from_bytes(subscriberPub, "big"))
        return shared_secret

    def generate_account(self):
        account = Account.create("entropy lol")
        return account

    def import_account(self):
        # TODO: fn() that imports json wallet account & decrypts w/ env(?) password.
        return

    def account_from_pk(self, pk):
        account = Account.from_key(pk)
        return account

    def get_uncompressed_pub_from_account(self, account = None):
        # Private key in base10.
        privTen = None
        if account != None:
            privTen = self.crypto.keyToBaseTen(account.key)
        else:
            privTen = self.crypto.keyToBaseTen(self.account.key)

        pub = privTen * self.crypto.curve.g
        uncompressedPub = hex(pub.x)+hex(pub.y)[2:]
        print("uncompressed pub key: ", uncompressedPub)

        return uncompressedPub
    