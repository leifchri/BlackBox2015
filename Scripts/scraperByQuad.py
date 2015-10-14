'''
Created on Sep 17, 2015
A program to gather data from the Black Box webpage
@author: leifchri
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import scipy
import time

'''
Changes the airport codes into numbers 
0:Black 1:Gray 2:Blue 3:Purple 4:Cyan 5:Green 6:Red 7:Orange 8:Pink 9:White
'''
def getColorCode(color):
    #Black
    if color == 'gru':
        return '0' 
    #Gray
    if color == 'pty':
        return '1'
    #Blue
    if color == 'jfk':
        return '2'
    #Purple
    if color == 'lax':
        return '3'
    #Cyan
    if color == 'las':
        return '4'
    #Green
    if color == 'lis':
        return '5'
    #Red
    if color == 'bru':
        return '6'
    #Orange
    if color == 'hkg':
        return '7'
    #Pink
    if color == 'icn':
        return '8'
    #White
    if color == 'mex':
        return '9'

BASE_URL = 'http://www.informatics.indiana.edu/rocha/blackbox/BlackBox.php'

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
    
    timestr = time.strftime("%Y%m%d-%H%M%S")

    fq1 = open('BBTestQ1_' + str(nStep) + 'x' + str(numReps) + timestr + '.txt','w')
    fq2 = open('BBTestQ2_' + str(nStep) + 'x' + str(numReps) + timestr + '.txt','w')
    fq3 = open('BBTestQ3_' + str(nStep) + 'x' + str(numReps) + timestr + '.txt','w')
    fq4 = open('BBTestQ4_' + str(nStep) + 'x' + str(numReps) + timestr + '.txt','w')
    fs = [fq1, fq2, fq3, fq4]
    
    #freq_matrix = [[0 for j in xrange(10)] for j in xrange(numReps)]#initializes the frequency matrix colomns are fixed to 10 i.e. number of colors
                                                                    #nrows are specified by # of repetitions.
    
    #with open('BBTestQ1_' + str(nStep) + 'x' + str(numReps) + '.txt','w') as fq1, open('BBTestQ2_' + str(nStep) + 'x' + str(numReps) + '.txt','w') as fq2:
    freq_mat = np.zeros((10, numReps))
            
    #Extract the color information for each cell in teh frame and write it to BBTest.txt
    for i in range(0,numReps): #counts the number of matrices to be generated which specifies nrows for frequency matrix
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table')
        rows = table.find_all('tr')
        p = 0
        for row in rows:
            q = 0 
            data = ""
            for ele in row.find_all('td'):
                #print row.find_all('td')                
                data = data + " " + getColorCode(ele['class'][0]) #will return the number code for each color
                #freq_matrix[int(i)][int(getColorCode(ele['class'][0]))] +=  1
                if (p < 10):
                    if (q > 9):
                        freq_mat[int(getColorCode(ele['class'][0]))][int(i)] += 1
                #print 'color_code: ', getColorCode(ele['class'][0])            
                q = q + 1
            if (p < 10):
                fq1.write(data[:20] + "\n")
                fq2.write(data[20:40] + "\n")
            else:
                fq3.write(data[:20] + "\n")
                fq4.write(data[20:40] + "\n")
            p = p + 1
            #print 'matrix: ', i
        for f in fs:
            f.write("\n")
        driver.find_element_by_xpath("//*[@id='controls']/form/button").click()
        
    for f in fs:
        f.close()
    driver.close()
    freq_mat /= 100
    return freq_mat, numReps, nStep

freq_matrix, numReps, nStep = main()
f1 = open('frequency_mat.txt', 'w')
for i in range(10):
    l=''
    for j in range(len(freq_matrix[0])):
        l = l + str(freq_matrix[i][j]) + '\t'
    f1.write(l + "\n")
f1.close()
plt.gca().set_color_cycle(['k', 'grey', 'blue', 'purple', 'cyan', 'g', 'red', 'orange', 'pink', 'yellow'])
for i in range(10):
    plt.plot(freq_matrix[i])
plt.legend(['black', 'grey', 'blue', 'purple', 'cyan', 'green' , 'red', 'orange', 'pink', 'white' ], loc = 'upper left', prop = {'size':8})
plt.xlabel("Number Of Steps")
plt.ylabel("Number of Occurances")
plt.yticks(scipy.arange(0,1,.1))
plt.savefig('BBTestQ1_'+str(nStep)+'x'+str(numReps)+'.png', dpi = 500)
#plt.show()