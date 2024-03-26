import numpy as np

def create_shingles(text, k=3):
    return set([text[i:i+k] for i in range(len(text) - k + 1)])

def one_hot_encoding(shingles, vocab_size):
    encoding = np.zeros(vocab_size)
    for idx, shingle in enumerate(shingles):
        encoding[hash(shingle) % vocab_size] = 1
    return encoding

def min_hashing(signature_matrix, num_hashes):
    num_rows, num_cols = signature_matrix.shape
    hash_values = np.full((num_hashes, num_cols), np.inf)
    
    for i in range(num_rows):
        for j in range(num_cols):
            if signature_matrix[i, j] == 1:
                for k in range(num_hashes):
                    hash_val = (3 * i + 13 * j + 17 * k) % num_hashes
                    hash_values[k, j] = min(hash_values[k, j], hash_val)
    
    return hash_values

def create_buckets(hash_values):
    buckets = {}
    for i, hash_val in enumerate(hash_values):
        bucket_key = tuple(hash_val)
        if bucket_key not in buckets:
            buckets[bucket_key] = []
        buckets[bucket_key].append(i)
    return buckets

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

def calculate_similarity_with_buckets_and_bands(sentence1, sentence2, k, vocab_size, num_hashes, num_bands):
    shingles1 = create_shingles(sentence1, k)
    shingles2 = create_shingles(sentence2, k)
    
    encoding1 = one_hot_encoding(shingles1, vocab_size)
    encoding2 = one_hot_encoding(shingles2, vocab_size)
    
    signature_matrix = np.vstack((encoding1, encoding2))
    
    hash_values1 = min_hashing(np.array([encoding1]), num_hashes)[0]
    hash_values2 = min_hashing(np.array([encoding2]), num_hashes)[0]
    
    # Create buckets for each band
    buckets1 = [hash(tuple(hash_values1[i:i+num_bands])) for i in range(0, len(hash_values1), num_bands)]
    buckets2 = [hash(tuple(hash_values2[i:i+num_bands])) for i in range(0, len(hash_values2), num_bands)]
    
    # Calculate similarity based on buckets
    bucket_similarity = sum(int(b1 == b2) for b1, b2 in zip(buckets1, buckets2)) / num_bands
    
    return bucket_similarity


# Example usage
sentence1 = "A quick brown fox jumps over the lazy dog"
sentence2 = "A quick brown fox jumps under the dog"
k = 2
vocab_size = 100
num_hashes = 100

# Example usage
num_bands = 10
similarity = calculate_similarity_with_buckets_and_bands(sentence1, sentence2, k, vocab_size, num_hashes, num_bands)
print(similarity)


