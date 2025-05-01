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
    if not sequence:
        return [], {}

    unique_symbols = sorted(set(sequence))
    dictionary = {symbol: i for i, symbol in enumerate(unique_symbols)}
    reverse_dict = {i: symbol for symbol, i in dictionary.items()}
    dict_size = len(dictionary)

    current = ""
    result = []

    for symbol in sequence:
        new_str = current + symbol
        if new_str in dictionary:
            current = new_str
        else:
            result.append(dictionary[current])
            dictionary[new_str] = dict_size
            dict_size += 1
            current = symbol

    if current:
        result.append(dictionary[current])

    return result, reverse_dict



def decode_lzw(encoded_sequence, dictionary):
    if not encoded_sequence:
        return ""

    dict_size = max(dictionary) + 1 if dictionary else 0
    decoded = []

    previous_code = encoded_sequence[0]
    previous = dictionary.get(previous_code, "")
    decoded.append(previous)

    for code in encoded_sequence[1:]:
        if code in dictionary:
            current = dictionary[code]
        else:
            current = previous + previous[0]

        decoded.append(current)
        dictionary[dict_size] = previous + current[0]
        dict_size += 1
        previous = current

    return "".join(decoded)


def save_results(original_sequences, filename="results_rle_lzw.txt"):
    results = []
    with open(filename, "w", encoding="utf-8") as file:
        for i, sequence in enumerate(original_sequences, start=1):
            entropy = calculate_entropy(sequence)

            # RLE
            encoded_rle = encode_rle(sequence)
            decoded_rle = decode_rle(encoded_rle)
            len_original = len(sequence)
            len_encoded_rle = len(encoded_rle)
            len_decoded_rle = len(decoded_rle)
            compression_ratio_rle = round(len_original / len_encoded_rle, 2) if len_encoded_rle > 0 else "-"

            # LZW
            encoded_lzw, reverse_dict = encode_lzw(sequence)
            decoded_lzw = decode_lzw(encoded_lzw, reverse_dict)
            lzw_bit_length = sum(math.ceil(math.log2(code + 1)) for code in encoded_lzw) if encoded_lzw else 1
            compression_ratio_lzw = round((len_original * 8) / lzw_bit_length, 2) if lzw_bit_length > 0 else "-"
            len_encoded_lzw = len(encoded_lzw)
            len_decoded_lzw = len(decoded_lzw)

            # Запис результатів
            file.write(f"Послідовність {i}:\n")
            file.write(f"Оригінальна: {sequence}\n")
            file.write(f"Ентропія: {entropy:.4f}\n")

            file.write(f"RLE кодування: {encoded_rle}\n")
            file.write(f"Декодована RLE: {decoded_rle}\n")
            file.write(f"Довжина оригіналу: {len_original}, довжина RLE: {len_encoded_rle}, довжина декодування RLE: {len_decoded_rle}\n")
            file.write(f"КС RLE: {compression_ratio_rle}\n")

            file.write(f"LZW кодування: {encoded_lzw}\n")
            file.write(f"Декодована LZW: {decoded_lzw}\n")
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


sequence = "AAAAABBBCCCCDDDDAAAA"
encoded_rle = encode_rle(sequence)
decoded_rle = decode_rle(encoded_rle)
original_sequences = read_sequences("results_sequence.txt")

print(original_sequences)

original_sequences = read_sequences("results_sequence.txt")
results = save_results(original_sequences)
visualize_results(results)

test_sequence = "ABABA"
encoded_test, reverse_dict = encode_lzw(test_sequence)
decoded_test = decode_lzw(encoded_test, reverse_dict)

print("Оригинал:", test_sequence)
print("Закодированная:", encoded_test)
print("Декодированная:", decoded_test)
