import visa # package that allows configuring, programming, and troubleshooting instrumentation systems comprising GPIB, VXI, PXI, Serial, Ethernet, and/or USB interfaces
import pyvisa # package that enables me to control all kinds of measurement devices independent of the interface

#https://pyvisa.readthedocs.io/en/latest/introduction/configuring.html 
# rm = ResourceManager('Path to library')# constructor to set path manually 
rm = pyvisa.ResourceManager() #Pyvisa can find Visa USUALLY, if not use a consructor 
rm.list_resources()
print(rm)

# instrument name can be found in NI Max 
my_instrument = rm.open_resource('instrument name')

#query = question
#asking the insturment's a question:"what are you?/ what is on your current display"
print(my_instrument.query('*IDN?'))

# using query is a short version of operation write & read
my_instruemnt.write('*IDN?')
print(my_instruemnt.read())

# to prevent VISAIOERROR, you need to properly set up the read & write termination attributes
# n = line feed
# r = carriage return
# null = 0
my_instrument.read_termination = '\n'
my_instrument.write_termination = '\n'
my_instrument.query('*IDN?')

while True:
    print(my_instrument.read_bytes(1))
#baund rate is a rate of infomation transferred in a communcation channel
#E.g 9600 baud = series port is capable of transfering a max of 9600 bits per sec
my_instrument.baud_rate = 57600 # my instrumetn had a baud rate of 57600 bits/per sec
#A GOOD baud rate is 5x or more than the fundamental frequency, 10x the 1st harmonic

