from random import randint
import numpy as np
import matplotlib.pyplot as plt
import os
from math import sin, cos, pi
import scipy.fft

def plot(x, y, axis_x="", axis_y="", title=""):
    plt.figure(figsize=(8.27, 5.51))
    plt.plot(x, y, linewidth=1)
    plt.xlabel(axis_x, fontsize=14)
    plt.ylabel(axis_y, fontsize=14)
    plt.title(title, fontsize=14)
    os.makedirs('./figures/', exist_ok=True)
    plt.savefig(f'./figures/{title}.png', dpi=600)
    plt.close()

def spectrum(seq):
    y = np.abs(scipy.fft.fftshift(scipy.fft.fft(seq)))
    x = scipy.fft.fftshift(scipy.fft.fftfreq(len(seq), 1 / len(seq)))
    return x[len(x)//2:], y[len(y)//2:]

def create_sequence():
    return np.concatenate([[v] * 100 for v in np.random.randint(0, 2, 10)])

def ask_modulation(f, seq):
    return np.array([seq[i] * cos(2 * pi * f * i / 1000) for i in range(len(seq))])

def psk_modulation(f, seq):
    return np.array([sin(2 * pi * f * i / 1000 + seq[i] * pi + pi) for i in range(len(seq))])

def fsk_modulation(f1, f2, seq):
    return np.array([seq[i] * sin(2 * pi * f1 * i / 1000) + (1 - seq[i]) * sin(2 * pi * f2 * i / 1000) for i in range(len(seq))])

def ask_demodulation(f, seq):
    prod = np.array([seq[i] * cos(2 * pi * f * i / 1000) for i in range(len(seq))])
    return _demodulate(prod)

def psk_demodulation(f, seq):
    prod = np.array([seq[i] * sin(2 * pi * f * i / 1000) for i in range(len(seq))])
    return _demodulate(prod)

def fsk_demodulation(f1, f2, seq):
    prod1 = np.array([seq[i] * sin(2 * pi * f1 * i / 1000) for i in range(len(seq))])
    prod2 = np.array([seq[i] * sin(2 * pi * f2 * i / 1000) for i in range(len(seq))])
    demod1, _ = _demodulate(prod1)
    demod2, _ = _demodulate(prod2)
    bits = 0.5 * (np.sign(demod1 - demod2) + 1)
    seq_demod = np.concatenate([[bits[i * 100]] * 100 for i in range(10)])
    return demod1, demod2, seq_demod

def _demodulate(prod):
    signal = np.zeros_like(prod)
    for i in range(10):
        S = sum(prod[i*100:(i+1)*100])
        signal[i*100:(i+1)*100] = S
    bits = 0.5 * (np.sign(signal - 25) + 1)
    seq_demod = np.concatenate([[bits[i * 100]] * 100 for i in range(10)])
    return signal, seq_demod

def create_noise(mean, std, length):
    return np.random.normal(mean, std, length)

def noise_stress(seq, mod_seq, mod_type, freqs):
    errors = []
    for i in range(20):
        err_sum = 0
        for _ in range(200):
            noisy = mod_seq + i * create_noise(0, 1, 1000)
            if mod_type == "ASK":
                _, demod = ask_demodulation(freqs[0], noisy)
            elif mod_type == "PSK":
                _, demod = psk_demodulation(freqs[0], noisy)
            else:
                _, _, demod = fsk_demodulation(freqs[0], freqs[1], noisy)
            err_sum += np.abs(seq - demod).sum() / 1000
        errors.append(err_sum / 200)
    return errors

def main(ask, psk, fsk1, fsk2):
    seq = create_sequence()
    x = np.arange(len(seq)) / 1000
    plot(x, seq, "Час, с", "Амплітуда", "Згенерована послідовність")

    mods = {
        "АМ": ask_modulation(ask, seq),
        "ФМ": psk_modulation(psk, seq),
        "ЧМ": fsk_modulation(fsk1, fsk2, seq)
    }
    for name, s in mods.items():
        plot(x, s, "Час, с", "Амплітуда", f"{name} модуляція")
        fx, fy = spectrum(s)
        plot(fx, fy, "Частота, Гц", "Амплітуда спектру", f"Спектр при {name.lower()} модуляції")

    noise = create_noise(0, 1, 1000)
    ask_noisy = mods["АМ"] + noise
    psk_noisy = mods["ФМ"] + noise
    fsk_noisy = mods["ЧМ"] + noise
    plot(x, ask_noisy, "Час, с", "Амплітуда", "АМ з шумом")
    plot(x, psk_noisy, "Час, с", "Амплітуда", "ФМ з шумом")
    plot(x, fsk_noisy, "Час, с", "Амплітуда", "ЧМ з шумом")

    y, d = ask_demodulation(ask, ask_noisy)
    plot(x, y, "Час, с", "Амплітуда", "Демодуляція АМ")
    plot(x, d, "Час, с", "Амплітуда", "Послідовність після АМ")

    y, d = psk_demodulation(psk, psk_noisy)
    plot(x, y, "Час, с", "Амплітуда", "Демодуляція ФМ")
    plot(x, d, "Час, с", "Амплітуда", "Послідовність після ФМ")

    y1, y2, d = fsk_demodulation(fsk1, fsk2, fsk_noisy)
    plot(x, y1, "Час, с", "Амплітуда", "Демодуляція ЧМ - 1")
    plot(x, y2, "Час, с", "Амплітуда", "Демодуляція ЧМ - 2")
    plot(x, d, "Час, с", "Амплітуда", "Послідовність після ЧМ")

    e_ask = noise_stress(seq, mods["АМ"], "ASK", [ask])
    e_psk = noise_stress(seq, mods["ФМ"], "PSK", [psk])
    e_fsk = noise_stress(seq, mods["ЧМ"], "FSK", [fsk1, fsk2])

    plt.figure(figsize=(8.27, 5.51))
    plt.plot(range(20), e_ask, label="ASK")
    plt.plot(range(20), e_psk, label="PSK")
    plt.plot(range(20), e_fsk, label="FSK")
    plt.xlabel("Діапазон змін шуму", fontsize=14)
    plt.ylabel("Ймовірність помилки", fontsize=14)
    plt.title("Оцінка завадостійкості трьох видів модуляції", fontsize=14)
    plt.legend()
    os.makedirs('./figures/', exist_ok=True)
    plt.savefig('./figures/Оцінка завадостійкості трьох видів модуляції.png', dpi=600)
    plt.close()


main(40, 40, 60, 30)
