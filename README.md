# IPHydra: a fork of ndn-hydra

IPHydra is a fork of [ndn-hydra](https://github.com/justincpresley/ndn-hydra) with two additional features:

- Ability to insert/fetch IP links to data instead of exclusively files
- Hosting nodes as IP servers via nginx

## Setup

1. Follow the same procedure as setting up ndn-hydra: [link to ndn-hydra docs](https://ndn-hydra.readthedocs.io/src/install.html)
2. Be able to use the 'globus-url-copy' command. On Ubuntu I found this to be easiest with: 
   ``sudo apt install globus-gass-copy-progs``
3. Optionally, install nginx to host data over IP. An nginx.conf example file is provided.

## URI command

URIs can be inserted/fetched with the new client command 'uri'.

Parameters:
- -r repo_name Specify the repo's name.   REQUIRED
- -f file_name Specify the file's name.   REQUIRED
- -u uri       The URI to be inserted.    Optional - for inserting
- -p path      The path for downloading.  Optional - for fetching

### Inserting
``python3 examples/client.py uri -r /hydra -f /sra/test/file.txt -u http://location-of-file.com``

### Fetching
``python3 examples/client.py uri -r /hydra -f /sra/test/file.txt -p /path/to/dest.txt``

## Fabric

An example of IPHydra running on Fabric is given in ./FABRIC. This specific example runs on layer 2 due to routing issues.
