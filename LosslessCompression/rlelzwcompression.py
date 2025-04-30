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
        return []
    dictionary = {chr(i): i for i in range(65536)}
    current = ""
    result = []
    for c in sequence:
        new_str = current + c
        if new_str in dictionary:
            current = new_str
        else:
            if current:
                result.append(dictionary[current])
            dictionary[new_str] = len(dictionary)
            current = c
    if current:
        result.append(dictionary[current])
    return result


def decode_lzw(encoded_sequence):
    if not encoded_sequence:
        return ""

    dictionary = {i: chr(i) for i in range(256)}

    if not encoded_sequence:
        return ""

    previous = dictionary.get(encoded_sequence.pop(0), "")
    if not previous:
        return ""

    result = [previous]
    for code in encoded_sequence:
        current = dictionary.get(code, previous + previous[0] if previous else "")
        result.append(current)
        dictionary[len(dictionary)] = previous + (current[0] if current else "")
        previous = current

    return "".join(result)


def save_results(original_sequences, filename="results_rle_lzw.txt"):
    results = []
    with open(filename, "w", encoding="utf-8") as file:
        for i, sequence in enumerate(original_sequences, start=1):
            entropy = calculate_entropy(sequence)
            encoded_rle = encode_rle(sequence)
            compression_ratio_rle = round(len(sequence) / len(encoded_rle), 2) if encoded_rle else "-"
            decoded_rle = decode_rle(encoded_rle)
            encoded_lzw = encode_lzw(sequence) if sequence else []
            compression_ratio_lzw = round(
                len(sequence) * 16 / sum(math.ceil(math.log2(code + 1)) for code in encoded_lzw), 2) if encoded_lzw else "-"
            decoded_lzw = decode_lzw(encoded_lzw) if encoded_lzw else ""

            file.write(f"Послідовність {i}:\n")
            file.write(f"Оригінальна: {sequence}\n")
            file.write(f"Ентропія: {entropy:.4f}\n")
            file.write(f"RLE: {encoded_rle}, КС: {compression_ratio_rle}\n")
            file.write(f"LZW: {encoded_lzw}, КС: {compression_ratio_lzw}\n\n")

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
