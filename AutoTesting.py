import time
#import visa
import pyvisa # for connection 
import numpy as np 
import matplotlib.pyplot as plt # for plotting signal 
import pandas as pd # for the function geneator 
import openpyxl # for gathering data into excel and exporting it 


#----------- Connecting ------------------------

rm = pyvisa.ResourceManager()

# Connect to function generator
Fgen_visa_address = 'USB0::0x0699::0x034C::C012350::INSTR'
gen = rm.open_resource(Fgen_visa_address)

# connecting to oscilloscope 
Oscope_visa_address = 'USB0::0x0699::0x0399::C040433::INSTR'
scope = rm.open_resource(Oscope_visa_address)



# --------------------  Function Generator ------------------

# Set delay before turning on function generator
time.sleep(5)

# Turn on function generator
gen.write(':OUTPUT:STATE ON')

# Set frequency
gen.write(':FREQUENCY 1000')

# Set amplitude Vpp 
gen.write(':VOLTAGE:AMPLITUDE 2')

# Set waveform
gen.write(':FUNCTION SINE')


# --------------------  Oscilloscope  ------------------


# Set delay before turning on Oscilloscope 
time.sleep(5)

# Turn on Oscilloscope 
scope.write(':OUTPUT:STATE ON')

# timeout, not reading data after amount of ms/s
scope.timeout = 10000 # 10k ms = 10s , can use 'none' to make it go longer 
scope.encoding = 'latin_1'

 # termination to new line 
scope.read_termination = '\n'
scope.write_termination = None

# string 'CLs' is sent to the oscilloscope to clear the event status register ESR
scope.write('*cls')

# questions the oscillospe for its identification 
print(scope.query('*idn?'))

input("""
ACTION:
Connect probe to oscilloscope Channel 1 and the probe compensation signal.

Press Enter to continue...
""")

# reset the oscilloscope 
scope.write('*rst') # reset

t1 = time.perf_counter()# records start time of reset

# questions oscilloscope for operation complete status 
r = scope.query('*opc?') # sync

t2 = time.perf_counter() # records end time of reset  
print('reset time: {}'.format(t2 - t1)) # duration of reset 

scope.write('autoset EXECUTE') # autoset operation 
t3 = time.perf_counter() # records start time of autoset 
r = scope.query('*opc?') # sync
t4 = time.perf_counter()# records end time of autoset 
print('autoset time: {} s'.format(t4 - t3)) # duration of autoset 

# io config
scope.write('header 0') # turn off header info in
scope.write('data:encdg SRIBINARY') # set data encoding to binary 
scope.write('data:source CH1') # set dtat source to channel 1 
scope.write('data:start 1') # first sample

# questions oscillospe for record length and converts results into an integar,and stores it in record 
record_length = int(scope.query('horizontal:recordlength?'))
scope.write('data:stop {}'.format(record_length)) # last sample
scope.write('wfmoutpre:byt_n 1') # 1 byte per sample

# acq config
scope.write('acquire:state 0') # stop
scope.write('acquire:stopafter SEQUENCE') # single
scope.write('acquire:state 1') # run
t5 = time.perf_counter()
r = scope.query('*opc?') # sync
t6 = time.perf_counter()
print('acquire time: {} s'.format(t6 - t5))

# data query
t7 = time.perf_counter()
bin_wave = scope.query_binary_values('curve?', datatype='b', container=np.array)
t8 = time.perf_counter()
print('transfer time: {} s'.format(t8 - t7))

# retrieve scaling factors
tscale = float(scope.query('wfmoutpre:xincr?'))
tstart = float(scope.query('wfmoutpre:xzero?'))
vscale = float(scope.query('wfmoutpre:ymult?')) # volts / level
voff = float(scope.query('wfmoutpre:yzero?')) # reference voltage
vpos = float(scope.query('wfmoutpre:yoff?')) # reference position (level)

# error checking
r = int(scope.query('*esr?'))
print('event status register: 0b{:08b}'.format(r))
r = scope.query('allev?').strip()
print('all event messages: {}'.format(r))

scope.close()
rm.close()

# create scaled vectors
# horizontal (time)
total_time = tscale * record_length
tstop = tstart + total_time
scaled_time = np.linspace(tstart, tstop, num=record_length, endpoint=False)

# vertical (voltage)
unscaled_wave = np.array(bin_wave, dtype='double') # data type conversion
scaled_wave = (unscaled_wave - vpos) * vscale + voff
print('')



# Export Data to Excel File -----------------
#EXCEL FILE SHOULD NOT BE OPEN WHEN RUNNING CODE
print('Exporting Data')
# creating the dataframe
scope_data = pd.DataFrame({'Time': scaled_time, 'Voltage': scaled_wave})
file_name = 'BWBoscilloscope_data.xlsx' # file name


# writing to excel
DataToExcel = pd.ExcelWriter(file_name)

# writing dataframe to excel  
scope_data.to_excel(file_name)
print('Exporting Data Complete')


# Plotting Signal ----------------------------
print('Plotting Graph')
plt.plot(scaled_time, scaled_wave)
plt.title('channel 1') # plot label
plt.xlabel('time (seconds)') # x label
plt.ylabel('voltage (volts)') # y label
print("look for plot window...")
plt.show()


print("\nend of demonstration")


