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

inputs = ['5.1K', '5K1', '10K', '1K', '1M', '0.33R', '33m']

for resistor in inputs:
    output = convert_resistor_code(resistor)
    print(f"Input: {resistor}, Output: {output}")
