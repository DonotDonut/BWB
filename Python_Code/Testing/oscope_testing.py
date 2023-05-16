import time
import pyvisa
import numpy as np

# Set up the resource manager
rm = pyvisa.ResourceManager()

# connecting to oscilloscope
Oscope_visa_address = 'USB0::0x0699::0x0399::C040433::INSTR'
scope = rm.open_resource(Oscope_visa_address)
print("resource manager: " + str(rm))
print("oscope: " + str(scope))
# scope.open()
print("session: " + str(scope.session))
print("timeout: " + str(scope.timeout))
scope.timeout = 20000
print("new timeout: " + str(scope.timeout))
print("chunk size (bytes): " + str(scope.chunk_size))

name = scope.query('*IDN?')
print("name: " + str(name))

# query values?
values = np.array(scope.query_binary_values('CURV?'))
print("len of values: " + str(len(values)))
print(values[0])
maximum = -20
minimum = 20

for val in values:
    if val > maximum:
        maximum = val
    if val < minimum:
        minimum = val

print("max: " + str(maximum))
print("min: " + str(minimum))

# working_dir_name = scope.query('FILES:FREES')
# print("type of thing: " + str(type(working_dir_name)))
# print("working directory name: " + str(working_dir_name))

# print("date: " + str(scope.query("measu:imm:typ")))

print(scope.resource_manufacturer_name)
