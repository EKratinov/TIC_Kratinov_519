import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


n = 500
Fs = 1000
F_max = 5


random_signal = np.random.normal(0, 10, n)


time = np.arange(n) / Fs


w = F_max / (Fs / 2)
sos = signal.butter(3, w, 'low', output='sos')

# 4. Фільтрація сигналу
filtered_signal = signal.sosfiltfilt(sos, random_signal)


fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(time, filtered_signal, linewidth=1)
ax.set_xlabel("Час, с", fontsize=14)
ax.set_ylabel("Амплітуда", fontsize=14)
plt.title("Фільтрований сигнал", fontsize=14)
fig.savefig('D:/TIC_Kratinov/SignalProcessing/figures/filtered_signal.png', dpi=600)
plt.close(fig)


spectrum = np.abs(np.fft.fftshift(np.fft.fft(filtered_signal)))
freq = np.fft.fftshift(np.fft.fftfreq(n, 1 / Fs))


fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(freq, spectrum, linewidth=1)
ax.set_xlabel("Частота, Гц", fontsize=14)
ax.set_ylabel("Амплітуда", fontsize=14)
plt.title("Спектр сигналу", fontsize=14)
fig.savefig('D:/TIC_Kratinov/SignalProcessing/figures/signal_spectrum.png', dpi=600)
plt.close(fig)
