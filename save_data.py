import csv
import os
import sys

def organize_data(raw, output):
    if raw['Data Type'] == 'SPE':
        output['SPE Charge'] = raw['Charge']
        output['SPE Charge Err Abs'] = raw['Err Abs']
    elif raw['Data Type'] == 'sodium':
        output['511 Peak Charge'] = raw['Charge']
        output['511 Peak Charge Err Abs'] = raw['Err Abs']

if __name__ == '__main__':
    ENERGY = 0.511
    data = []

    try: 
        with open('temp_data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        with open('Fit_Data.csv', 'a', newline='') as file:
            headers = [
                'Channel',
                'SPE Charge',
                'SPE Charge Err Abs',
                '511 Peak Charge',
                '511 Peak Charge Err Abs',
                'LO',
                'LO Under Err',
                'LO Over Err',
                'SiPM Number',
                'Jumper Position'
            ]
            ch_spec_args = int(sys.argv[1])

            for i in range(ch_spec_args+2, len(sys.argv)-1, 2):
                headers.append(sys.argv[i])

            writer = csv.DictWriter(file, headers)
            if os.stat('Fit_Data.csv').st_size == 0:
                writer.writeheader()
            
            rows = {}
            for chunk in data:
                if chunk['Channel'] in rows.keys():
                    organize_data(chunk, rows[chunk['Channel']])
                else:
                    rows[chunk['Channel']] = {'Channel': chunk['Channel']}
                    organize_data(chunk, rows[chunk['Channel']])
            for channel in rows.values():
                if channel:
                    if '511 Peak Charge' in channel.keys():
                        peak = float(channel['511 Peak Charge'])
                        peakerr = float(channel['511 Peak Charge Err Abs'])
                    if 'SPE Charge' in channel.keys():
                        spe = float(channel['SPE Charge'])
                        speerr = float(channel['SPE Charge Err Abs'])
                    if '511 Peak Charge' in channel.keys() and 'SPE Charge' in channel.keys():
                        channel['LO'] =  peak / spe / ENERGY
                        channel['LO Under Err'] = ((peak - peakerr) / (spe + speerr)) / ENERGY - channel['LO']
                        channel['LO Over Err'] = ((peak + peakerr) / (spe - speerr)) / ENERGY - channel['LO']
                    for i in range(ch_spec_args+2, len(sys.argv)-1, 2):
                        channel[sys.argv[i]] = sys.argv[i+1]

            if 'channel1' in rows.keys():
                rows['channel1']['SiPM Number'] = sys.argv[2]
                rows['channel1']['Jumper Position'] = sys.argv[3]
            if 'channel2' in rows.keys():
                rows['channel2']['SiPM Number'] = sys.argv[4]
                rows['channel2']['Jumper Position'] = sys.argv[5]
           
            for channel in rows.values():
                writer.writerow(channel)

            os.remove('temp_data.csv')

    except FileNotFoundError:
        print("No data to save to csv")
    
        
