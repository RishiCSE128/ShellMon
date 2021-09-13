echo 'Updating ketnel...' ; \
    apt -y update > /dev/null && \
echo '[OK]'

echo 'Installing packages...' ; \
    apt -y install  openssh-server \
                    net-tools \
                    iputils-ping \
                    sudo \
                    nano \
                    isc-dhcp-client > /dev/null && \
echo '[OK]'
    
echo 'Installing Python3 and packages... ' ;\
    apt -y install  python3 \
                    python3-pip > /dev/null && \
    echo 'Python3 Installed. Now installing Python Packages... ' ;\
    pip install psutil \
                flask > \dev\null &&\
echo '[OK]'