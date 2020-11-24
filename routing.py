#Python script to perform routing on the layout done in placement step

import matplotlib
import matplotlib.pyplot as plt

from placement import node_placement
from placement import ips
from placement import ops
from placement import gates
from placement import gate_sizes

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

#function to build connection matrix
def build_connection_matrix(fname, h, w):
    fh = open(fname, 'r')
    connection_matrix = [[0 for i in range(w + 1)] for j in range(h + 1)]

    for line in fh:
        line = line.split()

        for i in range(len(line)):
            line[i] = int(line[i])
        #for

        connection_matrix[line[2]][line[1]] = line[0]  #given block

        if (line [3] == 0 or line[3] == -1):  #for I/0
            if (line[1] != w):  #going clockwise, starting from right
                connection_matrix[line[2]][line[1] + 1] = line[0]
            #if

            if (line[2] != 0):
                connection_matrix[line[2] - 1][line[1]] = line[0]
            #if

            if (line[1] != 0):
                connection_matrix[line[2]][line[1] - 1] = line[0]
            #if

            if (line[2] != h):
                connection_matrix[line[2] + 1][line[1]] = line[0]
            #if
        #if

        else:
            for i in range(7):
                for j in range(2 + (5 * line[3])):
                    if (line[1] != 29 and j == 0):
                        continue
                    #if

                    if (i == 0 or i == 6):
                        if (j == 0 or j == 1 + (5 *line[3])):
                            continue
                        #if
                    #if

                    connection_matrix[line[2] + (i - 1)][line[1] + (j - 1)] = line[0]
                #for
            #for
        #else
    #for

    fh.close()
    return connection_matrix
#build_connection_matrix

#function to check if any adjacent block has count lower by 1
def check_predecessor(r, c, count, path_grid):
    h = 139
    w = 173
    found = False
    i = r
    j = c + 1

    if (i >= 0 and i <= h and j >= 0 and j <= w):
        if (path_grid[i][j] == count - 1):
            found = True
        #if
    #if

    i = r - 1
    j = c

    if (i >= 0 and i <= h and j >= 0 and j <= w):
        if (path_grid[i][j] == count - 1):
            found = True
        #if
    #if

    i = r
    j = c - 1

    if (i >= 0 and i <= h and j >= 0 and j <= w):
        if (path_grid[i][j] == count - 1):
            found = True
        #if
    #if

    i = r + 1
    j = c

    if (i >= 0 and i <= h and j >= 0 and j <= w):
        if (path_grid[i][j] == count - 1):
            found = True
        #if
    #if

    return found
#check_predecessor

#function to check alignment only h-v cross allowed apart from free flow
def check_alignment(i, j, path_grid, hvcn_matrix):
    if (hvcn_matrix[i][j] == 'c'):
        return False
    #if

    if (hvcn_matrix[i][j] == 'n'):
        return True
    #if

    if (hvcn_matrix[i][j] == 'h'):
        if (path_grid[i - 1][j] == path_grid[i][j] - 1):
            return True
        #if

        if (path_grid[i + 1][j] == path_grid[i][j] - 1):
            return True
        #if
    #if

    if (hvcn_matrix[i][j] == 'v'):
        if (path_grid[i][j - 1] == path_grid[i][j] - 1):
            return True
        #if

        if (path_grid[i][j + 1] == path_grid[i][j] - 1):
            return True
        #if
    #if

    return False
#check_alignment

#function to get the route from source to target
def get_route(source, target, connection_matrix, hvcn_matrix, h, w):
    path_grid = [[-1 for i in range(w + 1)] for i in range(h + 1)]
    count = 1
    target_reached = False
    path = []

    for i in range(h + 1):
        for j in range(w + 1):
            if (connection_matrix[i][j] == source):
                path_grid[i][j] = 0
            #if

            elif (connection_matrix[i][j] != target and connection_matrix[i][j] != 0):
                path_grid[i][j] = -2
            #elif
        #for
    #for

    while (True):
        for i in range(h + 1):
            for j in range(w + 1):
                if (path_grid[i][j] == -1):
                    if (check_predecessor(i, j, count, path_grid)):
                        if(check_alignment(i, j, path_grid, hvcn_matrix)):
                            path_grid[i][j] = count

                            if (connection_matrix[i][j] == target):
                                target_coordinate = [i, j]
                                target_reached = True
                                break
                            #if
                        #if
                    #if
                #if
            #for

            if (target_reached == True):
                break
            #if
        #for

        if (target_reached == True):
            break
        #if

        count += 1
    #while

    while (count != 0):
        path.append(target_coordinate)
        i = target_coordinate[0]
        j = target_coordinate[1] + 1

        if (i >= 0 and i <= h and j >= 0 and j <= w):
            if (path_grid[i][j] == count - 1):
                target_coordinate = [i, j]
                count -= 1
                continue
            #if
        #if

        i = target_coordinate[0] - 1
        j = target_coordinate[1]

        if (i >= 0 and i <= h and j >= 0 and j <= w):
            if (path_grid[i][j] == count - 1):
                target_coordinate = [i, j]
                count -= 1
                continue
            #if
        #if

        i = target_coordinate[0]
        j = target_coordinate[1] - 1

        if (i >= 0 and i <= h and j >= 0 and j <= w):
            if (path_grid[i][j] == count - 1):
                target_coordinate = [i, j]
                count -= 1
                continue
            #if
        #if

        i = target_coordinate[0] + 1
        j = target_coordinate[1]

        if (i >= 0 and i <= h and j >= 0 and j <= w):
            if (path_grid[i][j] == count - 1):
                target_coordinate = [i, j]
                count -= 1
                continue
            #if
        #if
    #while

    path.append(target_coordinate)
    return path
#get_route

#function to update connection matrix
def update_connection_matrix(connection_matrix, current_path, source):
    for i in range(len(current_path)):
        r = current_path[i][0]
        c = current_path[i][1]
        connection_matrix[r][c] = source

        if (c < 173):
            connection_matrix[r][c + 1] = source
        #if

        if (r > 0 and c < 173):
            connection_matrix[r - 1][c + 1] = source
        #if

        if (r > 0):
            connection_matrix[r - 1][c] = source
        #if

        if (r > 0 and c > 0):
            connection_matrix[r - 1][c - 1] = source
        #if

        if (c > 0):
            connection_matrix[r][c - 1] = source
        #if

        if (r < 139 and c > 0):
            connection_matrix[r + 1][c - 1] = source
        #if

        if (r < 139):
            connection_matrix[r + 1][c] = source
        #if

        if (r < 139 and c < 173):
            connection_matrix[r + 1][c + 1] = source
        #if
    #for
#update_connection_matrix

#function to update hvcn matrix
def update_hvcn_matrix(hvcn_matrix, current_path):
    h = 139
    w = 173

    for i in range(len(current_path)):
        r = current_path[i][0]
        c = current_path[i][1]
        coming = 'o'
        going = 'o'

        if (i != 0):
            if (r == current_path[i - 1][0]):
                coming = 'h'
            #if

            else:
                coming = 'v'
            #else
        #if

        if (i != len(current_path) - 1):
            if (r == current_path[i + 1][0]):
                going = 'h'
            #if

            else:
                going = 'v'
            #else
        #if

        if ((coming == 'h' and going == 'v') or (coming == ' v' and going == 'h')):
            hvcn_matrix[r][c] = 'c'

            if (r > 0):
                hvcn_matrix[r - 1][c] = 'c'
            #if

            if (r < h):
                hvcn_matrix[r + 1][c] = 'c'
            #if

            if (c > 0):
                hvcn_matrix[r][c - 1] = 'c'
            #if

            if (c < w):
                hvcn_matrix[r][c + 1] = 'c'
            #if

            if (r > 0 and c > 0):
                hvcn_matrix[r - 1][c - 1] = 'c'
            #if

            if (r > 0 and c < w):
                hvcn_matrix[r - 1][c + 1] = 'c'
            #if

            if (r < h and c > 0):
                hvcn_matrix[r + 1][c - 1] = 'c'
            #if

            if (r < h and c < w):
                hvcn_matrix[r + 1][c + 1] = 'c'
            #if
        #if

        elif (hvcn_matrix[r][c] == 'c'):
            continue
        #elif

        elif (coming == 'h' or going == 'h'):
            hvcn_matrix[r][c] = 'h'

            if (r > 0):
                hvcn_matrix[r - 1][c] = 'h'
            #if

            if (r < h):
                hvcn_matrix[r + 1][c] = 'h'
            #if
        #elif

        elif (coming == 'v' or going == 'v'):
            hvcn_matrix[r][c] = 'v'

            if (c > 0):
                hvcn_matrix[r][c - 1] = 'v'
            #if

            if (c < w):
                hvcn_matrix[r][c + 1] = 'v'
            #if
        #elif
    #for
#update_hvcn_matrix

#function to do entire routing
def do_routing(fname, connection_matrix, hvcn_matrix, h, w):
    fh = open(fname, 'r')
    paths = []
    count = 1

    for line in fh:
        line = line.split()
        line[0] = int(line[0])
        line[1] = int(line[1])
        current_path = get_route(line[1], line[0], connection_matrix, hvcn_matrix, h, w)
        print(count)
        update_hvcn_matrix(hvcn_matrix, current_path)
        update_connection_matrix(connection_matrix, current_path, line[1])
        paths.append(current_path)
        count += 1
    #for

    fh.close()
    return paths
#do_routing

#function to display routing
def disp_all(ax, fname, node_placement, paths, gate_sizes, ips, h, w):
    disp_nodes(ax, fname, node_placement, gate_sizes, ips, h, w)

    for i in range(len(paths)):
        for j in range(len(paths[i])):
            if (j != 0):
                if (paths[i][j][0] == paths[i][j - 1][0]):
                    dir = 'h'
                #if

                else:
                    dir = 'v'
                #else
            #if

            else:
                if (paths[i][j][0] == paths[i][j + 1][0]):
                    dir = 'h'
                #if

                else:
                    dir = 'v'
                #else
            #else

            if (dir == 'h'):
                box_colour = 'red'
            #if

            else:
                box_colour = 'blue'
            #else

            rect = matplotlib.patches.Rectangle((paths[i][j][1], paths[i][j][0]), 1, 1, color = box_colour)
            ax.add_patch(rect)
        #for
    #for
#disp_all

fname1 = 'connections.txt'
fname2 = 'layout.txt'
fname3 = 'netlist.isc'
h = 139
w = 173
connection_matrix = build_connection_matrix(fname2, h, w)
hvcn_matrix = [['n' for i in range(w + 1)] for j in range(h + 1)]
paths = do_routing(fname1, connection_matrix, hvcn_matrix, h, w)
fig1 = plt.figure()
ax = fig1.add_subplot()
plt.title('After routing.')
disp_all(ax, fname3, node_placement, paths, gate_sizes, ips, h, w)
plt.show()
