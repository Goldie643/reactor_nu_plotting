# arg 1..-2 is E spectrum files
# arg -1 is efficiencies

# geoneutrinos.org reactor info is in TNU per keV
# 1 event/10e32 free protons/year

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import sys
import csv

# width = (9.995-1.805)*1000 #width of the data in keV
width = 10 # keV
n_p_o = 8 # n protons in Oxygen
n_p_h = 1 # n protons in Hydrogen
u = 1.6605402e-27 # 1 atomic mass unit in kg
m_o = 15.999*u
m_h = 1*u
m_water = 2*m_h+m_o # kg
m_sk = 22.5e6 # kg (FV)
n_water_sk = m_sk/m_water
n_p_sk = n_water_sk*(2*n_p_h)
print("N protons in SK = %g\n" % n_p_sk)

class geo_file:
    def __init__(self,file_name):

        geo_data = []
        with open (file_name) as in_file:
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
        
        self.energy             = [row[0] for row in geo_data]
        self.total              = [row[1] for row in geo_data]
        self.standard_reactors  = [row[2] for row in geo_data]
        self.closest_reactor    = [row[3] for row in geo_data]
        self.custom_reactor     = [row[4] for row in geo_data]
        self.total_reactors     = [x+y for x,y in zip(self.standard_reactors,self.custom_reactor)]
        self.geo                = [row[5] + row[6] for row in geo_data]
        
        # Geo is in TNU/keV = int / 1e32 protons / year
        scale = width*n_p_sk/1e32
        self.total_sk               = [x*scale for x in self.total]
        self.standard_reactors_sk   = [x*scale for x in self.standard_reactors]
        self.closest_reactor_sk     = [x*scale for x in self.closest_reactor]
        self.custom_reactor_sk      = [x*scale for x in self.custom_reactor]
        self.total_reactors_sk      = [x*scale for x in self.total_reactors]
        self.geo_sk                 = [x*scale for x in self.geo]

class eff_file:
    def __init__(self,file_name,emin,emax,n_files):

        energies_effs = []
        eff_data = []

        e_interval_effs = (emax- emin)/n_files
        energy_effs = emin
        with open (file_name) as in_file:
            reader = csv.reader(in_file)
            for row in reader:
                dat_row = []
                try:
                    for data in row:
                        dat_row.append(float(data))
                except ValueError:
                    print('Skipping header...')
                    continue
                eff_data.append([energy_effs] + dat_row[:])
                del dat_row[:]

                energy_effs+=e_interval_effs

        self.energy         = [row[0] for row in eff_data]
        self.positron_def   = [row[1] for row in eff_data]
        self.gamma_def      = [row[2] for row in eff_data]
        self.positron_rel   = [row[3] for row in eff_data]
        self.gamma_rel      = [row[4] for row in eff_data]
        self.pairs_def      = [row[5] for row in eff_data]
        self.pairs_rel      = [row[6] for row in eff_data]
        self.pairs_def_err  = [row[7] for row in eff_data]
        self.pairs_rel_err  = [row[8] for row in eff_data]

        # Half width of energy bins to shift points to correct place
        self.energy_hw      = (self.energy[1] - self.energy[0])/2

    # Multiplying efficiencies by interaction rate to get detected rate
    # could do one the other way in geo_file, but will leave like this for now
    def detected_pairs(self,geo_file,def_or_rel,reactors_or_geo):
        effs = []
        if(def_or_rel == "def"):
            effs = self.pairs_def
        elif(def_or_rel == "rel"):
            effs = self.pairs_rel
        else:
            print("Please define \"def\" or \"co\" \
                    in detected_pairs(geo_obj,def_or_rel,reactors_or_geo)")
            exit(-1)
        totals = []
        if(reactors_or_geo == "reactors"):
            totals = geo_file.total_reactors_sk
        elif(reactors_or_geo == "geo"):
            totals = geo_file.geo_sk
        else:
            print("Please define \"reactors\" or \"geo\" \
                    in detected_pairs(geo_obj,def_or_rel,reactors_or_geo)")
            exit(-1)

        detected = []

        geo_counter=0

        for i in range(len(effs)):
            for j in range(geo_counter,len(geo_file.energy)):
                # If the geo energy leaves the eff bin, iterate up to next eff
                if (geo_file.energy[j] > self.energy[i] + 2*self.energy_hw):
                    break
                detected.append(totals[j]*effs[i])
                geo_counter+=1

        return detected

# Geo neutrinos file format:
# 0 - energy
# 1 - total
# 2 - all standard reactors
# 3 - closest reactor
# 4 - custom reactor
# 5 - geo_u
# 6 - geo_th

# WIT effs data file format:
# 0 - energy
# 1 - Default positron
# 2 - Default gamma
# 3 - Relaxed positron
# 4 - Relaxed gamma
# 5 - Default pairs
# 6 - Relaxed pairs
# 7 - Default pairs err
# 8 - Relaxed pairs err

# Plotting
fig, ax1 = plt.subplots(figsize=(10,5))
ax1.grid(color='k',alpha=0.2)
ax1.set_ylabel("Interactions in SK/y/10 keV")
ax1.set_xlabel("Neutrino Energy/MeV")


eff = eff_file(sys.argv[-1],1.8,10,82)

ax2 = ax1.twinx()
ax2.set_ylabel('WIT IBD Pair Detection Efficiency', color='r')

n_geo_files = len(sys.argv)-1

geo_files = []

for i in range(1,n_geo_files):

    file_name = sys.argv[i]
    file_name_clean = sys.argv[i][8:-6]
    print("Adding file " + file_name)
    new_file = geo_file(file_name)
    print(sum(new_file.total_sk))
    new_detected_def = sum(eff.detected_pairs(new_file,"def","reactors"))
    new_detected_rel = sum(eff.detected_pairs(new_file,"rel","reactors"))
    ax1.fill_between(
        new_file.energy,
        new_file.total_reactors,
        alpha=0.7,
        label=file_name_clean
        )
    ax1.fill_between([],[],
        color='k',
        alpha=0,
        label = "Co  : %0.1f\nDef : %0.1f" % (new_detected_rel,new_detected_def)
        )
    geo_files.append(new_file)

geo_temp_file = geo_file(sys.argv[1])
ax1.fill_between(
    geo_temp_file.energy,
    geo_temp_file.geo,
    alpha=0.2,
    color='k',
    label="Geo-neutrinos"
    )
geo_detected_def = sum(eff.detected_pairs(new_file,"def","geo"))
geo_detected_rel = sum(eff.detected_pairs(new_file,"rel","geo"))

# ax1.fill_between([],[],
# color='k',
# alpha=0,
# label = "Co  : %0.1f\nDef : %0.1f" % (geo_detected_rel,geo_detected_def)
# )
# ax2.plot(eff.energy,eff.positron_def,"-.b",label = "Positron",)
# ax2.plot(eff.energy,eff.gamma_def,":b",label = "Gamma",)
# ax2.plot(eff.energy,eff.gamma_rel,"-b",label = "Gamma (Relaxed)",)
ax2.plot(
    eff.energy,
    eff.pairs_rel,
    "-r"
# label = "Co-trigger",
    )
# ax2.plot(
# eff.energy,
# eff.pairs_def,
# "--r",
# label = "Standard",
# )

ax1.legend(loc=[0.7,0.1])
ax2.legend(loc=[0.7,0.75])

plt.show()
# ax1.plot(geo_energy[:len(detected_co)],detected_co, 'b-')
# ax1.plot(geo_energy[:len(detected_def)],detected_def, 'b-')
# ax1.fill_between(geo_energy,geo_geo,color='g',alpha=0.5,label='Geo-neutrinos')
# ax1.fill_between(geo_energy,geo_reactor,[0]*len(geo_reactor),color='b',alpha=0.5,label='Reactor Neutrinos')
# ax1.set_ylabel('Interaction rate/TNU', color='b')
# ax1.set_xlabel('Neutrino energy/MeV')
# ax1.legend(loc=[0.65,0.15])

# ax2 = ax1.twinx()

# ax2.errorbar(energies_effs, pair_effs, yerr=pair_effs_err, color='r')
# ax2.plot(eff_energy, eff_pairs_co,'-r',label="Co-trigger (Total = %0.1f)" % sum(detected_co))
# ax2.plot(eff_energy, eff_pairs_def,'--r',label="Standard WIT (Total = %0.1f)" % sum(detected_def))
# ax2.plot(eff_energy, eff_positron_def,'-.r',label="Positron")
# ax2.plot(eff_energy, eff_gamma_def,':r',label="Gamma")
# ax2.legend(loc=[0.65,0.3])

# plt.show()
