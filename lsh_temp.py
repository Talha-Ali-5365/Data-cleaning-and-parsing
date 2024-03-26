def create_shingles(text, k=3):
    return set([text[i:i+k] for i in range(len(text) - k + 1)])

def jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection)/len(union)

def minhash_signature(shingle_set, hash_funcs):
    signature = []
    for func in hash_funcs:
        min_hash = min([func(shingle) for shingle in shingle_set])
        signature.append(min_hash)
    return signature

p = 2**33-355

def hash_function_factory(a, b, p=p, m=2**32-1):
    def hash_function(x):
        return ((a * hash(x) + b) % p) % m
    return hash_function

def create_hash_functions(n):
    import random
    return [hash_function_factory(random.randint(1, p), random.randint(1, p)) for _ in range(n)]

def hash_buckets(signature, num_buckets):
    return hash(str(signature)) % num_buckets

# Example usage:
sentence1 = "The quick brown fox jumps over the lazy dog"
sentence2 = "The quick white cat jumps over the lazy fox"

shingles1 = create_shingles(sentence1)
shingles2 = create_shingles(sentence2)

hash_funcs = create_hash_functions(100)

signature1 = minhash_signature(shingles1, hash_funcs)
signature2 = minhash_signature(shingles2, hash_funcs)

num_buckets = 100
buckets = [set() for _ in range(num_buckets)]

# Hash the signatures into buckets
bucket_index1 = hash_buckets(signature1, num_buckets)
bucket_index2 = hash_buckets(signature2, num_buckets)

# Add the sentences to their respective buckets
buckets[bucket_index1].add(sentence1)
buckets[bucket_index2].add(sentence2)

similarity = jaccard_similarity(set(signature1), set(signature2))
print("Jaccard similarity", similarity)