# arg 1 is E spectrum
# arg 2 is positron efficiencies
# arg 3 is n capture efficiencies

# geoneutrinos.org reactor info is in TNU per keV
# 1 event/10e32 free protons/year

import matplotlib.pyplot as plt
import numpy as np
import sys
import csv
import math

width = 9.99-1.8 # width of the data
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
        try:
            for data in row:
                dat_row.append(float(data))
        except ValueError:
            print('Skipping header...')
            continue
        geo_data.append(dat_row[:])
        del dat_row[:]

geo_sums = []
geo_sums = [sum(x) for x in zip(*geo_data)]


# Efficiencies don't have energies in them, add in here instead
energies_effs = []
emin_effs = 1.8
emax_effs = 10
n_files = 82 # Generated, effs do not have to cover all
e_interval_effs = (emax_effs - emin_effs)/n_files

# Positron
effs_energy = []
positron_effs = []
positron_effs_err = []
energy_effs = emin_effs
with open (sys.argv[2]) as in_file:
    reader = csv.reader(in_file)
    for row in reader:
        try:
            header_test = float(row[0])
        except ValueError:
            print('Skipping header...')
            continue
        effs_energy.append(energy_effs)
        positron_effs.append(float(row[0]))
        positron_effs_err.append(float(row[1]))
        energy_effs+=e_interval_effs

# Gamma
gamma_effs = 0
gamma_effs_err = 0
with open (sys.argv[3]) as in_file:
    reader = csv.reader(in_file)
    for row in reader:
        print(row)
        gamma_effs = float(row[0])
        gamma_effs_err = float(row[1])

print(gamma_effs)

pairs_effs = [x*gamma_effs for x in positron_effs]
pairs_effs_err = [math.sqrt(x*x+gamma_effs_err*gamma_effs_err) for x in positron_effs_err]

# effs_sums = []
# effs_sums = [sum(x) for x in zip(*eff_data)]

# Geo neutrinos file format:
# 0 - energy
# 1 - total
# 2 - all standard reactors
# 3 - closest reactor
# 4 - custom reactor
# 5 - geo_u
# 6 - geo_th

print("Total (TNU/(%f keV)) = %f" % (geo_sums[1],width))
print("Total (TNU) = %f" % (geo_sums[1]*width))
print("Total (#interactions in SK/y) = %f" % (geo_sums[1]*width*(n_p_sk/10e32)))

geo_energy = [row[0] for row in geo_data]
geo_reactor = [row[2]+row[4] for row in geo_data]
# geo_geo = [row[2]+row[4]+row[5]+row[6] for row in geo_data]
geo_geo = [row[5]+row[6] for row in geo_data]

# To centre the bins when summing
eff_e_hw = (effs_energy[1] - effs_energy[0])/2

detected_co = []
detected_def = []
geo_counter=0
for i in range(len(positron_effs)):
    for j in range(geo_counter,len(geo_data)):
        if (geo_energy[j] > effs_energy[i] + eff_e_hw):
            break
        detected_co.append(geo_reactor[j]*width*(n_p_sk/10e32)*pairs_effs[i])
        geo_counter+=1
        
print("Total Detected by WIT       = %f" % sum(detected_co))

# Plotting
fig, ax1 = plt.subplots(figsize=(10,5))

ax1.grid(color='k',alpha=0.2)

# ax1.plot(geo_energy[:len(detected_co)],detected_co, 'b-')
# ax1.plot(geo_energy[:len(detected_def)],detected_def, 'b-')
ax1.fill_between(geo_energy,geo_geo,color='g',alpha=0.5,label='Geo-neutrinos')
ax1.fill_between(geo_energy,geo_reactor,[0]*len(geo_reactor),color='b',alpha=0.5,label='Reactor Neutrinos')
ax1.set_ylabel('Interaction rate/TNU', color='b')
ax1.set_xlabel('Neutrino energy/MeV')
ax1.legend(loc=[0.65,0.15])

ax2 = ax1.twinx()

# ax2.errorbar(energies_effs, pair_effs, yerr=pair_effs_err, color='r')
# ax2.errorbar(effs_energy, pairs_effs, yerr=pairs_effs_err,linestyle='-',color='r',label="Co-trigger (Total = %0.1f)" % sum(detected_co))
ax2.plot(effs_energy, pairs_effs, '-r',label="Co-trigger (Total = %0.1f)" % sum(detected_co))
# ax2.plot(effs_energy, positron_effs,'-.r',label="Positron")
# ax2.plot(effs_energy, [gamma_effs]*len(effs_energy),':r',label="Gamma")
ax2.legend(loc=[0.65,0.3])
ax2.set_ylabel('WIT IBD Pair Detection Efficiency', color='r')

plt.show()
