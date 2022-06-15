import csv


if __name__ == '__main__':
    with open('sodium_data', 'r') as file:
        reader = csv.DictReader(file)
        sodium_data = null
        for row in reader:
            sodium_data = row

    with open('SPE_data', 'r') as file:
        reader = csv.DictReader(file)
        SPE_data = null
        for row in reader:
            SPE_data = row

    with open('Fit_Data', 'a') as file:
        headers = [
            # 'SiPM Array',
            # 'Channel',
            # 'Jumper Position',
            # 'Bias Voltage',
            # 'n',
            'SPE Charge',
            'SPE Charge Err Abs',
            # 'n2',
            '511 Peak Charge',
            '511 Peak Charge Err Abs',
            # 'date',
            # 'hour',
            'LO',
            # 'Filename',
            # 'Comments'
        ]
        writer = csv.DictWriter(file, headers)
        writer.writerow({
            'SPE Charge': SPE_data['Charge']
            'SPE Charge Err Abs': SPE_data['Err_Abs']
            '511 Peak Charge': sodium_data['Charge']
            '511 Peak Charge Err Abs': sodium_data['Err Abs']
            'LO': sodium_data['Charge'] / SPE_data['Charge']
        })
