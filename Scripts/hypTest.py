'''
Created on Sep 17, 2015
A program to gather data from the Black Box webpage

Changes this version: Color codes are integers not strings. 
Because of this the output to text is not as pretty.

Tests a hypothesis for Q4 and computes the average time
a pixel spends being Red and being Orange

igraph could work for the graphing
@author: leifchri
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import scipy

'''
Changes the airport codes into numbers 
0:Black 1:Gray 2:Blue 3:Purple 4:Cyan 5:Green 6:Red 7:Orange 8:Pink 9:White
'''
def getColorCode(color):
    #Black
    if color == 'gru':
        return 0
    #Gray
    if color == 'pty':
        return 1
    #Blue
    if color == 'jfk':
        return 2
    #Purple
    if color == 'lax':
        return 3
    #Cyan
    if color == 'las':
        return 4
    #Green
    if color == 'lis':
        return 5
    #Red
    if color == 'bru':
        return 6
    #Orange
    if color == 'hkg':
        return 7
    #Pink
    if color == 'icn':
        return 8
    #White
    if color == 'mex':
        return 9

BASE_URL = 'http://www.informatics.indiana.edu/rocha/blackbox/BlackBox.php'

def testHypQ3(oldFrame, frame):
    return
    '''for i in range(10):
        for j in range(10):
            if (oldFrame[i][j] == 0):
                if (frame[i])'''

'''
Tests the hypotheses, within quadrant 4 Black only goes to Red, Red only goes to Orange, and Orange only goes to Black.
And even number colors chane to orange and odd number colors change to black.
Also, updates the arrays tracking the lifespans of red and orange pixels
'''
def testHypQ4(oldFrame, frame, count, lifeSpan, step):
    for i in range(10):
        for j in range(10):
            #print str(i) + " " + str(j)
            if (oldFrame[i][j] == 0): #if black
                if ((frame[i][j] != 0) and (frame[i][j] != 6)): #if not black and not red
                    print "Step: " + str(step) + " Black has gone to " + str(frame[i][j])
                    print " at position " + str(i) + " " + str(j)
            if (oldFrame[i][j] == 6): #if red
                if (frame[i][j] == 6): #if still red
                    count[i][j] = count[i][j] + 1.0
                elif (frame[i][j] == 7): #if changed to orange
                    lifeSpan[0] = lifeSpan[0]+1.0
                    lifeSpan[1] = lifeSpan[1] + count[i][j] 
                    #print "A Red changed after " + str(count[i][j])
                    count[i][j] = 0.0
                    #print "Current average time spent red: " + str(lifeSpan[1]/lifeSpan[0])
                else:
                    print "Step: " + str(step) +" Red has gone to " + str(frame[i][j])
                    print " at position " + str(i) + " " + str(j)
            if (oldFrame[i][j] == 7): #if orange
                if (frame[i][j] == 7):
                    count[i][j] = count[i][j] + 1.0
                elif (frame[i][j] == 0):
                    lifeSpan[2] = lifeSpan[2] + 1.0
                    lifeSpan[3] = lifeSpan[3] + count[i][j]
                    #print "An Orange changed after " + str(count[i][j])
                    count[i][j] = 0.0
                    #print "Average time spent orange: " + str(lifeSpan[3]/lifeSpan[2])                
                else:
                    print "Step: " + str(step) + " Orange has gone to " + str(frame[i][j])   
                    print " at position " + str(i) + " " + str(j)
        if((oldFrame[i][j] == 2) or (oldFrame[i][j] == 4) or (oldFrame[i][j] == 8)): #if blue, cyan, or pink
            if ((frame[i][j] != oldFrame[i][j]) and (frame[i][j] != 7)):
                print "Step: " + str(step) + str(oldFrame[i][j]) + " has gone to " + str(frame[i][j])
                print " at position " + str(i) + " " + str(j)
        if((oldFrame[i][j] == 1) or (oldFrame[i][j] == 3) or (oldFrame[i][j] == 5) or (oldFrame[i][j] == 9)): #if gray, purple, green, or white 
            if ((frame[i][j] != oldFrame[i][j]) and (frame[i][j] != 0)):
                print "Step: " + str(step) + str(oldFrame[i][j]) + " has gone to " + str(frame[i][j])
                print " at position " + str(i) + " " + str(j)

def countEdges(oldFrame, frame, edges):
    for i in range(10):
        for j in range(10):
            if (oldFrame[i][j] != frame[i][j]):
                p0 = oldFrame[i][j]
                p1 = frame[i][j]
                if (p0 == 0):
                    index = p0*9 + p1
                else:
                    index = p0*9 + p1%p0
                edges[index] = edges[index] + 1

'''
Opens the Black Box webpage, inputs a given n, clicks Next n Step numReps times, 
and outputs each frame to BBTest('nStep'x'numReps').txt. 
BBTest.txt has each frame stored starting from the top left cell, moving left to right
and top to bottom. There is a line break between each frame.
FYI the program clicks ~3.33 times a second or ~200 clicks per minute 
'''
def main():
    nStep = input('Enter n: ')
    numReps = input('Enter the number of times to click Next n Step: ')
    
    #Open the Black Box webpage
    driver = webdriver.Firefox()
    driver.get(BASE_URL)
    #Input the given n
    ele = driver.find_element_by_name("cycles")
    ele.send_keys(str(nStep))
    ele.send_keys(Keys.RETURN)
    
    #Opens four text files, one for each quadrant
    fq1 = open('BBTestQ1_' + str(nStep) + 'x' + str(numReps) + '.txt','w')
    fq2 = open('BBTestQ2_' + str(nStep) + 'x' + str(numReps) + '.txt','w')
    fq3 = open('BBTestQ3_' + str(nStep) + 'x' + str(numReps) + '.txt','w')
    fq4 = open('BBTestQ4_' + str(nStep) + 'x' + str(numReps) + '.txt','w')
    fs = [fq1, fq2, fq3, fq4]
        
    '''lifeSpan is the array used to store the total time pixels have spent red
    or orange and how many pixel have been tracked of each color.
    lifeSpan[0] = 'number of red counted'
    lifeSpan[1] = 'total time spent as red'
    lifeSpan[2] = 'number of orange counted'
    lifeSpan[3] = 'total time spent as red'
    '''
    lifeSpan = [0,0,0,0] 
    count = []
    for i in range(10):
        count.append([])
        for j in range(10):
            count[i].append(0.0)

    edges = [];
    for i in range(90):
        edges.append(0)
        
    oldFrame = []

    #Extract the color information for each cell in teh frame and write it to BBTest.txt
    for i in range(0,numReps): #counts the number of matrices to be generated which specifies nrows for frequency matrix
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table')
        rows = table.find_all('tr')  
        
        for f in fs:
            f.write("Step: " + str(i) + "\n")
           
        frame = []
        p = 0 #counts current row
        for row in rows:
            q = 0 #counts current column
            data = []
            for ele in row.find_all('td'):
                data.append(getColorCode(ele['class'][0])) #will return the number code for each color
                q = q + 1
            if (p < 10):
                fq1.write(str(data[:10]) + "\n")
                fq2.write(str(data[10:20]) + "\n")
                frame.append(data[10:20])
            else:
                fq3.write(str(data[:10]) + "\n")
                fq4.write(str(data[10:20]) + "\n")
            p = p + 1
            
        for f in fs:
            f.write("\n")
            
        driver.find_element_by_xpath("//*[@id='controls']/form/button").click()
    
        if (i!=0):
            testHypQ3(oldFrame, frame)
            #countEdges(oldFrame, frame, edges)
            #testHypQ4(oldFrame, frame, count, lifeSpan, i)
        oldFrame = frame
        
        #print lifeSpan
        
        #prints the count matrix prettily
        ''''s = [[str(e) for e in row] for row in count]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print '\n'.join(table)''' 
    
    for f in fs:
        f.close()
    #driver.close()
    #print edges
    totalEdges = 0
    for i in range(len(edges)):
        totalEdges = totalEdges + edges[i]
    for i in range(10):
        print str(i) + "--> "
        for j in range(10):
            if (i != j):
                if (i != 0):
                    index = i*9 + j%i
                else:
                    index = i*9 + j
                print "[" + str(j) + "]" + ": ",
                print ("%.2f" % (1.0*edges[index]/totalEdges)),
        print
    '''print lifeSpan
    try:
        print "Average time spent Red: " + str(lifeSpan[1]/lifeSpan[0])
    except ZeroDivisionError:
        print "No Reds measured"
    try:
        print "Average time spent Orange: " + str(lifeSpan[3]/lifeSpan[2])
    except ZeroDivisionError:
        print "No Oranges measured"'''

main()