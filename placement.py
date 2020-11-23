#Python script to perform placement step of the netlist
#Places the I/O nodes on the boundaries of the silicon area
#Does placement considering a standard cell layout

import matplotlib
import matplotlib.pyplot as plt

#function to classify nodes as input, gate or output
def classify_nodes(fname1):
    fhclassify = open(fname1, 'r')
    ips = []
    gates = []
    ops = []
    left = []
    right = []

    for line in fhclassify:
        line = line.split()
        left.append(line[0])
        right.append(line[1])
    #for

    for i in range(len(left)):
        if (right[i] not in left and right[i] not in ips):
            ips.append(right[i])
        #if

        if (left[i] not in right and left[i] not in ops):
            ops.append(left[i])
        #if

        if (right[i] in left and right[i] not in gates):
            gates.append(right[i])
        #if

        if (left[i] in right and left[i] not in gates):
            gates.append(left[i])
        #if
    #for

    fhclassify.close()
    return ips, gates, ops
#classify_nodes

#function to calculate the sizes of the gates
def calc_gate_sizes(gates, fname1):
    fhsize = open(fname1, 'r')
    sizes = {}

    for i in gates:
        sizes[i] = 0
    #for

    for line in fhsize:
        line = line.split()

        if (line[0] in sizes):
            sizes[line[0]] += 1
        #if

        if (line[1] in sizes):
            sizes[line[1]] += 1
        #if
    #for

    for gate in sizes:
        if (sizes[gate] % 2 != 0):
            sizes[gate] += 1
        #if

        sizes[gate] /= 2
        sizes[gate] = int(sizes[gate])
    #for

    fhsize.close()
    return sizes
#calc_gate_sizes

#function to calculate the length of each row
def calc_row_len(gate_sizes, io_count):
    total_len = 0
    max_size = 0

    for gate in gate_sizes:
        total_len += gate_sizes[gate]

        if (gate_sizes[gate] > max_size):
            max_size = gate_sizes[gate]
        #if
    #for

    if (io_count % 4 == 0):
        lr_pin_count = io_count / 4
    #if

    else:
        lr_pin_count = (int(io_count / 4)) +1
    #else

    row_count = lr_pin_count + 1
    row_len = (int(total_len / row_count)) + 1 + max_size
    return row_len, row_count
#calc_row_len

#function to calcutate the dimensions of rectangular area
def calc_dimensions(row_len, row_count):
    h = (row_count * 5) + ((row_count + 1) * 19)  #3 tracks between rows
    w = (row_len * 5) + (2 * 29)  #5 tracks on both sides
    return h, w
#calc_dimensions

#function to calculate next I/O coordinate with given last coordinate and dimensions
def calc_next_io_coordinate(last_coordinate, h, w):
    if (last_coordinate[0] == 0):
        if (last_coordinate[1] + 36 < h):
            next_coordinate = [0, last_coordinate[1] + 24]
        #if

        else:
            next_coordinate = [int(w/4), h]
        #else
    #if

    elif (last_coordinate[1] == h):
        if (last_coordinate[0] + (1.5 * int(w/4)) < w):
            next_coordinate = [last_coordinate[0] + int(w/4), h]
        #if

        else:
            next_coordinate = [w, h - 33]
    #elif

    elif (last_coordinate[0] == w):
        if (last_coordinate[1] - 36 > 0):
            next_coordinate = [w, last_coordinate[1] - 24]
        #if

        else:
            next_coordinate = [w - int(w/4) - 1, 0]
        #else
    #elif

    else:
        next_coordinate = [last_coordinate[0] - int(w/4), 0]
    #else

    return next_coordinate
#calc_next_io_coordinate

#function to place I/O nodes at the boundaries
def place_io(ips, ops, row_len, row_count):
    h, w = calc_dimensions(row_len, row_count)
    ip_placed_count = 0
    op_placed_count = 0
    ip_count = len(ips)
    op_count = len(ops)
    io_placement = {}
    last_coordinate = [0, 10]

    for ip in ips:
        io_placement[ip] = calc_next_io_coordinate(last_coordinate, h, w)
        last_coordinate = io_placement[ip]
    #for

    for op in ops:
        io_placement[op] = calc_next_io_coordinate(last_coordinate, h, w)
        last_coordinate = io_placement[op]
    #for

    return io_placement
#place_io

#function to display I/O nodes:
def disp_io(ax, io_placement, ips, ops, h, w):
    ax.set_aspect ((h + 1) / (w + 1))

    for io in io_placement:
        is_io = False

        if (io in ips):
            box_colour = 'black'
            is_io = True
        #if

        elif (io in ops):
            box_colour = 'brown'
            is_io = True
        #elif

        if (is_io):
            rect = matplotlib.patches.Rectangle((io_placement[io][0], io_placement[io][1]), 1, 1, color = box_colour, ec = 'black')
            ax.add_patch(rect)
        #if
    #for

    plt.xlim([0, w+1])
    plt.ylim([0, h+1])
#disp_io

#function to calculate cost if a gate is placed in the given coordinate
def calc_cost(fname1, gate, coordinate, node_placement):
    fhcost = open(fname1, 'r')
    cost = 0

    for line in fhcost:
        line = line.split()

        if (gate == line[0]):
            if (line[1] in node_placement):
                cost += (abs(coordinate[0] - node_placement[line[1]][0])) + (abs(coordinate[1] - node_placement[line[1]][1]))
            #if

            else:
                cost += 100
            #else
        #if

        elif (gate == line[1]):
            if(line[0] in node_placement):
                cost += (abs(coordinate[0] - node_placement[line[0]][0])) + (abs(coordinate[1] - node_placement[line[0]][1]))
            #if

            else:
                cost += 100
            #else
        #elif
    #for

    fhcost.close()
    return cost
#calc_cost

#function to calculate the next coordinate to place gates
def calc_next_gate_coordinate(last_coordinate, last_size, w):
    if (last_coordinate[0] + (last_size * 5) + 54 > w):
        next_coordinate = [29, last_coordinate[1] + 24]
    #if

    else:
        next_coordinate = [last_coordinate[0] + (last_size * 5), last_coordinate[1]]
    #else

    return next_coordinate
#calc_next_gate_coordinate

#function to place gates in on the silicon area
def place_gates(gate_sizes, gates, node_placement, fname1, w):
    last_coordinate = [29, 19]
    temp_gates = gates

    for i in range(len(gates)):
        min_cost = calc_cost(fname1, temp_gates[0], last_coordinate, node_placement)
        min_index = 0

        for j in range(len(temp_gates)):
            current_cost = calc_cost(fname1, temp_gates[j], last_coordinate, node_placement)
            if(current_cost < min_cost):
                min_cost = current_cost
                min_index = j
            #if
        #for

        node_placement[temp_gates[min_index]] = last_coordinate
        last_size = gate_sizes[temp_gates[min_index]]
        last_coordinate = calc_next_gate_coordinate(last_coordinate, last_size, w)
        del temp_gates[min_index]
    #for
#place_gates

#function to display all nodes
def disp_nodes(ax, fname2, node_placement, gate_sizes, ips, h, w):
    fhdisp = open(fname2, 'r')
    disp_io(ax, node_placement, ips, ops, h, w)

    for line in fhdisp:
        line = line.split()

        if (len(line) == 7):
            if (line[6] == '>sa1'):
                if (line[0] in gate_sizes):
                    if (line[2] == 'not'):
                        box_colour = 'red'
                    #if

                    if (line[2] == 'nand'):
                        box_colour = 'blue'
                    #if

                    if (line[2] == 'nor'):
                        box_colour = 'green'
                    #if

                    if (line[2] == 'and'):
                        box_colour = 'yellow'
                    #if

                    if (line[2] == 'xor'):
                        box_colour = 'pink'
                    #if

                    rect = matplotlib.patches.Rectangle((node_placement[line[0]][0], node_placement[line[0]][1]), 5 * gate_sizes[line[0]], 5, color = box_colour, ec = 'black')
                    ax.add_patch(rect)
                #if
            #if
        #if
    #for

    fhdisp.close()
#disp_nodes

fname1 = 'connections.txt'
fname2 = 'netlist.isc'
fname3 = 'layout.txt'
print('Classifying nodes as inputs, gates, or outputs...')
ips, gates, ops = classify_nodes(fname1)
io_count = len(ips) + len(ops)
print('Calculating sizes of gates (in units of (fan-ins + fan-outs)/2...)')
gate_sizes = calc_gate_sizes(gates, fname1)
row_len, row_count = calc_row_len(gate_sizes, io_count)
print('Placing I/O nodes on the boundary sequentially...')
node_placement = place_io(ips, ops, row_len, row_count)
print('I/O placement done.\n')
h, w = calc_dimensions(row_len, row_count)
fig1 = plt.figure()
ax = fig1.add_subplot(111)
disp_io(ax, node_placement, ips, ops, h, w)
plt.title('After completing sequential placement of I/O nodes at the boundaries')
print('Placing the gates in rows (semi-custom design) to minimize cost...')
print('[Cost = sum of manhatten distances between the nodes each node is connected to]')
place_gates(gate_sizes, gates, node_placement, fname1, w)
print('Gates placement done.\n')
fig2 = plt.figure()
ax = fig2.add_subplot(111)
plt.title('After completing placement of all nodes in semi-custom design.')
disp_nodes(ax, fname2, node_placement, gate_sizes, ips, h, w)
print('Writing layout data in layout.txt...')
fh = open(fname3, 'w')

for node in node_placement:

    if (node in gates):
        s = node + ' ' + str(node_placement[node][0]) + ' ' + str(node_placement[node][0]) + ' ' + gate_sizes[node] + '\n'
    #if

    elif (node in ips):
        s = node + ' ' + str(node_placement[node][0]) + ' ' + str(node_placement[node][0]) + ' ' + '0' + '\n'
    #elif

    else:
        s = node + ' ' + str(node_placement[node][0]) + ' ' + str(node_placement[node][0]) + ' ' + '-1' + '\n'
    #else

    fh.write(s)
#else
print('Placement completed.')
fh.close()
plt.show()
