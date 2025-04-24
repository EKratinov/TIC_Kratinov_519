import collections
import math
import random
import string
import matplotlib.pyplot as plt

N_sequence = 100
surname = "Кратінов"
group_number = "519"


sequence_1 = ''.join(random.sample(['1'] * 2 + ['0'] * (N_sequence - 2), N_sequence))
sequence_2 = surname.ljust(N_sequence, '0')
sequence_3 = ''.join(random.sample(list(surname) + ['0'] * (N_sequence - len(surname)), N_sequence))
sequence_4 = ''.join((surname + group_number) * (N_sequence // len(surname + group_number)))[:N_sequence]
sequence_5 = ''.join((surname[:2] + group_number) * 20)[:N_sequence]
sequence_6 = ''.join(random.choices(surname[:2], k=int(N_sequence * 0.7)) + random.choices(group_number, k=int(N_sequence * 0.3)))
sequence_7 = ''.join(random.choices(string.ascii_letters + string.digits, k=N_sequence))
sequence_8 = '1' * N_sequence

original_sequences = [sequence_1, sequence_2, sequence_3, sequence_4, sequence_5, sequence_6, sequence_7, sequence_8]



def calculate_probabilities(sequence):
    counts = collections.Counter(sequence)
    total = len(sequence)
    probabilities = {symbol: count / total for symbol, count in counts.items()}
    return probabilities


def calculate_entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities.values())


def calculate_redundancy(entropy, alphabet_size):
    return 1 - (entropy / math.log2(alphabet_size)) if alphabet_size > 1 else 1



with open("results_sequence.txt", "w", encoding="utf-8") as file:
    results = []
    for i, seq in enumerate(original_sequences, 1):
        probabilities = calculate_probabilities(seq)
        entropy = calculate_entropy(probabilities)
        redundancy = calculate_redundancy(entropy, len(set(seq)))
        avg_prob = sum(probabilities.values()) / len(probabilities)
        probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probabilities.items()])

        file.write(f"Послідовність №{i}: {seq}\n")
        file.write(f"Розмір послідовності: {len(seq)} byte\n")
        file.write(f"Розмір алфавіту: {len(set(seq))}\n")
        file.write(f"Середнє арифметичне ймовірностей: {avg_prob:.4f}\n")
        file.write(f"Ймовірності появи символів: {probability_str}\n")
        file.write(f"Ентропія: {entropy:.4f}\n")
        file.write(f"Надмірність джерела: {redundancy:.4f}\n\n")

        results.append([len(set(seq)), round(entropy, 2), round(redundancy, 2),
                        "нерівна" if entropy < math.log2(len(set(seq))) else "рівна"])


fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')
table = ax.table(cellText=results, colLabels=["Розмір алфавіту", "Ентропія", "Надмірність", "Ймовірність"],
                 rowLabels=[f'Послідовність {i}' for i in range(1, 9)], loc='center', cellLoc='center')

table.set_fontsize(12)
table.scale(1, 1.5)
plt.title("Характеристики сформованих послідовностей")
plt.savefig("table_characteristics.png", dpi=300)
plt.show()
