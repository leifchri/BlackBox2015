# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
"""
BUG: Numpy can take negative indices so all the try/excepts in the test* are wrong
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
from colorama import init
from colorama import Fore, Back, Style

current_mat = np.zeros((10, 10))
prev_mat = np.zeros((10, 10))
write_curr = 0
write_prev = 0
edges = []
numStep = 0
mutCount = []

def testHyp1(k):
    #if ( (prev_mat[k[0]][k[1]] == 2) and (current_mat[k[0]][k[1]] == 5) ):
        #printMats(k)
    if (prev_mat[k[0]][k[1]] == 2):
        st = ''
        num0 = 0
        numAdj = 0
        for i in range(3):
            for j in range(3):
                if ( ((k[0]-1+i) >= 0) and ((k[1]-1+j) >=0) and ((k[0]-1+i) < 10) and ((k[1]-1+j) < 10) ):
                    if ( (i == 1) and (j == 1) ):
                        #print Fore.RED,
                        st1 = "*" + str(int(prev_mat[k[0]-1+i][k[1]-1+j]))
                        #print st1,
                    else:
                        #print Fore.WHITE,
                        st1 = str(int(prev_mat[k[0]-1+i][k[1]-1+j]))
                        #print " " + st1,
                else:
                    st1 = ''
                st += " " + st1
                if (st1 == '0'):
                    num0+=1
                if (st1 != ''):
                    numAdj+=1
            st += "\n"

        total = 0
        numCount = 0
        if ((numAdj - num0) < 2):
            #print st.replace(" *", "*")
            printMats(k)
            raw_input("press enter to continue")


def testHyp2(k):
    #if ( (prev_mat[k[0]][k[1]] == 5) or ((prev_mat[k[0]][k[1]]%2) == 0) ):
    dif = int(current_mat[k[0]][k[1]]) - int(prev_mat[k[0]][k[1]])
    if dif < 0:
        dif += 10
    print "Step: ", numStep, " ", int(prev_mat[k[0]][k[1]]), " changed to ", int(current_mat[k[0]][k[1]]), " dif: ", dif
    oldC = prev_mat[k[0]][k[1]]
    newC = current_mat[k[0]][k[1]]

    mutCount[k[0]][k[1]] += 1

    #if ( (k[0] == 1) and (k[1] == 0) ):
    #    print int(prev_mat[k[0]][k[1]]), " changed to ", int(current_mat[k[0]][k[1]])

    if( (oldC == 2) and (newC == 0)):
        '''
        st = ''
        num0 = 0
        numAdj = 0
        for i in range(3):
            for j in range(3):
                if ( ((k[0]-1+i) >= 0) and ((k[1]-1+j) >=0) and ((k[0]-1+i) < 10) and ((k[1]-1+j) < 10) ):
                    if ( (i == 1) and (j == 1) ):
                        #print Fore.RED,
                        st1 = "*" + str(int(prev_mat[k[0]-1+i][k[1]-1+j]))
                        #print st1,
                    else:
                        #print Fore.WHITE,
                        st1 = str(int(prev_mat[k[0]-1+i][k[1]-1+j]))
                        #print " " + st1,
                else:
                    st1 = ''
                st += " " + st1
                if (st1 == '0'):
                    num0+=1
                if (st1 != ''):
                    numAdj+=1
            st += "\n"'''
        
        
        '''try:
            p0 = prev_mat[k[0]-1][k[1]]
        except:
            p0 = 0
        try:
            p1 = prev_mat[k[0]][k[1]-1]
        except:
            p1 = 0
        try:
            p2 = prev_mat[k[0]+1][k[1]]
        except:
            p2 = 0
        try:
            p3 = prev_mat[k[0]][k[1]+1]
        except:
            p3 = 0

        print("Sum of adj: " + str((p0+p1+p2+p3)%10)),'''
        #print("Product of adj: " + str((p0*p1*p2*p3)%10)),
        '''
        #printMats(k)
        total = 0
        numCount = 0
        if ((numAdj - num0)==1):
            for row in prev_mat:
                for ele in row:
                    total += ele
                    if (ele != 0):
                        numCount += 1
            print "Total Sum: " + str(total) + " numCount: " + str(numCount)
            printMats(k)
        '''
        #    print st.replace(" *", "*")
        #raw_input('press enter to continue')

count = []
for i in range(10):
    count.append(0)
def testHyp3(k):
    oldC = prev_mat[k[0]][k[1]]
    newC = current_mat[k[0]][k[1]]
    # if a color goes to black and isn't white and has no blacks adjacent
    if ( (newC == 3)):
        try:
            p0 = prev_mat[k[0]-1][k[1]]
        except:
            p0 = 1
        try:
            p1 = prev_mat[k[0]][k[1]-1]
        except:
            p1 = 1
        try:
            p2 = prev_mat[k[0]+1][k[1]]
        except:
            p2 = 1
        try:
            p3 = prev_mat[k[0]][k[1]+1]
        except:
            p3 = 1
        count[int(p0)]+=1
        count[int(p1)]+=1
        count[int(p2)]+=1
        count[int(p3)]+=1
        print("Product of adj: " + str(p0*p1*p2*p3)),
        print("Current count: "),
        print(count)
        printMats(k)
        #raw_input("press enter to coninue")
    '''if (newC != 0):
        return
    try:
        p0 = prev_mat[k[0]-1][k[1]]
    except:
        p0 = 10
    try:
        p1 = prev_mat[k[0]][k[1]-1]
    except:
        p1 = 10
    try:
        p2 = prev_mat[k[0]+1][k[1]]
    except:
        p2 = 10
    try:
        p3 = prev_mat[k[0]][k[1]+1]
    except:
        p3 = 10
    if ( ((p0 != newC) or (p0 == 10)) and ((p1 != newC) or (p1 == 10)) and ((p2 != newC) or (p2 == 10)) and ((p3 != newC) or (p3 == 10)) ):
        printMats(k)
        raw_input("press any key to continue")
    '''

    # a color changes to a color not shared by an adjacent pixel
    '''if ( (newC == 0) or (newC == 9) ):
        return
    try:
        p0 = prev_mat[k[0]-1][k[1]]
    except:
        p0 = 10
    try:
        p1 = prev_mat[k[0]][k[1]-1]
    except:
        p1 = 10
    try:
        p2 = prev_mat[k[0]+1][k[1]]
    except:
        p2 = 10
    try:
        p3 = prev_mat[k[0]][k[1]+1]
    except:
        p3 = 10
    if ( ((p0 != newC) or (p0 == 10)) and ((p1 != newC) or (p1 == 10)) and ((p2 != newC) or (p2 == 10)) and ((p3 != newC) or (p3 == 10)) ):
        printMats(k)
        raw_input("press any key to continue")'''

def printMats(k):
        print "Step: " + str(numStep)
        print int(prev_mat[k[0]][k[1]]), " changed to ", int(current_mat[k[0]][k[1]]),
        print "at row: " + str(k[0]) + " col: " + str(k[1])
        print '--------------------------------------'
        print 'PRINTING the previous matrix'
        for i in range(10):
            for j in range(10):
                if ( (i == k[0]) and (j == k[1]) ):
                    print Fore.RED,
                else:
                    print Fore.WHITE,
                print str(int(prev_mat[i][j])),
            print ''
        print '\n'
        print '--------------------------------------'
        print 'PRINTING the current matrix'
        for i in range(10):
            for j in range(10):
                if ( (i == k[0]) and (j == k[1]) ):
                    print Fore.RED,
                else:
                    print Fore.WHITE,
                print str(int(current_mat[i][j])),
            print ''
        print '\n'
        print '--------------------------------------'

def printEdges():
    # print the number of edges between i --> j
    p = 0
    for i in range(10):
        print str(i) + "--> "
        for j in range(10):
            if (i != j):
                '''if (p0 < p1):
                    index = p0*9 + p1 - 1
                else:
                    index = p0*9 + p1'''
                print "[" + str(j) + "]" + ": ",
                print ("%.2f" % (1.0*edges[p])),
                p += 1
        print

def plotNetwork(show, save, test_file):  
    G = nx.DiGraph()

    p = 0
    for i in range(10):
        for j in range(10):
            if (i == j):
                continue 
            G.add_edge(str(i), str(j), weight = edges[p])
            p = p+1
    
    vert = '9'
    edge_labels = dict([((u,v,),d['weight'])
                     for (u,v,d) in G.edges(data=True) if  u == vert])
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if u == vert]
    val_map = {'0':(0,0,0),
               '1':(0.5,0.5,0.5),
               '2':(0,0,1),
               '3':(1,0,1),
               '4':(0,1,1),
               '5':(0,0.5,0),
               '6':(1,0,0),
               '7':(1,0.65,0),
               '8':(1,0.75,0.8),
               '9':(1,1,1)
               }
    labels =  {'0':'0',
               '1':'1',
               '2':'2',
               '3':'3',
               '4':'4',
               '5':'5',
               '6':'6',
               '7':'7',
               '8':'8',
               '9':'9'
               }
    values = [val_map.get(node) for node in G.nodes()]

    fig = plt.figure()

    pos=nx.circular_layout(G) # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G,pos,node_size=700, node_color=values)
    nx.draw_networkx_labels(G,pos,labels,font_size=16)

    # edges
    nx.draw_networkx_edges(G,pos,edgelist=esmall)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)

    fig.canvas.set_window_title(test_file.replace(".txt",".png")) 

    plt.title(test_file)
    plt.axis('off')
    if(show): 
        plt.show()
    if(save):
        plt.savefig("from" + vert + test_file.replace(".txt",".png"), dpi = 500)


init()

file_path = 'C:\Users\Leif Christiansen\Documents\BlackBox\scripts\TestFiles'
#test_file = '\BBTestQ2_1x1000_2015-10-02_15-43.txt'
#file_name = file_path +  test_file 

file_name = ''

for file in os.listdir(file_path):
    for i in range(10):
        mutCount.append([])
        for j in range(10):
            mutCount[i].append(0)
    
    if (file.endswith(".txt") and file.startswith("BBTestQ2")):
        current_mat = np.zeros((10, 10))
        prev_mat = np.zeros((10, 10))
        write_curr = 0
        write_prev = 0
        edges = []
        numStep = 0

        file_name = file_path + "\\" + file

        print("Reading " + file_name)

        f = open(file_name, 'r')

        for i in range(90):
            edges.append(0)

        obs = []
        for i in range(10):
            obs.append(0)

        for i, line in enumerate(f): 
            clean_line = (line.replace(' ', '')).replace('\n', '')
            if ( i>= 10 and clean_line == '' ):#(i+1)%11 == 0):# and write_prev == write_curr -1):
                prev_mat = np.copy(current_mat)
                write_prev = i
                #print 'matrix copied at index: ' , i
            
            #print list(clean_line)
            
            if ((i%11) < 10):
                current_mat[((i)%11)] = list(clean_line)
            if (i%11 == 0):
                write_curr += 1
            if (i== (write_prev+10)):
                #print i
                #print prev_mat == current_mat
                #print 'the induced changes between the current matrix and the previous one are: \n'
                bool_mat = (prev_mat == current_mat)
                changes = zip(*np.where(bool_mat == False))
                for k in changes:
                    #print k
                    #print int(prev_mat[k[0]][k[1]]), " changed to ", int(current_mat[k[0]][k[1]])
                    p0 = int(prev_mat[k[0]][k[1]])
                    p1 = int(current_mat[k[0]][k[1]])
                    if (p0 < p1):
                        index = p0*9 + p1 - 1
                    else:
                        index = p0*9 + p1
                    edges[index] = edges[index] + 1

                    #testHyp1(k)

                    #testHyp2(k)
                    '''if( (int(prev_mat[k[0]][k[1]])%2) == 0 ):
                        print str(numStep) + ": ",
                        print int(prev_mat[k[0]][k[1]]), " changed to ", int(current_mat[k[0]][k[1]]),
                        print "at row: " + str(k[0]) + " col: " + str(k[1])'''
                    
                    # and (int(current_mat[k[0]][k[1]]) != 9)
                    #testHyp3(k)
                    #if( (int(current_mat[k[0]][k[1]]) == 0) ):
                        #printMats(k)        
                    #if( (k[0] < 2) or (k[0] > 7) or (k[1] < 3) or (k[1] > 6) ):
                        #if ( current_mat[k[0]][k[1]] == 1):
                            #printMats(k)
                if (numStep == 0):
                    for i in range(10):
                        for j in range(10):
                            obs[int(prev_mat[i][j])] += 1
                numStep = numStep + 1
        #print

        totalChanges = 0
        for i in range(len(edges)):
            totalChanges = totalChanges + edges[i]

        #print "Total # of changes: " + str(totalChanges)

        '''for i in range(10):
            for j in range(10):
                print mutCount[i][j],
            print '''

        total = edges[18]+edges[21]+edges[23]+edges[25]

        print "Init: ", obs

        print "2 -->"
        print "[0]: " + "%.2f" % (1.0*edges[18]/total),
        print "[4]: " + "%.2f" % (1.0*edges[21]/total),
        print "[6]: " + "%.2f" % (1.0*edges[23]/total),
        print "[8]: " + "%.2f" % (1.0*edges[25]/total)
        print "Total: ", total
        #plotNetwork(0, 1, file)
        
