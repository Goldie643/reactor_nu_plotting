# arg 1 is input file WITHOUT energies
# arg 2 is output file WITH energies
# arg 3 is minimum energy bin
# arg 4 is maz energy bin

import sys
import csv

try:
    e_min = float(sys.argv[3])
except:
    e_min = 1.8
try:
    e_max = float(sys.argv[4])
except:
    e_max = 10
width = 0.01 #MeV

e = e_min

with open (sys.argv[1]) as in_file:
    with open (sys.argv[2], 'wb') as out_file:
        reader = csv.reader(in_file)
        writer = csv.writer(out_file, lineterminator='\n')
        i=0
        for row in reader:
            i+=1
            try:
                try_data = row[0]
            except:
                print('Hit end of data on line %i, returning...' % i)
                exit()
            try:
                header_test = float(row[0])
            except ValueError:
                'Skipping header...'
                continue
            writer.writerow([e] + row)
            e+=width
