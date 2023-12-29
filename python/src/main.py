import sys
import json
import account
import hss
import secrets
import auth_socket
import config
from web3 import Web3

from threading import Thread

def sigint_handler(conn):
    print("killing process")
    conn.close()
    sys.exit()

#async thread
def hss_thread():
    s_hss = hss.SemaphoreNetworkHSS()
    return Thread(target=s_hss.hss_loop())

def auth_thread(socket_target):
    return Thread(target=socket_target.wait_for_rx())

def main():
    # socket
    conf = config.getConfig()

    web3 = Web3(Web3.HTTPProvider(conf['rpc_url']))
    default_account = web3.eth.account.from_key(conf['hss_private_key'][2:])

    #instantiate the HSS with default "Provider" account. 
    socket = auth_socket.SemaphoreNetworkAuthSocket(default_account)

    # todo kill/interrupt not being handled properly
    try:
        print(f'Starting Semaphore Network HSS')
        hss_t = hss_thread()
        hss_t.start()

        print(f'Opening socket thread:')
        auth_t = auth_thread(socket)

        # hss_t.join()
        auth_t.join()

    except KeyboardInterrupt:
        print(f'Caught Exit, Killing')
        socket.close_socket()
        sys.exit()

    except Exception:
        print(f'Unhandled Exception, Killing')
        socket.close_socket()
        hss_t.close_socket()
        sys.exit()


if __name__ == "__main__": 
    main()