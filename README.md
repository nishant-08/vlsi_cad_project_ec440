# vlsi_cad_project_ec440
## Course project for EC440: VLSI CAD

### Implemented on Ubuntu 20.04.1. Tested with python3, python3.8.

Completed till Partitioning step of VLSI design cycle.

Files:
1) netlist.isc
   Contains the netlist for 4 bit Fast Adder circuit.

2) netlist_parser.py
   Parses through the netlist (.isc) file and generates a file 'kl_input.txt'
   containing node pairs that have connection between them.

3) kl_partitioning.py
   Reads the file 'kl_input.txt' and performs the KL partitioning algorithms
   on the netlist. The algorithm iterates till the new swap results in more
   number of crossovers or the number of crossovers remain constant for five
   iterations. Also, plots the graph of number of crossovers vs iterations.

Run the following commands in the terminal:

$ python3.8 netlist_parser.py
$ python3.8 kl_partitioning.py

Required Libraries:
> matplotlib

  Install with the command:
  $ sudo apt install python3-matplotlib
