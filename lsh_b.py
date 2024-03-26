import numpy as np
import random

# Generate two random audios
audio1 = [random.randint(-20, 20) for _ in range(1000000)]
audio2 = [random.randint(-20, 20) for _ in range(1000000)]

# Define the function to create shingles
def create_shingles(audio, k=2):
    return set([tuple(audio[i:i+k]) for i in range(len(audio) - k + 1)])

# Define the function for one-hot encoding
def one_hot_encoding(shingles, vocab_size):
    encoding = np.zeros(vocab_size)
    for shingle in shingles:
        encoding[hash(shingle) % vocab_size] = 1
    return encoding

# Define the function for min-hashing
def min_hashing(encoding, num_hashes):
    hash_values = np.full(num_hashes, np.inf)
    for i in range(len(encoding)):
        if encoding[i] == 1:
            for k in range(num_hashes):
                hash_val = random.randint(0, 4)
                hash_values[k] = min(hash_values[k], hash_val)
    return hash_values

# Define the function to create buckets
def create_buckets(hash_values, num_bands):
    return [hash(tuple(hash_values[i:i+num_bands])) for i in range(0, len(hash_values), num_bands)]

# Define the function for Dice similarity
def dice_similarity(buckets1, buckets2):
    intersection = len(set(buckets1).intersection(set(buckets2)))
    total_length = len(buckets1) + len(buckets2)
    return 2 * intersection / total_length

# Define the parameters
k = 2
vocab_size = 1000000
num_hashes = 100
num_bands = 10

# Create shingles for the audios
shingles1 = create_shingles(audio1, k)
shingles2 = create_shingles(audio2, k)

# Apply one-hot encoding to the shingles
encoding1 = one_hot_encoding(shingles1, vocab_size)
encoding2 = one_hot_encoding(shingles2, vocab_size)

# Apply min-hashing to the encodings
hash_values1 = min_hashing(encoding1, num_hashes)
hash_values2 = min_hashing(encoding2, num_hashes)

# Create buckets for each band
buckets1 = create_buckets(hash_values1, num_bands)
buckets2 = create_buckets(hash_values2, num_bands)

# Calculate the Dice similarity between the two audios
similarity = dice_similarity(buckets1, buckets2)

# Print the Dice similarity
print(f"The Dice similarity between the two audios is {similarity}.")
