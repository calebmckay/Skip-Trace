#!/bin/sh

echo "----------"
echo "Skip Trace Instalation"
echo "----------"

read -p "Is this a client install? [Y/n] " -n 1 install

if [ "$install" == "n" || "$install" == "N" ]; then
    echo "Creating Server Instalation"
    echo "Moving common files to /root"
    sudo cp common/STcommon.py /root/.
    echo "Moving server script to /root"
    sudo cp server/server.py /root/.

    echo "Setting up server locationLog service."
    sudo cp server/locationLog.service /lib/systemd/system/.
    sudo systemctl daemon-reload
    sudo systemctl enable locationLog.service

    sudo python3 /root/STcommon.py -c "0.0.0.0" "3145" "/var/log/skip_trace.log"
else
    echo "Creating Server Instalation"
    echo "Moving common files to /root"
    sudo cp common/STcommon.py /root/.
    echo "Moving server script to /root"
    sudo cp server/server.py /root/.
    
    echo "Creating client locationLog service."
    sudo cp client/locationLog.service /lib/systemd/system/.
    sudo systemctl daemon-reload
    sudo systemctl enable locationLog.service
fi

echo "Exiting"
exit 0
