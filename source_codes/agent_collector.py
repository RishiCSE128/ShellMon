import psutil as ps
import pprint


def get_cpu_freq():
    temp = ps.cpu_freq(percpu=True)[0]
    return {'current' :temp[0], 'min': temp[1], 'max': temp[2] }

def get_cpu_util():
    temp = ps.cpu_percent(interval=1, percpu=True)
    return {'per_core_util' : temp, 'mean_util' : round(sum(temp)/len(temp) , 4)}

def get_mem_info():
    temp = ps.virtual_memory()
    return {'total_mb': round(temp[0]/(1024*1024), 4), 'util':temp[2]}

def get_iface_info():
    nic_result={}

    for iface in ps.net_if_stats().keys():   # for each interface 
        stat  = ps.net_if_stats()[iface]     # stat : state, duplex, speed, mtu
        addr =  ps.net_if_addrs()[iface]     # addr : ip, mask, mac
        count = ps.net_io_counters(pernic=True)[iface]  # counter : 

        nic_result[iface] = {
            'stats': {
                'state' : stat[0],
                'duplex' : stat[1],
                'speed' : stat[2],
                'mtu': stat[3]
            },
            'addr': {
                'mac' : addr[0][1],
                'ip4' : addr[1][1],
                'mask': addr[1][2]
            },
            'counter' : {
                'byte' : { 'tx' : count[0], 'rx' : count[1]},
                'packet' : { 'tx' : count[2], 'rx' : count[3]},
                'error' : {'tx' : count[5], 'rx' : count[4]},
                'drop' : { 'tx' : count[7], 'rx' : count[6] }
            }
        }

    return nic_result

def get_util():
    print()
    node_util = {
        'cpu' : {
            'util': get_cpu_util(),
            'freq': get_cpu_freq(),
            'core_count' : ps.cpu_count(),
        },
        'memory': get_mem_info(),
        'network': get_iface_info()
    }
    print(node_util)
    return node_util 


def main():
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(get_util())


main()

'''
if __name__ == '__main__':
    main()
'''



