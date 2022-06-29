#!/bin/sh
set -x
set -e

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
Lcode="NA"
# * Date
date=$(date +%m%d%Y)
# * Time
Time=$(date +%k":"%M":"%S)
# * Bias Voltage
BV="42"
# * Integration Time
IT="100"
# * Rewind Time
rewind="200"
# * Extra
EXTRA="SPE_fit_testing"

# First 4 arguments are in this order:
# Channel 1 SiPM Number
ch1SiPMNum="027"
# HAMAMATSU3x3
# Channel 1 Jumper Position (Position 1 is farthest from channel outlets)
ch1jp="4"
# Channel 2 SiPM Number
ch2SiPMNum="026"
# Channel 2 Jumper Position (Position 1 is farthest from channel outlets)
ch2jp="4"
# Number of Channel Specific Arguments
ChSpecArgs="4"

# Creating filenames
lspe="spe_settings.hdf5"
lp511="511_settings.hdf5"
spe_hdf5="sodium_spe_${Lcode}LYSO_${date}_${Time}_${BV}v_jp${ch1jp1},${ch2jp}_${EXTRA}.hdf5"
spe_root="sodium_spe_${Lcode}LYSO_${date}_${Time}_${BV}v_jp${ch1jp1},${ch2jp}_${EXTRA}.root"
p511_hdf5="sodium_p511_${Lcode}LYSO_${date}_${Time}_${BV}v_jp${ch1jp1},${ch2jp}_${EXTRA}.hdf5"
p511_root="sodium_p511_${Lcode}LYSO_${date}_${Time}_${BV}v_jp${ch1jp1},${ch2jp}_${EXTRA}.root"

# * number of events
ne=10000
# * ipadress
ipad="192.168.0.182"

python3 clear_temp_data.py

# SPE ANALYSIS
./load-settings --ip-address  $ipad $lspe
./acquire-waveforms -n $ne --ip-address $ipad -o $spe_hdf5
./analyze-waveforms $spe_hdf5 -o $spe_root --pdf --IT $IT --r $rewind 
./fit-histograms $spe_root --pdf --SPE_FLL -0.4 --SPE_FLR 1.5 #--IT $IT
# # P511 ANALYSIS
# ./load-settings --ip-address $ipad $lp511
# ./acquire-waveforms -n $ne --ip-address $ipad -o $p511_hdf5
# ./analyze-waveforms $p511_hdf5 -o $p511_root --sodium --pdf 
# ./fit-histograms $p511_root --sodium --pdf


python3 save_data.py "$ChSpecArgs" "$ch1SiPMNum" "$ch1jp" "$ch2SiPMNum" "$ch2jp" BV "$BV" "Number of Events" "$ne" Lcode "$Lcode" Date "$date" Time "$Time" Extra "$EXTRA"

echo "Ending time : "
date +"%D %T"
# Upgrades required:
# * check that the fit can be done in the background to check both fit plots
# * a
set -edd data to csv / excel automatically
