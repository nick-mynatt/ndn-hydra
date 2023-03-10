nfd-stop
rm ~/.ndn/repo/hydra/* -r
ndnsec delete nick
ndnsec key-gen /$(whoami) | ndnsec cert-install -
nfdc strategy set /hydra/group /localhost/nfd/strategy/multicast
nfd-start