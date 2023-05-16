import pyvisa

# Establish connection to the function generator
rm = pyvisa.ResourceManager()
fg = rm.open_resource('<VISA address of function generator>')

# Set up the function generator to output a pulse
fg.write('FUNC PULS')
fg.write('PULS:DCYC 50')
fg.write('PULS:WIDT 0.1m')
fg.write('PULS:PER 1')
fg.write('VOLT:UNIT VPP')
fg.write('VOLT 1')
fg.write('OUTP ON')

# Close connection to function generator
fg.close()
