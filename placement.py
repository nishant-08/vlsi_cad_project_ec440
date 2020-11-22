#Python script to perform placement step of the netlist
#Places the I/O nodes on the boundaries of the silicon area
#Does placement considering a standard cell layout

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
    return row_len
#calc_row_len

fname1 = 'connections.txt'
print('Classifying nodes as inputs, gates, or outputs...')
ips, gates, ops = classify_nodes(fname1)
io_count = len(ips) + len(ops)
print('Calculating sizes of gates (in units of (fan-ins + fan-outs)/2...)')
gate_sizes = calc_gate_sizes(gates, fname1)
row_len = calc_row_len(gate_sizes, io_count)
