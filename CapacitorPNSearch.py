Capacitors = [
    ["100nF", "50V", "0603", "We have this at home"], 
    ["220nF", "50V", "0603", "We have this at home"], 
    ["1uF", "50V", "0603", "1276-1860-1-ND"], 
    ["2.2uF", "16V", "0603", "1276-1040-1-ND"], 
    ["22uF", "10V", "0603", "1276-1274-1-ND"], 
    ["10uF", "25V", "0603", "1276-1869-1-ND"], 
    ["10uF", "50V", "1206", "1276-6736-1-ND"],
    ["470nF", "25V", "0603", "1276-2082-1-ND"],
    ["1nF", "50V", "0603", "1276-1091-1-ND"],
    ["2.2nF", "100V", "0603", "1276-6583-1-ND"],
    ["100pF", "50V", "0603", "1276-1008-1-ND"],
    ["22uF", "16V", "0603", "1276-7076-1-ND"],
    ["10nF", "50V", "0603", "1276-1009-1-ND"],
    ["100nF", "50V", "0805", "1276-1003-1-ND"],
    ["1uF", "50V", "0805", "1276-1029-1-ND"],
    ["10nF", "50V", "0805", "1276-1015-1-ND"],
    ]

import csv

def GetCapacitorPN(input_value, package, voltageRating):
    if("DNP" in input_value):
        return ""
    
    input_value = input_value.replace('f', 'F')
    input_value = input_value.replace('U', 'u')
    input_value = input_value.replace('N', 'n')
    input_value = input_value.replace('P', 'p')
    
    #save the multiplier of the code
    if('p' in input_value):
        letter = 'p'
    elif('n' in input_value):
        letter = 'n'
    elif('u' in input_value):
        letter = 'u'
    else:
        return ""

    if(float(input_value.split(letter)[0])<1):
        letterOld = letter
        if(letter == 'n'):
            letter = 'p'
        elif(letter == 'u'):
            letter = 'n'
        input_value = str(float(input_value.split(letterOld)[0]) * 1000)[:3] + letter + "F" #my lazy ass attempt to go from float to int is to splice off the decimal point. 
    VoltageInt = float(voltageRating.split("V")[0])
    for parts in Capacitors:
        if(input_value in parts[0]): #Match Capacitance
            if(package in parts[2]): #Match Package
                if(VoltageInt <= float(parts[1].split("V")[0])): #check voltage rating to be higher or equal
                    return parts[3]
    return "" 

with open('BOM.csv') as csv_file:
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
        if('C_' in row[IndexOfFootprint]):
            footprint = row[IndexOfFootprint].split('C_')[1][:4] #Returns 4 letter code from KiCAD footprint
            capacitance = row[IndexOfValue].split(' ')[0].split('/')[0] # Grabs Resistance value from KiCAD footprint. It chucks tolerances for now lol
            
            #JLC lib has the size in the value. remove it. 
            if((capacitance[:4]) in ["0201", "0402", "0603", "0805", "1206"]):
                capacitance = capacitance[5:]
                if(',' in capacitance):
                    capacitance = capacitance.split(',')[0]
            
            if(len(row[IndexOfValue].split('V')) > 1):
                voltage = row[IndexOfValue].split('V')[0] + "V"
                if(',' in voltage):
                    voltage = voltage.split(',')[len(voltage.split(',')) - 1 ]
            else:
                voltage = "25V"
            PartNumber = GetCapacitorPN(capacitance, footprint, voltage)
            
            print(PartNumber) #remove suffix if you want Manufacturer product number, keep it if you want digikey part number