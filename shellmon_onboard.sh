red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
blue=`tput setaf 4`
magenta=`tput setaf 5`
cyan=`tput setaf 6`
reset=`tput sgr0`


clear
echo -e "${green}Enter the management interface... ${reset}\c"
read iface

echo Initializing....
sudo apt -y update > /dev/null 2>&1
sudo apt -y install figlet git > /dev/null 2>&1
clear
echo ${cyan}
echo =======================================================
echo ${magenta}
figlet Welcome to ShellMon
echo Developped By SuITELab LSBU
echo ${cyan}
echo =======================================================
echo ${green}
echo -e '\n\tPress any key to start onboarding...'
read temp
echo ${rest}
cd /home/pi/Documents > /dev/null 2>&1
mkdir git > /dev/null 2>&1
cd git 2>&1

echo -e '\nOnboarding....\n'

echo ${cyan}
git clone https://github.com/RishiCSE128/ShellMon.git
echo ${reset}

x=`ifconfig $iface | grep "inet" | head -1`; ip_addr=`echo $x | cut -d " " -f 2`
echo -e "\n${yellow}API endpoint : ${cyan} https://$ip_addr:5000/node_util/all/$iface ${reset}\n" 
dt=`date`
echo -e "\n [ $dt ] Telemetry status [ ${green} ONLINE ${reset} ]\n"
cd ShellMon
python3 source_codes/Agent/agent_sender.py
dt=`date`
echo -e "\n[ $dt ]Telemetry status [ ${red} OFFLINE ${reset} ]"
