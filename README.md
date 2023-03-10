# IPHydra: a fork of ndn-hydra

IPHydra is a fork of [ndn-hydra](https://github.com/justincpresley/ndn-hydra) with two additional features:

- Ability to insert/fetch IP links to data instead of exclusively files
- Hosting nodes as IP servers via nginx

## Setup

1. Follow the same procedure as setting up ndn-hydra: [link to ndn-hydra docs](https://ndn-hydra.readthedocs.io/src/install.html)
2. Be able to use the 'globus-url-copy' command. On Ubuntu I found this to be easiest with: 
   ``sudo apt install globus-gass-copy-progs``
3. Optionally, install nginx to host data over IP. An nginx.conf example file is provided.