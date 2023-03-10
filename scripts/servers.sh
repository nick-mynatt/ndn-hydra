#!/bin/bash

num=1

while [ $num -le 4 ]; do
  echo "Starting node $num"
  gnome-terminal -- bash -c ". venv/bin/activate; python3 ./examples/repo.py -rp /hydra -n node$num -i '127.0.0.$num:8000'; exec bash"
  echo -n "Working? (y/n)"
  read -n1 input
  echo
  if [ $input == "y" ]; then
    ((num=num+1))
  fi
done

# cd github/ndn-hydra && . venv/bin/activate && python3 ./examples/repo.py -rp /hydra -n node1