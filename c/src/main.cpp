#include <cryptopp/dsa.h>
#include <cryptopp/eccrypto.h>
#include <cryptopp/hex.h>
#include <cryptopp/oids.h>
#include <cryptopp/osrng.h>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
// socket included
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#define PORT 6969

/**@dev returns the 128bit shared secret that will be used for Auth
   @params
        file: mock HSS to read public keys from (this will be RPC to chain HSS
in next feature). idx: index that the "subscribers'" public key is in the
on-chain HSS registry, transmitted during network auth/attach.
**/

std::string CreateSharedSecret(std::string file, int idx) {
  std::string line;
  int lineNumber = 0;

  std::ifstream infile(file);

  while (std::getline(infile, line)) {
    std::istringstream iss(line);
    if (lineNumber == idx) {
      // do key ss derivation with self priv key and this as pub key.
      return line;
    }

    lineNumber++;
  }

  // can even hardcode the return secret here for testing, error rn
  return "0xdeadbeef";
}


int main() {

  // EPC/CN will only need to send the index of it's (full) pubKey in the HSS
  // registry.

  int sock = 0, valread, client_fd;
  struct sockaddr_in serv_addr;
  // todo: get this from the auth/attach initial UE message.
  char *SNSubscriberID = "0";
  char buffer[1024] = {0};
  if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
    printf("\n Socket creation error \n");
    return -1;
  }

  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(PORT);

  // Convert IPv4 and IPv6 addresses from text to binary
  // form
  if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
    printf("\nInvalid address/ Address not supported \n");
    return -1;
  }

  if ((client_fd = connect(sock, (struct sockaddr *)&serv_addr,
                           sizeof(serv_addr))) < 0) {
    printf("\nConnection Failed \n");
    return -1;
  }
  send(sock, SNSSubscriberID, strlen(SNSSubscriberID), 0);
  printf("Subscriber index sent:\n");

  valread = read(sock, buffer, 1024);
  printf("Got shared secret for subscriber %s\n", buffer);

  // closing the connected socket
  // close(new_socket);

  // closing the listening socket
  // shutdown(server_fd, SHUT_RDWR);

  return 0;
}

