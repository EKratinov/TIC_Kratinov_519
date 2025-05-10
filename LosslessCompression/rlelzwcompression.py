import collections
import math
import matplotlib.pyplot as plt


def read_sequences(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    sequences = [line.split(": ")[1].strip() for line in lines if line.startswith("Послідовність №")]

    return sequences


def calculate_entropy(sequence):
    if not sequence:
        return 0.0
    counts = collections.Counter(sequence)
    probability = {symbol: count / len(sequence) for symbol, count in counts.items()}
    return -sum(p * math.log2(p) for p in probability.values())


def encode_rle(sequence):
    if not sequence:
        return ""
    encoded = []
    count = 1
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            count += 1
        else:
            encoded.append(f"{count}{sequence[i - 1]}")
            count = 1
    encoded.append(f"{count}{sequence[-1]}")
    return "".join(encoded)


def decode_rle(encoded_sequence):
    if not encoded_sequence:
        return ""
    decoded = []
    i = 0
    while i < len(encoded_sequence):
        if not encoded_sequence[i].isdigit():
            return ""
        count = int(encoded_sequence[i])
        if i + 1 >= len(encoded_sequence):
            return ""
        symbol = encoded_sequence[i + 1]
        decoded.extend([symbol] * count)
        i += 2
    return "".join(decoded)


def encode_lzw(sequence):
    dictionary = {}
    for i in range(65536):
        dictionary[chr(i)] = i
    current = ""
    result = []
    size = 0
    for c in sequence:
        new_str = current + c
        if new_str in dictionary:
            current = new_str
        else:
            result.append(dictionary[current])
            dictionary[new_str] = len(dictionary)
            element_bits = 16 if dictionary[current] < 65536 else math.ceil(math.log2(len(dictionary)))
            current = c
            with open("results_rle_lzw.txt", "a") as file:
                file.write(f"Code: {dictionary[current]}, Element: {current}, bits: {element_bits}\n")
                file.close()
            size = size + element_bits
    last = 16 if dictionary[current] < 65536 else math.ceil(math.log2(len(dictionary)))
    size = size + last
    with open("results_rle_lzw.txt", "a") as file:
        file.write(f"Code: {dictionary[current]}, Element: {current}, Bits: {last}\n")
    result.append(dictionary[current])
    return result, size


def decode_lzw(sequence):
    dictionary = {}
    for i in range(65536):
        dictionary[i] = chr(i)
    result = ""
    previous = None
    current = ""
    for code in sequence:
        if code in dictionary:
            current = dictionary[code]
            result += current
            if previous is not None:
                dictionary[len(dictionary)] = previous + current[0]
            previous = current
        else:
            current = previous + previous[0]
            result += current
            dictionary[len(dictionary)] = current
            previous = current
    return result


def save_results(original_sequences, filename="results_rle_lzw.txt"):
    results = []
    with open(filename, "w", encoding="utf-8") as file:
        for i, sequence in enumerate(original_sequences, start=1):
            entropy = calculate_entropy(sequence)

            encoded_rle = encode_rle(sequence)
            decoded_rle = decode_rle(encoded_rle)
            len_original = len(sequence)
            len_encoded_rle = len(encoded_rle)
            len_decoded_rle = len(decoded_rle)
            compression_ratio_rle = round(len_original / len_encoded_rle, 2) if len_encoded_rle > 0 else "-"

            encoded_result, size = encode_lzw(sequence)
            decoded_result_LZW = decode_lzw(encoded_result)
            len_encoded_lzw = len(encoded_result)
            len_decoded_lzw = len(decoded_result_LZW)
            compression_ratio_lzw = round((len_original * 8) / size, 2) if size > 0 else "-"

            file.write(f"Послідовність {i}:\n")
            file.write(f"Оригінальна: {sequence}\n")
            file.write(f"Ентропія: {entropy:.4f}\n")
            file.write(f"RLE кодування: {encoded_rle}\n")
            file.write(f"Декодована RLE: {decoded_rle}\n")
            file.write(f"Довжина оригіналу: {len_original}, довжина RLE: {len_encoded_rle}, довжина декодування RLE: {len_decoded_rle}\n")
            file.write(f"КС RLE: {compression_ratio_rle}\n")
            file.write(f"LZW кодування: {encoded_result}\n")
            file.write(f"Декодована LZW: {decoded_result_LZW}\n")
            file.write(f"Довжина закодованої LZW: {len_encoded_lzw}, довжина декодованої LZW: {len_decoded_lzw}\n")
            file.write(f"КС LZW: {compression_ratio_lzw}\n\n")

            results.append([round(entropy, 2), compression_ratio_rle, compression_ratio_lzw])
    return results


def visualize_results(results):
    headers = ['Ентропія', 'КС RLE', 'КС LZW']
    row_labels = [f"Послідовність {i + 1}" for i in range(len(results))]

    fig, ax = plt.subplots(figsize=(12, len(results) / 1.5))
    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=row_labels, loc='center', cellLoc='center')
    table.set_fontsize(14)
    table.scale(0.8, 2)

    fig.savefig("Результати_стиснення.png")


original_sequences = read_sequences("results_sequence.txt")
results = save_results(original_sequences)
visualize_results(results)