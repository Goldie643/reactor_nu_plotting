# arg 1 is E spectrum
# arg 2 is efficiencies

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


geo_data = [] 

with open (sys.argv[1]) as in_file:
    reader = csv.reader(in_file)
    for row in reader:
        dat_row = []
        for data in row:
            dat_row.append(float(data))
        geo_data.append(dat_row[:])
        del dat_row[:]

geo_sums = []
geo_sums = [sum(x) for x in zip(*geo_data)]


eff_data = []

# Efficiencies don't have energies in them, add in here instead
energies_effs = []
emin_effs = 1.8
emax_effs = 10
n_files = 82 # Generated, effs do not have to cover all
e_interval_effs = (emax_effs - emin_effs)/n_files
energy_effs = emin_effs
with open (sys.argv[2]) as in_file:
    reader = csv.reader(in_file)
    for row in reader:
        dat_row = []
        for data in row:
            dat_row.append(float(data))
        eff_data.append(dat_row[:])
        del dat_row[:]

        energies_effs.append(energy_effs)
        energy_effs+=e_interval_effs

effs_sums = []
effs_sums = [sum(x) for x in zip(*eff_data)]

# Geo neutrinos file format:
# 0 - energy
# 1 - total
# 2 - all standard reactors
# 3 - closest reactor
# 4 - custom reactor
# 5 - geo_u
# 6 - geo_th

# WIT effs data file format:
# 0 - Default positron
# 1 - Default gamma
# 2 - Relaxed positron
# 3 - Relaxed gamma
# 4 - Default pairs
# 5 - Relaxed pairs
# 6 - Default pairs err
# 7 - Relaxed pairs err

print(geo_data[0])
print(eff_data[0])

print("Total (TNU/(%f keV)) = %f\n" % (geo_sums[1],width))
print("Total (TNU) = %f\n" % (geo_sums[1]*width))
print("Total (#interactions/y) = %f\n" % (geo_sums[1]*width*(n_p_sk/10e32)))

fig, ax1 = plt.subplots()

geo_energy = [row[0] for row in geo_data]
geo_reactor = [row[2]+row[4] for row in geo_data]
geo_geo = [row[2]+row[4]+row[5]+row[6] for row in geo_data]
ax1.plot(geo_energy,geo_geo,'y-')
ax1.plot(geo_energy,geo_reactor, 'b-')
ax1.fill_between(geo_energy,geo_reactor,geo_geo,color='yellow',alpha=0.5)
ax1.fill_between(geo_energy,geo_reactor,[0]*len(geo_reactor),color='b',alpha=0.5)
ax1.set_ylabel('Interaction rate/TNU', color='b')
ax1.set_xlabel('Neutrino energy/MeV')

ax2 = ax1.twinx()

# ax2.errorbar(energies_effs, pair_effs, yerr=pair_effs_err, color='r')
ax2.plot(energies_effs, [row[5] for row in eff_data],'-r',label="IBD Pairs")
ax2.plot(energies_effs, [row[4] for row in eff_data],'--r',label="IBD Pairs (Old)")
# ax2.plot(energies_effs, positron_effs_def,'-.r',label="Positron")
# ax2.plot(energies_effs, gamma_effs_def,':r',label="Gamma")
ax2.legend(loc='center right')
ax2.set_ylabel('WIT Detection efficiency', color='r')

plt.show()
