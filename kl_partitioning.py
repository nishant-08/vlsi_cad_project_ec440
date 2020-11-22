#Python script to read the file containing node pairs with connection between them.
#Displays the partitioning before and after applying the KL algorithm.
#Also displays the number of crossovers agains the number of iterations.

import matplotlib.pyplot as plt
import networkx as nx

#function to calculate number of crossovers between partitions
def calc_cross(a_nodes, b_nodes):
    fhcross = open('connections.txt', 'r')
    cross = 0

    for line in fhcross:
        line = line.split()

        if (line[0] in a_nodes):
            if (line[1] in b_nodes):
                cross += 1
            #if
        #if

        elif (line[1] in a_nodes):
            cross += 1
        #elif
    #for

    fhcross.close()
    return cross
#calc_cross

#function to calculate the difference between external and internal connections
def calc_diff(a_nodes, b_nodes):
    fhdiff = open('connections.txt', 'r')
    a_nodes_diff = {}
    b_nodes_diff = {}

    for i in a_nodes:
        a_nodes_diff[i] = 0
    #for

    for i in b_nodes:
        b_nodes_diff[i] = 0
    #for

    for line in fhdiff:
        line = line.split()

        if (line[0] in a_nodes):
            if (line[1] in a_nodes):
                a_nodes_diff[line[0]] -= 1
                a_nodes_diff[line[1]] -= 1
            #if

            else:
                a_nodes_diff[line[0]] += 1
                b_nodes_diff[line[1]] += 1
            #else
        #if

        else:
            if (line[1] in b_nodes):
                b_nodes_diff[line[0]] -= 1
                b_nodes_diff[line[1]] -= 1
            #if

            else:
                b_nodes_diff[line[0]] += 1
                a_nodes_diff[line[1]] += 1
            #else
        #else
    #for

    fhdiff.close()
    return a_nodes_diff, b_nodes_diff
#calc_diff

#function to display the partitions with interconnections
def display_partition(a_nodes, b_nodes):
    fhnetwork = open('connections.txt', 'r')
    g = nx.Graph()
    fixed_positions = {}

    for line in fhnetwork:
        line = line.split()
        g.add_edge(int(line[0]), int(line[1]))
    #for

    for i in range(len(a_nodes)):
        fixed_positions[int(a_nodes[i])] = (-10, i)
    #for

    for i in range(len(b_nodes)):
        fixed_positions[int(b_nodes[i])] = (10, i)
    #for

    fixed_nodes = fixed_positions.keys()
    pos = nx.spring_layout(g, pos = fixed_positions, fixed = fixed_nodes)
    nx.draw(g, pos, with_labels = True)
    fhnetwork.close()
#display_partition

#function to swap given nodes between the two partitions
def swap_nodes(a_nodes, b_nodes, node_a, node_b):
    ind_a = a_nodes.index(node_a)
    ind_b = b_nodes.index(node_b)
    a_nodes[ind_a] = node_b
    b_nodes[ind_b] = node_a
#swap_nodes

fname1 = 'connections.txt'
print('Opening file', fname1, 'in read mode...')
fh1 = open(fname1, 'r')
a_nodes = []
b_nodes = []
print('Reading file', fname1, 'to generate list of nodes...\n')
i = 0

for line in fh1:
    line = line.split()

    if (line[0] not in a_nodes and line[0] not in b_nodes):
        if (i % 2 == 0):
            a_nodes.append(line[0])
        #if

        else:
            b_nodes.append(line[0])
        #else

        i += 1
    #if

    if (line[1] not in a_nodes and line[1] not in b_nodes):
        if (i % 2 == 0):
            a_nodes.append(line[1])
        #if

        else:
            b_nodes.append(line[1])
        #else

        i += 1
    #if
#for

fh1.close()
print('Initial Partitioning (randomized):\n')
print('Nodes in partition A:\n', a_nodes)
print('\nNodes in partition B:\n', b_nodes)
new_cross_count = calc_cross(a_nodes, b_nodes)
print('\nNumber of crossovers before applying KL partitioning algorithm:', new_cross_count, '\n')
plt.figure(1)
plt.title('Before applying KL partitioning algorithm. (Crossovers: ' + str(new_cross_count) + ')')
display_partition(a_nodes, b_nodes)
const_count = 0
print('\nApplying KL algorithm for partitioning the nodes in 2 sets such that there is minimal crossovers between the sets...\n')
crosses = [new_cross_count]

while True:
    old_cross_count = new_cross_count
    a_nodes_diff, b_nodes_diff = calc_diff(a_nodes, b_nodes)
    max_gain_pair = [a_nodes[0], b_nodes[0]]
    max_gain = a_nodes_diff[a_nodes[0]] + b_nodes_diff[b_nodes[0]]

    for i in a_nodes_diff:
        for j in b_nodes_diff:
            if (a_nodes_diff[i] + b_nodes_diff[j] > max_gain):
                max_gain_pair = [i, j]
                max_gain = a_nodes_diff[i] + b_nodes_diff[j]
            #if
        #for
    #for

    swap_nodes(a_nodes, b_nodes, max_gain_pair[0], max_gain_pair[1])
    new_cross_count = calc_cross(a_nodes, b_nodes)
    crosses.append(new_cross_count)

    if (new_cross_count < old_cross_count):
        const_count = 0
    #if

    elif (old_cross_count == new_cross_count):
        const_count += 1

        if (const_count >= 5):
            break
        #if
    #elif

    else:
        swap_nodes(a_nodes, b_nodes, max_gain_pair[1], max_gain_pair[0])
        break
    #else
#while

print('Final Partitioning (after performing KL partitioning algorithm):\n')
print('Nodes in partition A:\n', a_nodes)
print('\nNodes in partition B:\n', b_nodes)
new_cross_count = calc_cross(a_nodes, b_nodes)
print('\nNumber of crossovers after applying KL partitioning algorithm:', new_cross_count, '\n')
plt.figure(2)
plt.title('After applying KL partitioning algorithm. (Crossovers: ' + str(new_cross_count) + ')')
display_partition(a_nodes, b_nodes)
iterations = []

for i in range(len(crosses)):
    iterations.append(i)
#for

plt.figure(3)
plt.plot(iterations, crosses)
plt.xlabel('Number of Iterations')
plt.ylabel('Number of Crossovers Between Partitions')
plt.title('Result of KL Algorithm (for Partitioning)')
plt.show()
