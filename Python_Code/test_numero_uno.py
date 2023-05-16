import time
# import visa
import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The methods that a USB instrument can use via pyvisa
# https://pyvisa.readthedocs.io/en/1.13.0/api/resources.html#pyvisa.resources.USBInstrument
# funny little tutorial
# https://www.youtube.com/watch?v=IaQl_l0yuIg
# and linked github: https://github.com/AsserHic/alab
# FUNCTION GENERATOR PROGRAMMING MANUAL
# https://download.tek.com/manual/AFG3000-Series-Arbitrary-Function-Generator-Programmer-EN.pdf
# OSCOPE PROGRAMMING MANUAL
# https://download.tek.com/manual/077009701_RevA_web.pdf

#----------- Connection ------------------------
# Set up the resource manager
rm = pyvisa.ResourceManager()

# Connect to function generator
Fugen_visa_address = 'USB0::0x0699::0x034C::C012350::INSTR'
gen = rm.open_resource(Fugen_visa_address)

# connecting to oscilloscope
Oscope_visa_address = 'USB0::0x0699::0x0399::C040433::INSTR'
scope = rm.open_resource(Oscope_visa_address)



# -------------------- Setting Function Generator ------------------

# Set delay before turning on function generator
time.sleep(5)

# Turn on function generator
gen.write(':OUTPUT:STATE ON')

# Set frequency (in Hertz)
gen.write(':FREQUENCY 1000000')

# Set amplitude
gen.write(':VOLTAGE:AMPLITUDE 1')

# Set waveform
gen.write(':FUNCTION:RAMP')

gen_name = gen.write('IDN?')
print("function generator name: " +str(gen_name))

#----------- Setting Oscilloscope  ------------------------
working_dir_name = scope.write(':FILESystem:CWD')
print("working directory name: " + str(working_dir_name))

# the internet's take
'''
interval_in_ms = 500
number_of_readings = 10
scope.write("status:measurement:enable 512; *sre 1")
scope.write("sample:count %d" % number_of_readings)
scope.write("trigger:source bus")
scope.write("trigger:delay %f" % (interval_in_ms / 1000.0))
scope.write("trace:points %d" % number_of_readings)
scope.write("trace:feed sense1; trace:feed:control next")

scope.write("initiate")
scope.assert_trigger()
scope.wait_for_srq()

voltages = scope.query_ascii_values("trace:data?")
print("Average voltage: ", sum(voltages) / len(voltages))

scope.query("status:measurement?")
scope.write("trace:clear; trace:feed:control next")
'''
# an older take
'''
# Set oscilloscope to single acquisition mode
# scope.write(':SINGLE')

# Retrieve data from channel 1
# **WHY READ RAW??** JUST DON'T
# scope.write(':WAV:POINTS:MODE RAW')
# scope.write(':WAV:DATA? CH1')
# data = scope.read_raw()
scope.write('CURV?')
data = np.array(scope.query_binary_values('CURV?'))


# Plot data
plt.plot(data)
plt.show()

# Export data to Excel file
df = pd.DataFrame(data, columns=['Voltage'])
df.to_excel('oscilloscope_data.xlsx', index=False)
'''