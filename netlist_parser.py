# Python script to parse the .isc netlist file
# and generate a file containing the node pairs that have connection between them.

# This parser only works for the given .isc file in this directory

fname1 = 'netlist.isc'
fname2 = 'connections.txt'
print('Opening file', fname1, 'in read mode...')
fh1 = open(fname1, 'r')
fh2 = open(fname2, 'w')
fanouts={}
print('Parsing through the file', fname1+'...')

for line in fh1:

    parts = line.split()
    l = len(parts)

    if (parts[l - 1] == '>sa1'):
        if (len(parts) == 7):
            node_id = parts[0]
            fanouts[node_id] = []
        #if

        elif (len(parts) == 6):
            fanout_from = ''

            for i in parts[3]:
                if(i.isdigit()):
                    fanout_from = fanout_from + i
                #if

                else:
                    break
                #else
            #for

            fanouts[fanout_from].append(parts[0])
        #elif
    #if

    else:
        for i in parts:
            s = str(node_id)

            for j in fanouts:
                if(i == j or i in fanouts[j]):
                    s = s + ' ' + str(j)
                    break
                #if
            #for

            fh2.write(s + '\n')
        #for
    #else
#for

fh1.close()
fh2.close()
fh2 = open(fname2, 'r')
left = []
right = []

for line in fh2:
    line = line.split()
    left.append(int(line[0]))
    right.append(int(line[1]))
#for

fh2.close()
last_gate = max(max(left), max(right))
ops = []
new_ops = []
fh2 = open(fname2, 'a')

for i in range(len(left)):
    if (left[i] not in right):
        if (left[i] not in ops):
            ops.append(left[i])
    #if
#for

for i in range(len(ops)):
    new_ops.append(last_gate + i + 1)
    s = str(new_ops[i]) + ' ' + str(ops[i]) + '\n'
    fh2.write(s)
#for

fh2.close()
print('Parsing done.')
print('Created file:', fname2, ': stores node pairs that have connection between them.')
