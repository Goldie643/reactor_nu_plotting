# arg 1 is E spectrum 1
# arg 2 is E spectrum 2

# geoneutrinos.org reactor info is in TNU per keV
# 1 event/10e32 free protons/year

import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

width = 9.995-1.805 # width of the data
n_p_o = 8 # n protons in Oxygen
n_p_h = 1 # n protons in Hydrogen

u = 1.6605402e-27 # 1 atomic mass unit in kg

m_o = 15.999*u
m_h = 1*u

m_water = 2*m_h+m_o # kg

m_sk = 22.5e6 # kg (FV)

n_water_sk = m_sk/m_water

n_p_sk = n_water_sk*(n_p_o + n_p_h)

print("N protons in SK = %f\n" % n_p_sk)

# I could've done all the above elsewhere
# and put the number here
# but that aint how I roll

geo_1_data = [] 

with open (sys.argv[1]) as in_file_1:
    reader = csv.reader(in_file_1)
    for row in reader:
        dat_row = []
        try:
            for data in row:
                dat_row.append(float(data))
        except ValueError:
            print('Skipping header...')
            continue
        geo_1_data.append(dat_row[:])
        del dat_row[:]

geo_2_data = [] 

with open (sys.argv[2]) as in_file_2:
    reader = csv.reader(in_file_2)
    for row in reader:
        dat_row = []
        try:
            for data in row:
                dat_row.append(float(data))
        except ValueError:
            print('Skipping header...')
            continue
        geo_2_data.append(dat_row[:])
        del dat_row[:]

geo_1_sums = [sum(x) for x in zip(*geo_1_data)]
geo_2_sums = [sum(x) for x in zip(*geo_2_data)]

# Geo neutrinos file format:
# 0 - energy
# 1 - total
# 2 - all standard reactors
# 3 - closest reactor
# 4 - custom reactor
# 5 - geo_1_u
# 6 - geo_1_th

# print("Total (TNU/(%f keV)) = %f" % (geo_1_sums[1],width))
# print("Total (TNU) = %f" % (geo_1_sums[1]*width))
# print("Total (#interactions in SK/y) = %f" % (geo_1_sums[1]*width*(n_p_sk/10e32)))
geo_1_n = (geo_1_sums[2]+geo_1_sums[4])*width*(n_p_sk/10e32)
geo_2_n = (geo_2_sums[2]+geo_2_sums[4])*width*(n_p_sk/10e32)
geo_geo_n = (geo_1_sums[5]+geo_1_sums[6])*width*(n_p_sk/10e32)

geo_1_energy = [row[0] for row in geo_1_data]
# geo_1_reactor = [row[2]+row[4] for row in geo_1_data]
geo_1_reactor = [(row[2]+row[4])*width*(n_p_sk/10e32) for row in geo_1_data]
# geo_1_geo = [row[2]+row[4]+row[5]+row[6] for row in geo_1_data]
geo_1_geo = [(row[5]+row[6])*width*(n_p_sk/10e32) for row in geo_1_data]

geo_2_energy = [row[0] for row in geo_2_data]
# geo_2_reactor = [row[2]+row[4] for row in geo_2_data]
geo_2_reactor = [(row[2]+row[4])*width*(n_p_sk/10e32) for row in geo_2_data]
# geo_1_geo = [row[2]+row[4]+row[5]+row[6] for row in geo_1_data]
geo_2_geo = [row[5]+row[6] for row in geo_2_data]

print(sum(geo_1_reactor))
print(sum(geo_2_reactor))

chi_2 = [(x-y)*(x-y) for x,y in zip(geo_1_reactor,geo_2_reactor)]
chi_2 = sum(chi_2)
print("Chi^2 = %f" % chi_2)

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.grid(color='k',alpha=0.2)

ax1.fill_between(geo_2_energy,geo_2_reactor,color='r',alpha=0.5,label='2018 (Total = %0.1f)' % geo_1_n)
ax1.fill_between(geo_1_energy,geo_1_reactor,color='b',alpha=0.5,label='2018 + 2010 Kashiwazaki (Total = %0.1f)' % geo_2_n)
ax1.fill_between(geo_1_energy,geo_1_geo,color='g',alpha=0.5,label='Geo-neutrinos (Total = %0.1f)' % geo_geo_n)
ax1.set_ylabel('SK interaction rate/y')
ax1.set_xlabel('Neutrino energy/MeV')

# ax1.plot([],[],alpha=0,label=('2018 Reactors:                   %0.1f'% geo_1_n))
# ax1.plot([],[],alpha=0,label=('2018+2010 Kashiwazaki 6 & 7: %0.1f'% geo_2_n))

# ax1.set_aspect(50)
ax1.legend(loc='center right')

plt.show()
