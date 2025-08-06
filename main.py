import wfdb
import matplotlib.pyplot as plt
import numpy as np

# Load ECG Record 100 (Normal)
record_100 = wfdb.rdrecord('100')
ann_100 = wfdb.rdann('100', 'atr')

# Load ECG Record 200 (Abnormal arrhythmia)
record_200 = wfdb.rdrecord('200')
ann_200 = wfdb.rdann('200', 'atr')

# Sampling frequency
fs = record_100.fs
samples = int(fs * 10)  # First 10 seconds

# Extract first 10 seconds of signal
sig_100 = record_100.p_signal[:samples, 0]
sig_200 = record_200.p_signal[:samples, 0]

# Get R-peaks for each
rpeaks_100 = [i for i in ann_100.sample if i < samples]
rpeaks_200 = [i for i in ann_200.sample if i < samples]

# Normalize both signals for visual comparison
def normalize(signal):
    return (signal - np.mean(signal)) / np.std(signal)

sig_100_norm = normalize(sig_100)
sig_200_norm = normalize(sig_200)

# Plotting
plt.figure(figsize=(14, 6))

# Plot 100 (Normal)
plt.subplot(2, 1, 1)
plt.plot(sig_100_norm, label='Normal ECG (Record 100)', color='blue')
plt.plot(rpeaks_100, sig_100_norm[rpeaks_100], 'ro', label='R-peaks')
plt.title('Normalized ECG – Normal Rhythm (First 10 Seconds)')
plt.ylabel('Normalized Voltage')
plt.grid(True)
plt.legend()

# Plot 200 (Abnormal)
plt.subplot(2, 1, 2)
plt.plot(sig_200_norm, label='Abnormal ECG (Record 200)', color='orange')
plt.plot(rpeaks_200, sig_200_norm[rpeaks_200], 'ro', label='R-peaks')

# Highlight irregular RR intervals
for i in range(1, len(rpeaks_200)):
    rr_interval = rpeaks_200[i] - rpeaks_200[i - 1]
    if rr_interval < fs * 0.5 or rr_interval > fs * 1.5:
        plt.axvspan(rpeaks_200[i - 1], rpeaks_200[i], color='red', alpha=0.2)

plt.title('Normalized ECG – Abnormal Rhythm (First 10 Seconds)')
plt.xlabel('Sample')
plt.ylabel('Normalized Voltage')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()