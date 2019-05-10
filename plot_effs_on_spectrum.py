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

tnu_sum = 0
energies = []
tnus = []

with open (sys.argv[1]) as in_file:
    reader = csv.reader(in_file)
    in_file.readline()
    for row in reader:
        energies.append(float(row[0]))
        tnus.append(float(row[1]))
        tnu_sum+=float(row[1])

# My naming convention is all over the place here lol
positron_effs = []
gamma_effs = []
positron_effs_def = []
gamma_effs_def = []

pair_effs = []
pair_effs_err = []
pair_effs_def = []
pair_effs_err_def = []
energies_effs = []
emin_effs = 1.8
emax_effs = 10
n_files = 82 # Generated, effs do not have to cover all
e_interval_effs = (emax_effs - emin_effs)/n_files
energy_effs = emin_effs
with open (sys.argv[2]) as in_file:
    reader = csv.reader(in_file)
    in_file.readline()
    for row in reader:
        positron_effs_def.append(float(row[0]))
        gamma_effs_def.append(float(row[1]))
        positron_effs.append(float(row[2]))
        gamma_effs.append(float(row[3]))

        pair_effs_def.append(float(row[4]))
        pair_effs.append(float(row[5]))
        pair_effs_err_def.append(float(row[6]))
        pair_effs_err.append(float(row[7]))
        energies_effs.append(energy_effs)
        energy_effs+=e_interval_effs

print("Total (TNU/(%f keV)) = %f\n" % (tnu_sum,width))
print("Total (TNU) = %f\n" % (tnu_sum*width))
print("Total (#interactions/y) = %f\n" % (tnu_sum*width*(n_p_sk/10e32)))

# print(len(energies))
# print(len(tnus))
# print(len(pair_effs))

fig, ax1 = plt.subplots()

ax1.plot(energies,tnus, 'b-')
ax1.set_ylabel('Interaction rate/TNU', color='b')
ax1.set_xlabel('Neutrino energy/MeV')

ax2 = ax1.twinx()

# ax2.errorbar(energies_effs, pair_effs, yerr=pair_effs_err, color='r')
ax2.plot(energies_effs, pair_effs,'-r',label="IBD Pairs")
ax2.plot(energies_effs, pair_effs_def,'--r',label="IBD Pairs (Old)")
# ax2.plot(energies_effs, positron_effs_def,'-.r',label="Positron")
# ax2.plot(energies_effs, gamma_effs_def,':r',label="Gamma")
ax2.legend(loc='center right')
ax2.set_ylabel('WIT Detection efficiency', color='r')

plt.show()
