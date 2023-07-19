# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 21:01:17 2023

@author: Winnie
"""

#from JLC's basic resistor list
AvailableResistors = [470,330,300,220,150,120,100,510,680,1200,1500,2200,2400,2000,3300,3900,4700,5100,5600,6800,7500,8200,10000,12000,15000,18000,20000,22000,24000,27000,33000,39000,47000,49900,51000,56000,68000,75000,100000,120000,150000,200000,220000,300000,330000,470000,510000]
AvailableResistors.sort()

def FindOptimalResistorDivider(vin, vout, ResistorList = AvailableResistors, MinRh = 1000, MaxRh=100000):
    Options = [] #Each entry in list shall be in [error, Rh, Rl, Vout_Atual, Vin_Actual]
    for Rl_test in AvailableResistors:
        Rh_ideal = Rl_test * vin/vout - Rl_test 
        LargerThanRh =[1 if resistor > Rh_ideal else 0 for resistor in AvailableResistors]
        if(1 in LargerThanRh):
            idx = LargerThanRh.index(1)
            Rh_high = AvailableResistors[idx]
            Rh_low = AvailableResistors[idx-1]
            error_high = Rl_test / (Rl_test + Rh_high) - vout/vin
            error_low = Rl_test / (Rl_test + Rh_low) - vout/vin
            Options.append([abs(error_high), Rh_high, Rl_test, vin * Rl_test/(Rl_test+Rh_high), vout*(Rh_high+Rl_test)/Rl_test])
            Options.append([abs(error_low), Rh_low, Rl_test, vin * Rl_test/(Rl_test+Rh_low), vout*(Rh_low+Rl_test)/Rl_test])
    Options.sort()
    RemoveEntries = []
    for i in range(len(Options)):
        if (Options[i][1] > MaxRh) or Options[i][1] < MinRh:
            RemoveEntries.append(Options[i])
    if len(RemoveEntries):
        for Entry in RemoveEntries:
            Options.remove(Entry)
    return Options

Options = FindOptimalResistorDivider(48, 0.7)

for i in range(5):
    print("Option ", i, ": Rhigh = ", Options[i][1]/1000, "kOhms, Rlow = ", Options[i][2]/1000, "kOhms, Vout_Actual: ", round(Options[i][3], 4), "V, Vin_Actual: ", round(Options[i][4], 3), "V")