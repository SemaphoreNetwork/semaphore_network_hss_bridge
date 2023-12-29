# Semaphore Network HSS Plugin

## What
This repo contains the provider-side plugin that provides the **bridge** between the on-chain Semaphore HSS registry and the cellular backend. 

Current Services

* Provides Authentication for Semaphore Network Subscribers (by SNID) given the on-chain HSS Contract


## How

See "Usage"; A python "server" runs alongside an active forked instance of srsEPC (srsRAN project) [link]

* provides access to on chain objects, including registry of subscriber public keys through UNIX socket to the EPC/CN
* creates shared ECDH key using above to be used in cellular AKA procedure.


## Usage

### Configuration
To run the python plugin you will have to create a config.json and place it in the root directory.

The format is as follows
```
{
  "rpc_url": "<SEPOLIA RPC URL>",
  "hss_address":"0x48138B8486bc6095Dd90F7baA72C199593aa2c56",
  "private_key": "<HSS Private Key>",
  "socket_port": "6969"
}
```
### Basic Instantation:
Run:
```
python3 python/src/main.py
```

Test:
```
python3 python/src/test.py 
```


## Future/Other BoH Implementation
* example code included in "c" directory to add to other EPC/CN codebases, see below
## Semaphore Network  Integration Test 
Included in the "c" directory is a simple integration test/example for including the Semaphore Network Auth procedure. 

### Compilation/Installation/Running

Prerequisites to compile server-side

```
apt install libcrypto++-dev
```

Make and Run (g++)
```
cd build
./build_run_shim.sh
```













