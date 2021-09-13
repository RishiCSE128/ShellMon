import socket
import sys
import json

def main(argv):
    PORT = argv[1]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
        try:
            print(f'Starting server...{PORT}')
            skt.bind(('0.0.0.0', int(PORT)))
            print(f'Server started... ')
            skt.listen()
            conn, addr = skt.accept()

            with conn:
                while True:
                    data = conn.recv(1024)
                    print(json.loads(bytes.decode(data)))
        except:
            print(f'Error in server start')

if __name__ == '__main__':
    main(sys.argv)