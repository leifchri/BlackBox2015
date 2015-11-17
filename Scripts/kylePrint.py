file_path = 'C:\Users\Leif Christiansen\Documents\BlackBox\scripts\TestFiles'

file_name = file_path + "\\" + "BBTestQ1_1x1000.txt"

#print("Reading " + file_name)

f = open(file_name, 'r')

f2 = open('kylePrint.txt', 'w')

state = ''
for line in f: 
    if (line == '\n'):
        f2.write(state + '\n')
        state = ''
    else:
        state += line.replace('\n','')
f2.close()