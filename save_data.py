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
            print(sys.argv[1])
            ch_spec_args = int(sys.argv[1])

            for i in range(ch_spec_args+2, len(sys.argv)-1, 2):
                headers.append(sys.argv[i])

            writer = csv.DictWriter(file, headers)
            if os.stat('Fit_Data.csv').st_size == 0:
                writer.writeheader()
            
            channel1 = {}
            channel2 = {}
            
            for chunk in data:
                print(chunk)
                if chunk['Channel'] == 'channel1':
                    channel1['Channel'] = 'channel1'
                    organize_data(chunk, channel1)
                elif chunk['Channel'] == 'channel2':
                    channel2['Channel'] = 'channel2'
                    organize_data(chunk, channel2)
                else:
                    raise ValueError('Unsupported channel')
          
            for channel in [channel1, channel2]:
                if channel:
                    peak = float(channel['511 Peak Charge'])
                    peakerr = float(channel['511 Peak Charge Err Abs'])
                    print(channel)
                    spe = float(channel['SPE Charge'])
                    speerr = float(channel['SPE Charge Err Abs'])
                    channel['LO'] =  peak / spe / ENERGY
                    channel['LO Under Err'] = ((peak - peakerr) / (spe + speerr)) / ENERGY - channel['LO']
                    channel['LO Over Err'] = ((peak + peakerr) / (spe - speerr)) / ENERGY - channel['LO']
                    for i in range(ch_spec_args+2, len(sys.argv)-1, 2):
                        channel[sys.argv[i]] = sys.argv[i+1]

            if channel1:
                channel1['SiPM Number'] = sys.argv[2]
                channel1['Jumper Position'] = sys.argv[3]
                writer.writerow(channel1)
            if channel2:
                channel2['SiPM Number'] = sys.argv[4]
                channel2['Jumper Position'] = sys.argv[5]
                writer.writerow(channel2)
            
            os.remove('temp_data.csv')

    except FileNotFoundError:
        print("No data to save to csv")
    
        
