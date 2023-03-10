#!/bin/bash

clear
cd ndn-hydra
. venv/bin/activate

while :
do
    echo "1: query hydra"
    echo "2: insert test file"
    echo "3: fetch test file"
    echo "4: delete test file"
    echo "5: insert uri"
    echo "6: fetch uri"
    read -p "#: " choice
    if [ "$choice" = "1" ]; then
        echo "Running command: python3 ./examples/client.py query -r /hydra -q /files"
        python3 ./examples/client.py query -r /hydra -q /files
    fi
    if [ "$choice" = "2" ]; then
        echo "Running command: python3 ./examples/client.py insert -r /hydra -f /home/a.txt -p ./examples/files/10mb.txt -w 1"
        python3 ./examples/client.py insert -r /hydra -f /home/a.txt -p ./examples/files/10mb.txt -w 1
    fi
    if [ "$choice" = "3" ]; then
        echo "Running command: python3 ./examples/client.py fetch -r /hydra -f /home/a.txt -p ./examples/output/10mb.txt"
        python3 ./examples/client.py fetch -r /hydra -f /home/a.txt -p ./examples/output/10mb.txt
    fi
    if [ "$choice" = "4" ]; then
        echo "Running command: python3 ./examples/client.py delete -r /hydra -f /home/a.txt"
        python3 ./examples/client.py delete -r /hydra -f /home/a.txt
    fi
    if [ "$choice" = "5" ]; then
        echo "Running command: python3 ./examples/client.py uri -r /hydra -f /home/a.txt"
        python3 ./examples/client.py insert -r /hydra -f /home/a.txt -u ""
    fi
    if [ "$choice" = "6" ]; then
        echo "Running command: python3 ./examples/client.py uri -r /hydra -f /home/a.txt"
        python3 ./examples/client.py uri -r /hydra -f /home/a.txt
    fi
    echo ""
done

# Raw commands
# python3 ./examples/client.py insert -r /hydra -f /home/a.txt -p ./examples/files/10mb.txt -w 1
# python3 ./examples/client.py query -r /hydra -q ./files
# python3 ./examples/client.py fetch -r /hydra -f /home/a.txt -p ./examples/output/10mb.txt
# python3 ./examples/client.py delete -r /hydra -f /home/a.txt
