# vlsi_cad_project_ec440
## Course project for EC440: VLSI CAD

### Implemented on Ubuntu 20.04.1, Ubuntu 20.10. Tested with python3, python3.8.

Completed till Partitioning step of VLSI design cycle.


Files:
1) netlist.isc

   Contains the netlist for 4 bit Fast Adder circuit.

2) netlist_parser.py

   Parses through the netlist (.isc) file and generates a file 'kl_input.txt'
   containing node pairs that have connection between them. Currently, only
   works for the given file (supports parsing through a small subset of syntax
   of the netlist).

3) kl_partitioning.py

   Reads the file 'kl_input.txt' and performs the KL partitioning algorithms
   on the netlist. The algorithm stops iterating when the new swap results in
   more number of crossovers or the number of crossovers remain constant for
   five iterations. Also, plots the graph of number of crossovers vs iterations.
   Displays the partitioning before and after applying KL algorithm, clearly
   showing the reduction in number of crossovers.


Run the following commands in the terminal:

` $ python3 netlist_parser.py` or ` $ python3.8 netlist_parser.py`

` $ python3 kl_partitioning.py` or ` $ python3.8 kl_partitioning.py`


Required Libraries:
- matplotlib

  Install using the command:
  
  ` $ sudo apt install python3-matplotlib`

  or

  ` $ sudo apt-get install python3-matplotlib`


- networkx

  Install using the command:

  ` $ sudo apt install python3-networkx`

  or

  ` $ sudo apt-get install python3-networkx`
