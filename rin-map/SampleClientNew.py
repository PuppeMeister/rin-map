from __future__ import print_function
import socket
import ssl
import sslpsk2

#PSKS = {b'server1' : b'abcdef',
#        b'server2' : b'uvwxyz'}

PSKS = {b'server1' : b'true',
        b'identity' : b'uvwxyz',
        b'value' : b'231.27:232.63:14.98:205.0:212.04'}

def client(host, port, psk):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((host, port))

    ssl_sock = sslpsk2.wrap_socket(tcp_socket,
                                  ssl_version=ssl.PROTOCOL_TLSv1,
                                  ciphers='ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH',
                                  psk=lambda hint: (PSKS[hint], b'client1'))
#                                 psk=lambda hint: PSKS[hint])

    msg = "ping"
    ssl_sock.sendall(msg.encode())
    msg = ssl_sock.recv(4).decode()
    print('Client received: %s'%(msg))

    ssl_sock.shutdown(socket.SHUT_RDWR)
    ssl_sock.close()

def main():
    host = '127.0.0.1'
    port = 6000
    client(host, port, PSKS)

if __name__ == '__main__':
    main()
