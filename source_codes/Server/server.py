import subprocess
import time
import requests 
import pprint
import sqlite3
import json
import pandas as pd 
import threading
import os

pp =pprint.PrettyPrinter(indent=2)
lock = threading.Lock()
local_store = []     #storing telemetry locally

def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')

def fetch_request(hosts , conn, timer=1):
    """[summary]
    Fetches the node utilization from a host

    Args:
        host (dict): {ip:'x.x.x.x' , 'port' : nn}
        timer (int): default 1 
    """

    while True:
        try:
            for host in hosts:
                response = requests.get(f"https://{host['host_ip']}:{host['port']}/node_util/{host['util_type']}/{host['exit_iface']}",
                                        verify=False
                            )
                #response = requests.get('https://192.168.1.98:5000/node_util/all',verify=False)
                #print(response.content)
                #pp.pprint(response.json())
                #screen_clear()
            
                
                db_insert(connection=conn, 
                            util=response.json(), 
                            iface=host['exit_iface'],
                            lock = lock)
                time.sleep(timer)
                
                #local_store.append(response.json())
                

        except KeyboardInterrupt:
            break
        

        '''
        except AttributeError:
            print('SSL certificate error... ')
            break

        except: 
            print('Error: fetching error... ')
            time.sleep(2)
        '''

def db_init(connection):
    #create master tables
    #with connection.cursor() as cur:
    cur = connection.cursor()
    cur.execute(''' create table if not exists tab_node_util(
                                source text,
                                t_stamp text,
                                cpu_mean_util real,
                                cpu_max_freq real,
                                cpu_core_count integer,
                                mem_vol real,
                                mem_util real,
                                net_iface text,
                                net_iface_state text,
                                net_iface_speed real,
                                net_iface_duplex integer,
                                net_iface_mtu integer,
                                net_iface_mac text,
                                net_iface_ip text,
                                net_iface_mask text,
                                net_iface_byte_tx integer,
                                net_iface_byte_rx integer,
                                net_iface_packet_tx integer,
                                net_iface_packet_rx integer,
                                net_iface_error_tx integer,
                                net_iface_error_rx integer,
                                net_iface_drop_tx integer,
                                net_iface_drop_rx integer
                        )'''
        )
    cur.close()
    
def db_insert(connection, util,iface, lock):
    with lock:
        cur = connection.cursor()
        cur.execute(f'''insert into tab_node_util values(
            "{util['source']}",
            "{util['t_stamp']}",
            { float(util['node_util']['cpu']['util']['mean_util']) },
            { float(util['node_util']['cpu']['freq']['max']) },
            { int(util['node_util']['cpu']['core_count']) },
            { float(util['node_util']['memory']['total_mb']) },
            { float(util['node_util']['memory']['util']) },
            "{iface}",
            "{util['node_util']['network'][iface]['stats']['state']}",
            { float(util['node_util']['network'][iface]['stats']['speed']) },
            { int(util['node_util']['network'][iface]['stats']['duplex']) },
            { int(util['node_util']['network'][iface]['stats']['mtu']) },
            "{util['node_util']['network'][iface]['addr']['mac']}",
            "{util['node_util']['network'][iface]['addr']['ip4']}",
            "{util['node_util']['network'][iface]['addr']['mask']}",
            { int(util['node_util']['network'][iface]['counter']['byte']['tx']) },
            { int(util['node_util']['network'][iface]['counter']['byte']['rx']) },
            { int(util['node_util']['network'][iface]['counter']['packet']['tx']) },
            { int(util['node_util']['network'][iface]['counter']['packet']['rx']) },
            { int(util['node_util']['network'][iface]['counter']['error']['tx']) },
            { int(util['node_util']['network'][iface]['counter']['error']['rx']) },
            { int(util['node_util']['network'][iface]['counter']['drop']['tx']) },
            { int(util['node_util']['network'][iface]['counter']['drop']['rx']) })'''
        )
        cur.execute('commit')
        print('\n\ninserted....')
        cur.close()


def main():
    con = sqlite3.connect('local_db_2.db')
    db_init(connection=con)


    #reading the host file
    '''
    #workinf_dir = subprocess.run(['pwd'], 
                                capture_output=True,
                                text=True, 
                                check=True,
                                shell=True
                    ).stdout.replace('\n','')
    '''
    
    hosts_dict = pd.read_csv(f'source_codes/Server/hosts.csv').transpose().to_dict()
    
    #polulating the hosts list
    hosts=[]
    for k in hosts_dict.keys():
        hosts.append(hosts_dict[k])

    thread_pool = [] 
    lock  = threading.Lock()

    fetch_request(hosts,con)

    '''
    for host in hosts:
        print(host)
        thread_pool.append( threading.Thread(target=fetch_request, args=(host,con, lock)) )
        print(f"Startung SSL thread for {host['username']}@{host['host_ip']}:{host['port']} --> {host['exit_iface']}")
        
    for thread in thread_pool:
        thread.start()
        thread.join()
    '''
main()