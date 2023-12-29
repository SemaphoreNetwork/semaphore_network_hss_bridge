import argparse

parser = argparse.ArgumentParser(description = "CLI for Semaphore Network Registration")
 
# add argument
parser.add_argument("register-proivder-pub", nargs = '*', metavar = "public key", type = str,
                     help = "uncompressed public key to register with")
 
# parse the arguments from standard input
args = parser.parse_args()


def trigger(pubkey):
    print('triggered', pubkey)
    # check if add argument has any input data.
    # If it has, then print sum of the given numbers
    if len(args.register-provider-pub) != 0:
        trigger(args.register-provider-pub)