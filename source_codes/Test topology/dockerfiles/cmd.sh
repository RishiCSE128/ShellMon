echo -e '\nRequeesting IP Address... \c' \
            dhclient -v > /dev/null  && \ 
echo  '[OK]'

echo -e '\nStarting SSH Service... \c' \
            /etc/init.d/ssh start /dev/null &&\
echo '[OK]' 

echo -e '\nAdding user... \c' ;\ 
            useradd -m user1 &&\
echo '[OK]' 

echo '\nUpdating password... \c' ;\
            echo '{user1:password}' | chpasswd &&\
echo '[OK]'

echo '\nAdding user to sudoer group... \c' ;\
            usermod -aG user1 sudo &&\
echo '[OK]'

bash