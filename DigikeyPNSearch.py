import csv



def convert_resistor_code(input_value):
    
    input_value = input_value.replace('r', 'R')
    input_value = input_value.replace('k', 'K') # All letters now uppercase (assume M/m will not be confused with each other)
    
    #save the multiplier of the code
    if('K' in input_value):
        letter = 'K'
        multiplier = 1000
    elif('M' in input_value):
        letter = 'M'
        multiplier = 1000000
    elif('m' in input_value):
        letter = 'm'
        multiplier = 0.001
    else:
        letter = 'R'
        multiplier = 1

    if('.' in input_value):
        input_value = input_value.replace(letter, '')
    input_value = input_value.replace('.', letter)
    output_value = input_value + '0000000'
    return output_value[:4]

with open('bom2.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    first_row = next(csv_reader)
    IndexOfValue = first_row.index('Value') if 'Value' in first_row else None
    if(IndexOfValue == None):
        print("Error! Could not find column named 'Value'!")
    IndexOfFootprint = first_row.index('Footprint') if 'Footprint' in first_row else None
    if(IndexOfFootprint == None):
        print("Error! Could not find column named 'Value'!")
  
    for row in csv_reader:
        if('Resistor_SMD' in row[IndexOfFootprint]):
            footprint = row[IndexOfFootprint].split('Resistor_SMD:R_')[1][:4] #Returns 4 letter code from KiCAD footprint
            resistance = row[IndexOfValue].split(' ')[0].split('/')[0] # Grabs Resistance value from KiCAD footprint. It chucks tolerances for now lol
            resistanceCode = convert_resistor_code(resistance)
            
            #Stockpole naming
            NamePrefix = 'RMCF'
            Packaging = 'FT'
            print(NamePrefix+ footprint + Packaging + resistanceCode)