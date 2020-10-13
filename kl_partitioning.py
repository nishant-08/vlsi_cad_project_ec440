#Python scrript to read the file containing node pairs with connection between them.
#Produces a file with nodes partitioned into two sets with minimal crossing between them.

import matplotlib.pyplot as plt

def calc_cross(a_nodes, b_nodes):
    fhcross=open('kl_input.txt', 'r')
    cross=0
    
    for line in fhcross:
        line=line.split()

        if(line[0] in a_nodes):
            if(line[1] in b_nodes):
                cross+=1
            #if ends
        #if ends
        
        else:
            if(line[1] in a_nodes):
                cross+=1
            #if ends
        #else ends
    #for loop ends

    fhcross.close()
    return cross
#function calc_cross ends

def calc_diff(a_nodes, b_nodes):
    fhdiff=open('kl_input.txt', 'r')
    a_nodes_diff={}
    b_nodes_diff={}

    for i in a_nodes:
        a_nodes_diff[i]=0
    #for loop ends

    for i in b_nodes:
        b_nodes_diff[i]=0
    #for loop ends
    
    for line in fhdiff:
        line=line.split()

        if(line[0] in a_nodes):
            if(line[1] in a_nodes):
                a_nodes_diff[line[0]]-=1
                a_nodes_diff[line[1]]-=1
            #if ends

            else:
                a_nodes_diff[line[0]]+=1
                b_nodes_diff[line[1]]+=1
            #else ends
        #if ends

        else:
            if(line[1] in b_nodes):
                b_nodes_diff[line[0]]-=1
                b_nodes_diff[line[1]]-=1
            #if ends

            else:
                b_nodes_diff[line[0]]+=1
                a_nodes_diff[line[1]]+=1
            #else ends
        #else ends
    #for loop ends

    fhdiff.close()
    return a_nodes_diff, b_nodes_diff
#function calc_diff ends

def swap_nodes(a_nodes, b_nodes, node_a, node_b):
    ind_a=a_nodes.index(node_a)
    ind_b=b_nodes.index(node_b)
    a_nodes[ind_a]=node_b
    b_nodes[ind_b]=node_a
#function swap_nodes ends

fname1='kl_input.txt'
print('Opening file', fname1, 'in read mode...')
fh1=open(fname1, 'r')
nodes=[]
print('Reading file', fname1, 'to generate list of nodes...\n')
for line in fh1:
    line=line.split()
    
    if(line[0] not in nodes):
        nodes.append(line[0])
    #if ends

    if(line[1] not in nodes):
        nodes.append(line[1])
    #if ends
#for loop ends

fh1.close()
l=len(nodes)
a_nodes=nodes[0:int(l/2)]
b_nodes=nodes[int(l/2):l]
print('Initial Partitioning (randomized):\n')
print('Nodes in partition A:\n', a_nodes)
print('\nNodes in partition B:\n', b_nodes)
new_cross_count=calc_cross(a_nodes, b_nodes)
print('Number of crossovers before partitioning:', new_cross_count, '\n')
const_count=0
print('Applying KL algorithm for partitioning the nodes in 2 sets such that there is minimal crossovers between the sets...\n')
crosses=[new_cross_count]

while True:
    old_cross_count=new_cross_count
    a_nodes_diff, b_nodes_diff=calc_diff(a_nodes, b_nodes)
    max_gain_pair=[a_nodes[0], b_nodes[0]]
    max_gain=a_nodes_diff[a_nodes[0]]+b_nodes_diff[b_nodes[0]]

    for i in a_nodes_diff:
        for j in b_nodes_diff:
            if(a_nodes_diff[i]+b_nodes_diff[j]>max_gain):
                max_gain_pair=[i, j]
                max_gain=a_nodes_diff[i]+b_nodes_diff[j]
            #if ends
        #for loop ends
    #for loop ends

    swap_nodes(a_nodes, b_nodes, max_gain_pair[0], max_gain_pair[1])
    new_cross_count=calc_cross(a_nodes, b_nodes)
    crosses.append(new_cross_count)

    if(new_cross_count<old_cross_count):
        const_count=0
    #if ends

    elif(old_cross_count==new_cross_count):
        const_count+=1
        
        if(const_count>=5):
            break
        #if ends
    #elif ends

    else:
        swap_nodes(a_nodes, b_nodes, max_gain_pair[1], max_gain_pair[0])
        break
    #if ends
#while loop ends

print('Final Partitioning (after performing KL partitioning algorithm):\n')
print('Nodes in partition A:\n', a_nodes)
print('\nNodes in partition B:\n', b_nodes)
print('Number of crossovers after partitioning:', calc_cross(a_nodes, b_nodes), '\n')
iterations=[]

for i in range(len(crosses)):
    iterations.append(i)
#for loop ends

plt.plot(iterations, crosses)
plt.xlabel('Number of Iterations')
plt.ylabel('Number of Crossovers Between Partitions')
plt.title('Result of KL Algorithm (for Partitioning)')
plt.show()
