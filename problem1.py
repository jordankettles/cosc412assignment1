from asyncio import constants
from glob import glob
import os

acceptable_bigrams = ['ng', 'wh']
vowels = ['a', 'e', 'i', 'o', 'u']
constants = ['h', 'k', 'm', 'p', 'r', 'w', 'n', 't']
for vowel in vowels:
    for const in constants:
        acceptable_bigrams.append(const + vowel)
    for const in constants:
        if const == 'g':
            continue
        acceptable_bigrams.append(vowel + const)
    for vowel2 in vowels:
        if vowel + vowel2 not in acceptable_bigrams:
            acceptable_bigrams.append(vowel + vowel2)

def calc_distribution_with_files(files, is_key=False):
    char_dict = {}
    for file_path in files:
        if file_path.endswith("README.txt"):
            continue
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip().lower()
                for char in line:
                    if char.isalpha():
                        if is_key:
                            if char not in "thkmprwngaeiou":
                                continue
                        if char not in char_dict:
                            char_dict[char] = 1
                        else:
                            char_dict[char] += 1
    total_chars = sum(char_dict.values())
    for char in char_dict:
        char_dict[char] /= total_chars
    return char_dict

def calc_distribution(a_list):
    char_dict = {}
    for guess in a_list:
        char = guess[0]
        if char not in char_dict:
            char_dict[char] = 1
        else:
            char_dict[char] += 1
    total_chars = sum(char_dict.values())
    for char in char_dict:
        char_dict[char] /= total_chars
    return char_dict

def calc_bigram_distribution(files, is_key=False):
    bi_gram_dict = {}
    for file_path in files:
        if file_path.endswith("README.txt"):
            continue
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip().lower()
                bi_grams = [line[i:i+2] for i in range(0, len(line))]
                for bi_gram in bi_grams:
                    if bi_gram.isalpha() and len(bi_gram) == 2:
                        if is_key:
                            if not acceptable_characters(bi_gram):
                                continue
                        if bi_gram not in bi_gram_dict:
                            bi_gram_dict[bi_gram] = 1
                        else:
                            bi_gram_dict[bi_gram] += 1
    total_bi_grams = sum(bi_gram_dict.values())
    for bi_gram in bi_gram_dict:
        bi_gram_dict[bi_gram] /= total_bi_grams
    return bi_gram_dict

def acceptable_characters(gram):
    for char in gram:
        if char not in "thkmprwngaeiou":
            return False
    return True

def acceptable_bigram(gram):
    global acceptable_bigrams
    return gram in acceptable_bigrams

def get_similarities(encoded_dist, corpus_dist_value):
    similarities = [(encoded_gram, abs(encoded_dist[encoded_gram] - corpus_dist_value)) for encoded_gram in encoded_dist]
    return similarities

def find_ng(encoded_dist, encoded_bigram_dist):
    for possible_g in encoded_dist:
        possible_ngs = {i for i in encoded_bigram_dist if i[1] == possible_g[0]}
        if len(possible_ngs) == 1:
            print("ng could be...",possible_ngs)


def print_answer(cipher_text, solution):
    decoded_text = ""
    for char in cipher_text:
        if char.lower() in solution.keys():
            if char.isupper():
                decoded_text += solution[char.lower()].upper()
            else:
                decoded_text += solution[char.lower()]
        else:
            decoded_text += char
    print(decoded_text)   

def top3_freqs(corpus_unigram_dist, cipher_unigram_dist):
    corpus_dist = corpus_unigram_dist.copy()
    top_corpus_freqs = sorted(corpus_dist.items(), key=lambda x: x[1], reverse=True)
    top_cipher_freqs = sorted(cipher_unigram_dist.items(), key=lambda x: x[1], reverse=True)
    for i in range(3):
        print(top_corpus_freqs[i], top_cipher_freqs[i])


def second_attempt(corpus_bi_gram_dist, cipher_bi_gram_dist, cipher_text):
    
    letter_keys = {
        'a': None,
        'e': None,
        'i': None,
        'o': None,
        'u': None,
        't': None,
        'h': None,
        'k': None,
        'm': None,
        'p': None,
        'r': None,
        'w': None,
        'n': None,
        'g': None,
    }
    phi = 0.5
    added_key = False
    
    while None in letter_keys.values() and phi > 0.1:
        corpus_dist = {i: corpus_bi_gram_dist[i] for i in corpus_bi_gram_dist if letter_keys[i[0]] is None or letter_keys[i[1]] is None}
        cipher_dist = {i: cipher_bi_gram_dist[i] for i in cipher_bi_gram_dist if i[0] not in letter_keys.values() \
            or i[1] not in letter_keys.values()}
        for cd in cipher_dist:
            # Update the dist value based on the length of cipher_dist
            cipher_dist[cd] = (cipher_dist[cd] * len(cipher_bi_gram_dist)) /  len(cipher_dist)
        for cd in corpus_dist:
            corpus_dist[cd] = (corpus_dist[cd] * len(corpus_bi_gram_dist)) /  len(corpus_dist)
        added_key = False
        
        bigram_keys = dict()
        for bigram in sorted(cipher_dist, key=lambda x: cipher_dist[x], reverse=True):
                if len(corpus_dist) == 0:
                    break
                similarities = get_similarities(corpus_dist, cipher_dist[bigram])
                best_match = min(similarities, key=lambda x: x[1])[0]
                bigram_keys[bigram] = best_match
                corpus_dist.pop(best_match)

        # if majority? of bigrams containing a unigram agree, then set the letter key, otherwise try again.
        for letter in letter_keys:
            if letter_keys[letter] != None:
                continue
            curr_guesses = []
            bigram_info_list = [bigram_info for bigram_info in bigram_keys.items() if letter in bigram_info[1]]
            for c, m in bigram_info_list:
                letter_loc = m.index(letter)
                curr_guesses.append(c[letter_loc])
            best_match = max(calc_distribution(curr_guesses).items(), key=lambda x: x[1])
            if best_match[1] > phi and best_match[0] not in letter_keys.values():
                letter_keys[letter] = best_match[0]
                added_key = True
        if added_key == False:
            phi -= 0.01
    if None in letter_keys.values():
        print("Failed to find all keys.") 
    letter_keys2 = {v: k for k, v in letter_keys.items() if v is not None}
    decoded_text = ""
    for char in cipher_text:
        if char.lower() in letter_keys2:
            if char.isupper():
                decoded_text += letter_keys2[char.lower()].upper()
            else:
                decoded_text += letter_keys2[char.lower()]
        else:
            decoded_text += char
    print("second attempt:", decoded_text)

# First attempt and third atttempt.
def first_attempt(corpus_dist, cipher_dist, cipher_text, unigram_keys):
    if unigram_keys is None:
        attempt = "First Attempt:"
    else:
        attempt = "Third Attempt:"
    corpus_dist = corpus_dist.copy()
    print(cipher_text)
    print()

    # This if else statement was added during my third attempt. It's not needed for the first attempt.
    if unigram_keys is None:
        unigram_keys = dict()
    else:
        for k, v in unigram_keys.items():
            if k is not None:
                corpus_dist.pop(v)

    for unigram in cipher_dist:
        if len(corpus_dist) == 0:
            break
        similarities = get_similarities(corpus_dist, cipher_dist[unigram])
        best_match = min(similarities, key=lambda x: x[1])[0]
        if unigram in unigram_keys.keys():
            continue
        unigram_keys[unigram] = best_match
        corpus_dist.pop(best_match)
    print(attempt)
    print_answer(cipher_text, unigram_keys)

if __name__ == "__main__":
    solutions = list()
    solutions.append({
        'i':'a', #
        'x': 'e', #
        'a': 'i', #
        't': 'o', #
        'h': 'u', #
        'g': 't', #
        'j': 'h', #
        'z': 'k', #
        'n': 'm', #
        'm': 'p', #
        'k': 'r', #
        'o': 'w', #
        's': 'n', #
        'p': 'g', #
    })

    solutions.append(
        {
        'u':'a',
        'k': 'e',
        'f': 'i',
        'i': 'o',
        's': 'u',
        'y': 't',
        'b': 'h',
        'q': 'k',
        'w': 'm',
        'd': 'p',
        'r': 'r',
        'v': 'w',
        'j': 'n',
        'x': 'g',
    })

    ciphers_path_list = ["./c1.txt", "./c2.txt"]
    corpus_path_list = glob(os.path.normpath("BCP_subset_Te_Reo_Maori") + "/*")
    corpus_dist = calc_distribution_with_files(corpus_path_list, is_key=True)
    corpus_bi_gram_dist = calc_bigram_distribution(corpus_path_list, is_key=True)
    forbidden_bigrams = list(set(corpus_bi_gram_dist.keys()) - set(acceptable_bigrams))
    for fb in forbidden_bigrams:
        corpus_bi_gram_dist.pop(fb)
    cipher_count = 0
    for cipher in ciphers_path_list:
        # Get text from cipher file
        with open(cipher, encoding='utf-8') as f:
            cipher_text = f.read().strip()
            cipher_dist = calc_distribution_with_files([cipher])
            cipher_bi_gram_dist = calc_bigram_distribution([cipher])
            
            assert len(corpus_dist) == len(cipher_dist)
            first_attempt(corpus_dist, cipher_dist, cipher_text, None)
            print()

            second_attempt(corpus_dist, cipher_dist, cipher_text)
            print()

            print("corpus_bi_gram_dist: {}".format(len(corpus_bi_gram_dist)))
            print("cipher_bi_gram_dist: {}".format(len(cipher_bi_gram_dist)))
            top3_freqs(corpus_dist, cipher_dist)
            find_ng(cipher_dist, cipher_bi_gram_dist)
            first_attempt(corpus_dist, cipher_dist, cipher_text, solutions[cipher_count])
            cipher_count += 1
