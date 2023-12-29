from tinyec import registry

class CryptoUtils:
# curve constant, needs recent tinyec
    curve = registry.get_curve('secp256k1')

# helper fn() for compressing the pubKey x&y coords into common format.
    def __init__(self):
        self.curve = registry.get_curve('secp256k1')

    def compress(self, pubKey):
        return hex(pubKey.x) + hex(pubKey.y % 2)[2:]

# chop 0x from key take from hex to base10
    def keyToBaseTen(self, key):
        return int(key.hex()[2:], 16)

# get compressed pub from full account obj.
    def get_compressed_pub_from_account(self, account):
    # make priv key a Base10 int.
        priv = account.key
        privBaseTen = self.keyToBaseTen(priv)

    # multiply priv by generator
        pub = privBaseTen * self.curve.g

    # compress pubkey
        compressedPub = self.compress(pub)
        return compressedPub

    # account - self account obj
    # public key of subscriber in base 10


    def gen_shared_secret(self, account, pubKeyBaseTen):
        accountPrivBaseTen = self.keyToBaseTen(account.key)

        shared = accountPrivBaseTen * pubKeyBaseTen
        return shared


## hardcoded to secp256k1 (eth curve)
    def decompress_publicKey(self, compressedPubKey):
        p_hex = 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F'
        p = int(p_hex, 16)
        b = self.curve.b
        x_hex = compressedPubKey[2:66]
        x = int(x_hex,16)

        y_square = (pow(x, 3, p) + b) % p
        y_square_square_root = pow(y_square, (p+1)//4, p)

    
        #todo fix parity
        # y = (-y_square_square_root) % p
        y = y_square_square_root

        return y
    
    def public_key_from_raw_priv(self,raw_priv):
        pub = self.curve.g * raw_priv
        pubKeyCompressed = '0' + str(2 + pub.y % 2) + str(hex(pub.x)[2:])
        # print('compressed pubkey: ', pubKeyCompressed)
        return pubKeyCompressed


    