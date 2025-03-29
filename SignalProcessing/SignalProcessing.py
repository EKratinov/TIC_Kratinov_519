import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
import os


output_dir = "D:/TIC_Kratinov/SignalProcessing/figures"
os.makedirs(output_dir, exist_ok=True)


n = 500
Fs = 1000
F_max = 5
filter_band = 10


random_signal = np.random.normal(0, 10, n)
time = np.arange(n) / Fs


w = F_max / (Fs / 2)
sos = signal.butter(3, w, 'low', output='sos')
filtered_signal = signal.sosfiltfilt(sos, random_signal)


Dt_values = [2, 4, 8, 16]
discrete_signals = []
discrete_spectrums = []
restored_signals = []
errors = []
snr_values = []
frequencies = fft.fftshift(fft.fftfreq(n, 1 / Fs))

for Dt in Dt_values:
    discrete_signal = np.zeros_like(filtered_signal)
    discrete_signal[::Dt] = filtered_signal[::Dt]
    discrete_signals.append(discrete_signal)


    spectrum = np.abs(fft.fftshift(fft.fft(discrete_signal)))
    discrete_spectrums.append(spectrum)


    w_restore = filter_band / (Fs / 2)
    sos_restore = signal.butter(3, w_restore, 'low', output='sos')
    restored_signal = signal.sosfiltfilt(sos_restore, discrete_signal)
    restored_signals.append(restored_signal)


    error = restored_signal - filtered_signal
    error_var = np.var(error)
    errors.append(error_var)
    snr_values.append(np.var(filtered_signal) / error_var if error_var != 0 else np.inf)



def save_plot(x, y, title, xlabel, ylabel, filename):
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(x, np.array(y), linewidth=1)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.set_title(title, fontsize=14)
    filepath = os.path.join(output_dir, f"{filename}.png")
    fig.savefig(filepath, dpi=600)
    plt.close(fig)



save_plot(time, filtered_signal, "Фільтрований сигнал", "Час (с)", "Амплітуда", "filtered_signal")

for i, Dt in enumerate(Dt_values):
    save_plot(time, discrete_signals[i], f"Дискретизований сигнал (Dt={Dt})", "Час (с)", "Амплітуда",
              f"discrete_signal_Dt{Dt}")
    save_plot(frequencies, discrete_spectrums[i], f"Спектр дискретного сигналу (Dt={Dt})", "Частота (Гц)", "Амплітуда",
              f"discrete_spectrum_Dt{Dt}")
    save_plot(time, restored_signals[i], f"Відновлений сигнал (Dt={Dt})", "Час (с)", "Амплітуда",
              f"restored_signal_Dt{Dt}")


save_plot(Dt_values, errors, "Дисперсія помилки від кроку дискретизації", "Крок дискретизації (Dt)", "Дисперсія",
          "error_vs_dt")


save_plot(Dt_values, snr_values, "Співвідношення сигнал-шум від кроку дискретизації", "Крок дискретизації (Dt)", "SNR",
          "snr_vs_dt")

print(f"Завдання виконано! Всі графіки збережено в '{output_dir}'.")
