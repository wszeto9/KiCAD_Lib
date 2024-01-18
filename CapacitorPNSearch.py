

Capacitors = [["100nF", "50V", "0603", ""], ["220nF", "50V", "0603", ""], ["1uF", "50V", "0603", "1276-1860-1-ND"], ["2.2uF", "16V", "0603", "1276-1040-1-ND"], ["22uF", "10V", "0603", "1276-1274-1-ND"], ["10uF", "25V", "0603", "1276-1869-1-ND"]]


import csv



def GetCapacitorPN(input_value, package, voltageRating):
    input_value = input_value.replace('f', 'F')
    input_value = input_value.replace('U', 'u')
    input_value = input_value.replace('N', 'n')
    input_value = input_value.replace('P', 'p')
    #save the multiplier of the code
    if('p' in input_value):
        letter = 'p'
        multiplier = 10**-12
    elif('n' in input_value):
        letter = 'n'
        multiplier = 10**-9
    elif('u' in input_value):
        letter = 'u'
        multiplier = 10**-6
    VoltageInt = float(voltageRating.split("V")[0])
    for parts in Capacitors:
        if(input_value in parts[0]): #Match Capacitance
            if(package in parts[2]): #Match Package
                if(VoltageInt <= float(parts[1].split("V")[0])): #check voltage rating to be higher or equal
                    return parts[3]
    return "" 



with open('George.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    first_row = next(csv_reader)
    
    # determine the index of the value and footprint row. this helps identify the column to look for resistor values in. 
    IndexOfValue = first_row.index('Value') if 'Value' in first_row else None
    if(IndexOfValue == None):
        print("Error! Could not find column named 'Value'!")
    IndexOfFootprint = first_row.index('Footprint') if 'Footprint' in first_row else None
    if(IndexOfFootprint == None):
        print("Error! Could not find column named 'Value'!")
  
    for row in csv_reader:
        if('Capacitor_SMD:' in row[IndexOfFootprint]):
            footprint = row[IndexOfFootprint].split('Capacitor_SMD:')[1][2:6] #Returns 4 letter code from KiCAD footprint
            capacitance = row[IndexOfValue].split(' ')[0].split('/')[0] # Grabs Resistance value from KiCAD footprint. It chucks tolerances for now lol
            if(len(row[IndexOfValue].split(' ')) > 1):
                voltage = row[IndexOfValue].split(' ')[1]
            else:
                voltage = "25V"
            PartNumber = GetCapacitorPN(capacitance, footprint, voltage)
            
            print(PartNumber) #remove suffix if you want Manufacturer product number, keep it if you want digikey part number