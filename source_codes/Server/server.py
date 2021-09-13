from time import time
import requests 
import pprint
from threading import Thread as th

host = {
    'ip': '127.0.0.1',
    'port': 5000
}

pp =pprint.PrettyPrinter(indent=2)
"""[summary]
    

    Args:
        host ([type] ): [description]
    """
def fetch_request(host: dict , timer=1):
    """[summary]
    Fetches the node utilization from a host

    Args:
        host (dict): {ip:'x.x.x.x' , 'port' : nn}
        timer (int): default 1 
    """

    while True:
        try:
            response = requests.get(f"http://{host['ip']}:{host['port']}/node_util/all")
            #print(response.content)
            pp.pprint(response.json())
            time.sleep(timer)

        except KeyboardInterrupt:
            break

        except: 
            print('Error: fetching error... ')

fetch_request(host=host)