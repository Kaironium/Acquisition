#!/bin/sh

#Author : Guillermo Reales & Anthony La Torre
#Commands required for a single spe/LO callibration
#Script follows here:

### VARIABLES
# * LYSO barcode
Lcode="572"
# * Date
date = "090822"
# * Bias Voltage
BV = "42"
# * Extra
EXTRA = ""
# Creating filenames
lspe = "sodium_spe_437LYSOv0_45v.hdf5"
lp511 = "sodium_p511_437LYSOv0_45v.hdf5"
spe_hdf5 ="sodium_spe_${Lcode}LYSO_${date}_${BV}v${EXTRA}.hdf5"
spe_root ="sodium_spe_${Lcode}LYSO_${date}_${BV}v${EXTRA}.root"
p511_hdf5 ="sodium_p511_${Lcode}LYSO_${date}_${BV}v${EXTRA}.hdf5"
p511_root ="sodium_p511_${Lcode}LYSO_${date}_${BV}v${EXTRA}.root"

# * number of events
ne = 4000
# * ipadress
ipad = "192.168.0.182"

# SPE ANALYSIS
./load-settings --ip-address  $ipad -o $lspe
./acquire-waveforms -n $ne --ip-address $ipad -o $spe_hdf5
./analyze-waveforms $spe_hdf5 -o $spe_root --pdf 
./fit-histogram $spe_root --pdf
# P511 ANALYSIS
./load-settings --ip-address $ipad -o $lp511
./acquire-waveforms -n $ne --ip-address $ipad -o $p511_hdf5
./analyze-waveforms $p511_hdf5 -o $spe_root --sodium --pdf 
./fit-histograms $p511_root --sodium --pdf

# Upgrades required:
# * check that the fit can be done in the background to check both fit plots
# * add data to csv / excel automatically
