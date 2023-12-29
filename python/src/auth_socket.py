import socket
import test
import account
import crypto
import account
import config


class SemaphoreNetworkAuthSocket:
    conf = config.getConfig()

    #socket ops
    HOST = "127.0.0.1"
    PORT = int(conf['socket_port'])

    def __init__(self, account):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_socket()
        self.connection = None
        self.account = account

    def bind_socket(self):
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen()

    def parse_rx_data(data):
        json = json.loads(data)
        return json

    def get_shared_secret(self, subscriberIndex):
        s_account = account.SemaphoreNetworkAccount(self.account)

        print('subindex', subscriberIndex)
        #might need to further parse subscriber index
        return s_account.get_shared_secret(int(subscriberIndex))

        #generate shared secret 
        #print(int(subscriberPub.hex()[2:], 16))
        c = crypto.CryptoUtils()
        shared_secret = c.gen_shared_secret(providerAccount, int.from_bytes(subscriberPub, "big"))
        return shared_secret

    def get_socket_rx(self):
        conn, addr = self.sock.accept()
    # connection happened
        with conn:
            print(f"socket connection from {addr}")
            while True:
                # todo recv vs. recvmsg?
                data = conn.recv(1024)
                if data:
                    print(f'data from epc, {data}')
                    # conn.send(bytes("heres a secret", "utf-8"))
                    ss = self.get_shared_secret(data)
                    # TODO: truncate to 48b
                    print('sending shared secret' , bytes(hex(ss).encode('utf-8')[2:]) )
                    conn.send(bytes(hex(ss).encode('utf-8')[2:]))
                    return conn

    def wait_for_rx(self):
        conn = self.get_socket_rx()
        while self.connection is None:
            try:
                print(f'Waiting for new subscriber SNID')
                self.connection = self.get_socket_rx()

            finally:
                self.connection.close()
                self.connection = None

    def send_socket_tx(byte_data):
        code = self.sock.sendall(byte_data)
        print(f"Sent shared secret to epc; ret code: {code}")
        return

    def close_socket(self):
        self.connection.close()