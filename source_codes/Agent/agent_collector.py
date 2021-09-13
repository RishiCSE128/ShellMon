import time
import agent_accumulator as accumulator
import pprint

pp = pprint.PrettyPrinter(indent=2)  # debug

def run_util_collection(exit_iface, timer=1):
    '''
    runs an indefinite loop colelcting node_util data
    Params
        1. timer : positive interger sets collection timer
        2. exit_interface : network interface name that sends data out   
    '''
    node_util = accumulator.get_util()
    temp = {
                'source' : node_util['network'][exit_iface]['addr']['ip4'],  #ipv4 addr of the exit_iface 
                't_stamp' : time.ctime(),
                'node_util' : node_util
        }

    #pp.pprint(temp)  # debug    
    return temp       

#debug
'''
def main():
    run_util_collection(exit_iface='Wi-Fi')

main()
'''