import numpy as np
import matplotlib.pyplot as plt

def generate_pulse(frequency, duration, duty_cycle):
    # Calculate the number of samples based on the frequency
    num_samples = int(frequency * duration)

    # Generate time data for the waveform
    t = np.linspace(0, duration, num_samples, endpoint=False)

    # Generate the waveform by creating an array with alternating values of 1 and 0
    waveform = np.zeros(num_samples)
    waveform[0:int(duty_cycle * num_samples)] = 1

    return t, waveform

# Define the parameters for the waveform
frequency = 10 # Hz
duration = 1 # seconds
duty_cycle = 0.5 # fraction of the waveform that is high

# Call the function to generate the pulse
t, waveform = generate_pulse(frequency, duration, duty_cycle)

# Plot the waveform
plt.plot(t, waveform)
plt.title("Square Wave Pulse")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()
