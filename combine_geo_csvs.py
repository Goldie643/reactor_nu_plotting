# assumes energy hasn't been added (but actually shouldn't matter)
# arg 1 and 2 are files to add
# arg 3 is 2017 baseline
# arg 4 is out_file name

import sys
import csv

def pull_data(file_name):
    dat = []
    print('Pulling data from %s' % file_name)
    with open(file_name) as in_file:
        reader = csv.reader(in_file)
        i = 0
        for row in reader:
            i+=1
            dat_row = []
            # Check if there is data in row
            try:
                try_data=row[0]
            # Finish parsing file if no data
            except:
                print('Hit end of data on line %i, returning...' % i)
                return dat
            # Skipping line if string (header)
            try:
                for data in row:
                    dat_row.append(float(data))
            except ValueError:
                print('Skipping header..')
                continue
            dat.append(dat_row[:])
            del dat_row[:]
    return dat

if __name__ == '__main__':
    mrg_1 = sys.argv[1]
# print(mrg_1)
    mrg_2 = sys.argv[2]
# print(mrg_2)
    base = sys.argv[3]
# print(base)

    if (len(sys.argv) == 4):
        print('Using default out name (geo_combine.csv)')
        out_name = 'geo_combine.csv'
    else:
        out_name = sys.argv[4]

    for i in range(1,3):
        if(sys.argv[i] == out_name):
            print('One of input files is same as output file!')
            print('Exiting...')
            exit()

    dat_1 = pull_data(mrg_1)
    print('%i lines from %s' % (len(dat_1), mrg_1))
    dat_2 = pull_data(mrg_2)
    print('%i lines from %s' % (len(dat_2), mrg_2))
    dat_base  = pull_data(base) 
    print('%i lines from %s' % (len(dat_base), base))

    with open (out_name,'w') as out_file:
        writer = csv.writer(out_file, lineterminator='\n')
        for i in range(len(dat_1)):
            dat_row_merge=[x + y for x,y in zip(dat_1[i],dat_2[i])]
# print(dat_row_merge)
            dat_row_merge_str=["%0.11f" % (x - y) for x,y in zip(dat_row_merge,dat_base[i])]
            writer.writerow(dat_row_merge_str)
        out_file.close()
