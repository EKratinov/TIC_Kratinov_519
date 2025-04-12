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
    save_plot(time, discrete_signals[i], f"Дискретизований сигнал (Dt={Dt})", "Час (с)", "Амплітуда", f"discrete_signal_Dt{Dt}")
    save_plot(frequencies, discrete_spectrums[i], f"Спектр дискретного сигналу (Dt={Dt})", "Частота (Гц)", "Амплітуда", f"discrete_spectrum_Dt{Dt}")
    save_plot(time, restored_signals[i], f"Відновлений сигнал (Dt={Dt})", "Час (с)", "Амплітуда", f"restored_signal_Dt{Dt}")

save_plot(Dt_values, errors, "Дисперсія помилки від кроку дискретизації", "Крок дискретизації (Dt)", "Дисперсія", "error_vs_dt")
save_plot(Dt_values, snr_values, "Співвідношення сигнал-шум від кроку дискретизації", "Крок дискретизації (Dt)", "SNR", "snr_vs_dt")

# === КВАНТУВАННЯ ===
quant_levels = [4, 16, 64, 256]
quantized_signals = []
quant_errors = []
quant_snrs = []

for M in quant_levels:
    delta = (np.max(filtered_signal) - np.min(filtered_signal)) / (M - 1)
    quantize_signal = delta * np.round(filtered_signal / delta)
    quantized_signals.append(quantize_signal)

    quantize_levels = np.arange(np.min(quantize_signal), np.max(quantize_signal)+delta, delta)
    quantize_bit = np.arange(0, M)
    bit_len = int(np.log2(M))
    quantize_bit = [format(bits, '0' + str(bit_len) + 'b') for bits in quantize_bit]

    quantize_table = np.c_[quantize_levels[:M], quantize_bit[:M]]

    fig, ax = plt.subplots(figsize=(14/2.54, M/2.54))
    table = ax.table(cellText=quantize_table, colLabels=['Значення сигналу', 'Кодова послідовність'], loc='center')
    table.set_fontsize(14)
    table.scale(1, 2)
    ax.axis('off')
    fig.savefig(os.path.join(output_dir, f"quant_table_{M}.png"), dpi=600)
    plt.close(fig)

    bits = []
    for signal_value in quantize_signal:
        for index, value in enumerate(quantize_levels[:M]):
            if np.round(np.abs(signal_value - value), 0) == 0:
                bits.append(quantize_bit[index])
                break

    flat_bits = [int(bit) for bit in ''.join(bits)]
    x = np.arange(0, len(flat_bits))
    y = flat_bits

    fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
    ax.step(x, y, linewidth=0.1)
    ax.set_title(f"Бітова послідовність сигналу (M={M})")
    ax.set_xlabel("Індекс біта")
    ax.set_ylabel("Значення біта")
    fig.savefig(os.path.join(output_dir, f"bit_sequence_{M}.png"), dpi=600)
    plt.close(fig)

    quant_error = filtered_signal - quantize_signal
    quant_var = np.var(quant_error)
    quant_error_power = np.var(quant_error)
    signal_power = np.var(filtered_signal)
    snr = signal_power / quant_error_power if quant_error_power != 0 else np.inf

    quant_errors.append(quant_var)
    quant_snrs.append(snr)


plt.figure(figsize=(12, 8))
for i, M in enumerate(quant_levels):
    plt.plot(time, quantized_signals[i], label=f"M={M}")
plt.xlabel("Час (с)")
plt.ylabel("Амплітуда")
plt.title("Цифрові сигнали при різному M")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "all_quantized_signals.png"), dpi=600)
plt.close()


save_plot(quant_levels, quant_errors, "Дисперсія квантованого сигналу", "Кількість рівнів M", "Дисперсія", "quant_error_vs_m")


save_plot(quant_levels, quant_snrs, "SNR квантованого сигналу", "Кількість рівнів M", "SNR", "quant_snr_vs_m")

print(f"Завдання виконано! Всі графіки збережено в '{output_dir}'.")
