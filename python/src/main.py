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
    print("sigint_handler: terminating process.")
    conn.close()
    sys.exit()

# Async thread to run HSS program.
def hss_thread():
    s_hss = hss.SemaphoreNetworkHSS()
    return Thread(target=s_hss.hss_loop())

def auth_thread(socket_target):
    return Thread(target=socket_target.wait_for_rx())

def main():
    conf = config.getConfig()

    web3 = Web3(Web3.HTTPProvider(conf["rpc_url"]))
    default_account = web3.eth.account.from_key(conf["hss_private_key"][2:])

    # Instantiate the HSS with default "Provider" account.
    socket = auth_socket.SemaphoreNetworkAuthSocket(default_account)

    # TODO: kill/interrupt not being handled properly
    try:
        print("Starting Semaphore Network HSS.")
        hss_t = hss_thread()
        hss_t.start()

        print("Opening socket thread.")
        auth_t = auth_thread(socket)

        # hss_t.join()
        auth_t.join()

    except KeyboardInterrupt:
        print("Caught exit, terminating HSS program.")
        socket.close_socket()
        sys.exit()

    except Exception as e:
        print(f"Unhandled exception (main):", e)
        print("Terminating HSS program.")
        socket.close_socket()
        hss_t.close_socket()
        sys.exit()


if __name__ == "__main__": 
    main()