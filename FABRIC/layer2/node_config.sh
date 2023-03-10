#!/bin/bash

# This script installs the libraries and runs the setup required to run IPHydra on Fabric

echo "Starting node config..."

node_name=$1
node_ip=$2
ip1=$3
ip2=$4
ip3=$5
ip4=$6
apt_get_args="-y -q"

echo "- Parameters -"
echo "Node name: $node_name"
echo "IP: $node_ip"
echo "IPs: $ip1 $ip2 $ip3"

# Python install
echo "================="
echo "Installing python..."
echo "================="
sudo apt install software-properties-common
sudo apt-get update
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install $apt_get_args python3.9 python3-pip python3.9-dev python3.9-distutils python3.9-venv python3-pip sqlite3 nginx
sudo pip3 install --upgrade pip

# NDN setup
echo "================="
echo "Installing NDN..."
echo "================="
sudo apt-get install $apt_get_args software-properties-common
sudo add-apt-repository -y ppa:named-data/ppa
sudo apt-get update
sudo apt-get install $apt_get_args nfd ndn-tools
ndnsec key-gen /$(whoami) | ndnsec cert-install -
nfdc strategy set /hydra/group /localhost/nfd/strategy/multicast

nfdc face create udp4://$ip1 persistency permanent 
nfdc face create udp4://$ip2 persistency permanent
nfdc face create udp4://$ip3 persistency permanent
nfdc face create udp4://$ip4 persistency permanent

nfdc route add /node1 udp4://$ip1
nfdc route add /node2 udp4://$ip2
nfdc route add /node3 udp4://$ip3
nfdc route add /node4 udp4://$ip4

nfdc route add /hydra udp4://$ip1
nfdc route add /hydra udp4://$ip2
nfdc route add /hydra udp4://$ip3
nfdc route add /hydra udp4://$ip4

nfdc route add /client udp4://$ip1
nfdc route add /client udp4://$ip2
nfdc route add /client udp4://$ip3
nfdc route add /client udp4://$ip4

nfd-start

# Clone repo
echo "================="
echo "Cloning repo..."
echo "================="
git clone --branch IP-Hydra https://github.com/nick-mynatt/ndn-hydra.git
cd ndn-hydra
python3.9 -m venv venv
. venv/bin/activate
pip3 install -e .
pip3 install numpy

# ndn-svs 'Face' import fix
cp ~/svs_base.py /home/ubuntu/ndn-hydra/venv/lib/python3.9/site-packages/ndn/svs/svs_base.py
cp ~/svs_thread.py /home/ubuntu/ndn-hydra/venv/lib/python3.9/site-packages/ndn/svs/svs_thread.py
cp ~/svs_base_thread.py /home/ubuntu/ndn-hydra/venv/lib/python3.9/site-packages/ndn/svs/svs_base_thread.py
cp ~/svs_shared_thread.py /home/ubuntu/ndn-hydra/venv/lib/python3.9/site-packages/ndn/svs/svs_shared_thread.py

# Create run script
cat <<EOF > run.sh
#!/bin/bash
cd ndn-hydra
. venv/bin/activate
python3.9 examples/repo.py -rp /hydra -i "${node_ip}" -n "${node_name}"
EOF

sudo cp run.sh /home/ubuntu/

echo "Configuration done."