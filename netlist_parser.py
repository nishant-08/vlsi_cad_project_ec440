# Python script to parse the .isc netlist file
# and generate a file containing the node pairs that have connection between them.

# This parser only works for the given .isc file in this directory

fname1='netlist.isc'
fname2='kl_input.txt'
print('Opening file', fname1, 'in read mode...')
fh1=open(fname1, 'r')
fh2=open(fname2, 'w')
fanouts={}
print('Parsing through the file', fname1+'...')

for line in fh1:

    parts=line.split()
    alpha_found=False
    l=len(parts)

    if(parts[l-1]=='>sa1'):
        if(len(parts)==7):
            node_id=parts[0]
            fanouts[node_id]=[]
        #if ends        
        
        elif(len(parts)==6):
            fanout_from=''
            
            for i in parts[3]:
                if(i.isdigit()):
                    fanout_from=fanout_from+i
                #if ends
                
                else:
                    break
                #else ends
            #for loop ends

            fanouts[fanout_from].append(parts[0])
        #elif ends
    #if ends

    else:
        for i in parts:
            s=str(node_id)

            for j in fanouts:
                if(i==j or i in fanouts[j]):
                    s=s+' '+str(j)
                    break
                #if ends
            #for loop ends
            
            fh2.write(s+'\n')
        #for loop ends
    #else ends
#for loop ends

print('Parsing done.')
print('Created file:', fname2, ': stores node pairs that have connection between them.')
print('Closing opened files...')
fh1.close()    
fh2.close()
