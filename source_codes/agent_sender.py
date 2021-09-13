import socket
import sys
import agent_collector
import json
import time 

def main(argv):
    '''
    Usage: python3 agent_sender {SERER_IP} {SERVER_PORT} {NET_IFACE}
    '''
    HOST = argv[1]  # server IP
    PORT = argv[2]  # server port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
        #try:
        print(f'Connecting to {HOST}:{PORT}...')
        skt.connect((HOST, int(PORT)))
        print(f'Connected ! ')
        while(True):
            try:
                data = agent_collector.get_util(iface=argv[3])
                print('data', data)     
                skt.sendall(str.encode(json.dumps(data)))
                time.sleep(1)
            except( KeyboardInterrupt ):
                skt.close()
                break
        #except:
            #print('Connection error!!')

main(sys.argv)


