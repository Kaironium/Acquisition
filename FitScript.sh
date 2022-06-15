#!/bin/sh
set -x

#Author : Guillermo Reales & Anthony La Torre
#Commands required for a single spe/LO callibration
#Script follows here:

echo "Starting Time:"
date +"%D %T"

# IF error "Permission denied" run:
# chmod u+r+x <filename>.sh

# IF variable gives error "Command not recognize"
# Remember that the equal sign can have no spaces to the variable name

### VARIABLES
# * LYSO barcode
Lcode="526"
# * Date
date="140622"
# * Bias Voltage
BV="42"
# * Extra
EXTRA="Kai_test"
# Creating filenames
lspe="spe_settings.hdf5"
lp511="511_settings.hdf5"
spe_hdf5="sodium_spe_${Lcode}LYSO_${date}_${BV}v${EXTRA}.hdf5"
spe_root="sodium_spe_${Lcode}LYSO_${date}_${BV}v${EXTRA}.root"
p511_hdf5="sodium_p511_${Lcode}LYSO_${date}_${BV}v${EXTRA}.hdf5"
p511_root="sodium_p511_${Lcode}LYSO_${date}_${BV}v${EXTRA}.root"

# * number of events
ne=20000
# * ipadress
ipad="192.168.0.182"

# SPE ANALYSIS
./load-settings --ip-address  $ipad $lspe
sleep 10
./acquire-waveforms -n $ne --ip-address $ipad -o $spe_hdf5
sleep 10
./analyze-waveforms $spe_hdf5 -o $spe_root --pdf 
sleep 10
./fit-histograms $spe_root --pdf
# P511 ANALYSIS
./load-settings --ip-address $ipad $lp511
sleep 10
./acquire-waveforms -n $ne --ip-address $ipad -o $p511_hdf5
sleep 10
./analyze-waveforms $p511_hdf5 -o $p511_root --sodium --pdf 
sleep 10
./fit-histograms $p511_root --sodium --pdf

./save_data

echo "Ending time : "
date +"%D %T"
# Upgrades required:
# * check that the fit can be done in the background to check both fit plots
# * add data to csv / excel automatically
