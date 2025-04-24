import random
import string
import math
from collections import Counter
import collections
import matplotlib.pyplot as plt

N_sequence_1 = 100
N1_1 = 2
N0_1 = N_sequence_1 - N1_1

list1_1 = ['1'] * N1_1
list0_1 = ['0'] * N0_1

sequence_1 = list1_1 + list0_1
random.shuffle(sequence_1)

original_sequence_1 = ''.join(sequence_1)

N_sequence_2 = 100
surname = "Кратінов"
N1_2 = len(surname)
N0_2 = N_sequence_2 - N1_2

list1_2 = list(surname)
list0_2 = ['0'] * N0_2

original_sequence_2 = ''.join(list1_2 + list0_2)

N_sequence_3 = 100
N1_3 = len(surname)
N0_3 = N_sequence_3 - N1_3

list1_3 = list(surname)
list0_3 = ['0'] * N0_3

sequence_3 = list1_3 + list0_3
random.shuffle(sequence_3)

original_sequence_3 = ''.join(sequence_3)

N_sequence_4 = 100
group_number = "519"
letters_digits = list(surname) + list(group_number)

n_letters = len(letters_digits)
n_repeats = N_sequence_4 // n_letters
remainder = N_sequence_4 % n_letters

sequence_4 = letters_digits * n_repeats + letters_digits[:remainder]
original_sequence_4 = ''.join(sequence_4)

N_sequence_5 = 100
first_two_letters = surname[:2]
elements = list(first_two_letters) + list(group_number)

sequence_5 = [random.choice(elements) for _ in range(N_sequence_5)]
random.shuffle(sequence_5)

original_sequence_5 = ''.join(sequence_5)

N_sequence_6 = 100
letters = list(surname[:2])
digits = list(group_number)

n_letters_6 = int(0.7 * N_sequence_6)
n_digits_6 = N_sequence_6 - n_letters_6

sequence_6 = [random.choice(letters) for _ in range(n_letters_6)] + [random.choice(digits) for _ in range(n_digits_6)]
random.shuffle(sequence_6)

original_sequence_6 = ''.join(sequence_6)

N_sequence_7 = 100
characters = list(string.ascii_letters + string.digits)

sequence_7 = [random.choice(characters) for _ in range(N_sequence_7)]
original_sequence_7 = ''.join(sequence_7)

with open("results_sequence.txt", "a", encoding="utf-8") as file:
    file.write(f"Послідовність №1: {original_sequence_1}\n")
    file.write(f"Розмір послідовності: {len(original_sequence_1)} byte\n")
    file.write(f"Розмір алфавіту: {len(set(original_sequence_1))}\n\n")

    file.write(f"Послідовність №2: {original_sequence_2}\n")
    file.write(f"Розмір послідовності: {len(original_sequence_2)} byte\n")
    file.write(f"Розмір алфавіту: {len(set(original_sequence_2))}\n\n")

    file.write(f"Послідовність №3: {original_sequence_3}\n")
    file.write(f"Розмір послідовності: {len(original_sequence_3)} byte\n")
    file.write(f"Розмір алфавіту: {len(set(original_sequence_3))}\n\n")

    file.write(f"Послідовність №4: {original_sequence_4}\n")
    file.write(f"Розмір послідовності: {len(original_sequence_4)} byte\n")
    file.write(f"Розмір алфавіту: {len(set(original_sequence_4))}\n\n")

    file.write(f"Послідовність №5: {original_sequence_5}\n")
    file.write(f"Розмір послідовності: {len(original_sequence_5)} byte\n")
    file.write(f"Розмір алфавіту: {len(set(original_sequence_5))}\n\n")

    file.write(f"Послідовність №6: {original_sequence_6}\n")
    file.write(f"Розмір послідовності: {len(original_sequence_6)} byte\n")
    file.write(f"Розмір алфавіту: {len(set(original_sequence_6))}\n\n")

    file.write(f"Послідовність №7: {original_sequence_7}\n")
    file.write(f"Розмір послідовності: {len(original_sequence_7)} byte\n")
    file.write(f"Розмір алфавіту: {len(set(original_sequence_7))}\n\n")


def calculate_entropy(sequence):
    count = Counter(sequence)
    total = len(sequence)
    probabilities = [freq / total for freq in count.values()]

    entropy = -sum(p * math.log2(p) for p in probabilities)
    return entropy


def calculate_redundancy(sequence):
    entropy = calculate_entropy(sequence)
    alphabet_size = len(set(sequence))
    max_entropy = math.log2(alphabet_size)

    redundancy = 1 - (entropy / max_entropy)
    return redundancy


sequences = [original_sequence_1, original_sequence_2, original_sequence_3,
             original_sequence_4, original_sequence_5, original_sequence_6, original_sequence_7]

for i, seq in enumerate(sequences, 1):
    entropy = calculate_entropy(seq)
    redundancy = calculate_redundancy(seq)
    print(f"Послідовність №{i}: Ентропія = {entropy:.4f}, Надмірність = {redundancy:.4f}")


    def calculate_probabilities(sequence):
        counts = collections.Counter(sequence)
        total = len(sequence)
        probabilities = {symbol: count / total for symbol, count in counts.items()}
        return probabilities


    def determine_uniformity(probabilities):
        mean_probability = sum(probabilities.values()) / len(probabilities)
        uniform = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in probabilities.values())
        return "рівна" if uniform else "нерівна"


    sequences = [original_sequence_1, original_sequence_2, original_sequence_3,
                 original_sequence_4, original_sequence_5, original_sequence_6, original_sequence_7]

    with open("results_sequence.txt", "a", encoding="utf-8") as file:
        for i, seq in enumerate(sequences, 1):
            probabilities = calculate_probabilities(seq)
            uniformity = determine_uniformity(probabilities)
            probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probabilities.items()])

            file.write(f"Послідовність №{i}: {seq}\n")
            file.write(f"Ймовірності появи символів: {probability_str}\n")
            file.write(f"Ймовірність розподілу символів: {uniformity}\n\n")

            print(f"Послідовність №{i}: Ймовірність розподілу символів = {uniformity}")

import matplotlib.pyplot as plt


headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
rows = [f'Послідовність {i+1}' for i in range(7)]

data = [
    [2, 0.1414, 0.8586, "нерівна"],
    [9, 0.6422, 0.7974, "нерівна"],
    [9, 0.6422, 0.7974, "нерівна"],
    [11, 3.4587, 0.0002, "нерівна"],
    [5, 2.2869, 0.0151, "нерівна"],
    [5, 2.0306, 0.1255, "нерівна"],
    [52, 5.4437, 0.0305, "нерівна"]
]

fig, ax = plt.subplots(figsize=(8, 6))
ax.axis('off')
table = ax.table(cellText=data, colLabels=headers, rowLabels=rows, loc='center', cellLoc='center')

table.set_fontsize(12)
table.scale(1, 1.5)

plt.title("Характеристики сформованих послідовностей")
plt.savefig("table_characteristics.png", dpi=300)
plt.show()


sequence = "bZYfBllLFQepWZ4nX2hvK0QX78xil4mAZPYZMTjEeiLnwUlqNGlljvuUFc6kWRYEzBTwUI7R33OPfCwEoJlHNiDyMlWfRHBZhWw1"

counts = collections.Counter(sequence)

plt.figure(figsize=(12, 6))
plt.bar(counts.keys(), counts.values(), color='skyblue')

plt.xlabel("Символи")
plt.ylabel("Кількість входжень")
plt.title("Частоти появи символів у послідовності №7")
plt.xticks(rotation=90)

plt.savefig("histogram_sequence7.png", dpi=300)
plt.show()