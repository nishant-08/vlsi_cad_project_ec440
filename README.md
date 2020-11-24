# vlsi_cad_project_ec440
## Course project for EC440: VLSI CAD

### Implemented on Ubuntu 20.10. Tested with python3, python3.8.

Completed till Placement step of VLSI design cycle.


Files:
1) netlist.isc

   Contains the netlist for 4 bit Fast Adder circuit.

2) netlist_parser.py

   Parses through the netlist (.isc) file and generates a file 'connections.txt'
   containing node pairs that have connection between them. It also creates new
   nodes dedicated to the module outputs (absent in the netlist (.isc) file).
   Currently, only works for the given file (supports parsing through a small
   subset of syntax of the netlist).

3) kl_partitioning.py

   Reads the file 'connections.txt' and performs the KL partitioning algorithms
   on the netlist. The algorithm stops iterating when the new swap results in
   more number of crossovers or the number of crossovers remain constant for
   five iterations. Also, plots the graph of number of crossovers vs iterations.
   Displays the partitioning before and after applying KL algorithm, clearly
   showing the reduction in number of crossovers.

4) placement.py

   Reads the file 'connections.txt' and performs placement. The I/O nodes are
   placed at the boundary of the silicon area. Displayes the placement after
   I/O nodes placement and after gates placement. Placement is done using
   standard cell layout. So, floorplanning is the same as placement. Also writes
   layout data in 'layout.txt' in the following format:

   <node_number> <x_coordinate> <y_coordinate> <gate_size/0(input)/-1(output)>

5) routing.py

   Reads the file ‘layout.txt’, ‘connections.txt’, and ‘netlist.isc’ to perform
   routing. It uses two matrices to assist in the routing process, i.e.
   connection matrix and hvcn (horizontal-vertical-cross-none) matrix. The
   connection matrix is used to mark the  grid blocks with the nodes they belong
   to. hvcn matrix is used to avoid wrong overappings in the interconnections.

Run the following commands in the terminal:

` $ python3 netlist_parser.py` or ` $ python3.8 netlist_parser.py`

` $ python3 kl_partitioning.py` or ` $ python3.8 kl_partitioning.py`

` $ python3 placement.py` or ` $ python3.8 placement.py`

` $ python3 routing.py` or ` $ python3.8 routing.py`
(Gets stck in an infinite loop while routing one of the connections)

Required Libraries:
- matplotlib

  Install using the command:

  ` # apt install python3-matplotlib`

  or

  ` # apt-get install python3-matplotlib`


- networkx

  Install using the command:

  ` # apt install python3-networkx`

  or

  ` # apt-get install python3-networkx`
