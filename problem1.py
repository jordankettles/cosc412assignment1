from asyncio import constants
from glob import glob
import os
import sys

acceptable_bigrams = ['ng', 'wh']
vowels = ['a', 'e', 'i', 'o', 'u']
constants = ['h', 'k', 'm', 'p', 'r', 'w', 'n']
for vowel in vowels:
    for const in constants:
        acceptable_bigrams.append(const + vowel)

print(len(acceptable_bigrams))

def count_chars(files):
    for file_path in files:
        char_list = []
        if file_path.endswith("README.txt"):
            continue
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip().lower()
                for char in line:
                    if char.isalpha() and char not in char_list:
                        print(char)
                        char_list.append(char)
                        # if char not in "thkmprwhngaeiou":
                        #     print(file_path)

        print("Unique alphabetic chars of {} is {}.".format(file_path, len(char_list)))

def calc_distribution(files, is_key=False):
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
                            if not acceptable_bigram(bi_gram):
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

def calc_trigram_distribution(files, is_key=False):
    tri_gram_dict = {}
    for file_path in files:
        if file_path.endswith("README.txt"):
            continue
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip().lower()
                tri_grams = [line[i:i+3] for i in range(0, len(line))]
                for tri_gram in tri_grams:
                    if tri_gram.isalpha() and len(tri_gram) == 3:
                        if is_key:
                            if not acceptable_characters(tri_gram):
                                continue
                        if tri_gram not in tri_gram_dict:
                            tri_gram_dict[tri_gram] = 1
                        else:
                            tri_gram_dict[tri_gram] += 1
    total_tri_grams = sum(tri_gram_dict.values())
    for tri_gram in tri_gram_dict:
        tri_gram_dict[tri_gram] /= total_tri_grams
    return tri_gram_dict

def get_similarities(encoded_dist, corpus_dist_value):
    similarities = [(encoded_gram, abs(encoded_dist[encoded_gram] - corpus_dist_value)) for encoded_gram in encoded_dist]
    similarities.sort(key=lambda x: x[1])
    return similarities

def second_attempt():
    # letter_dist = {
    #     'a': corpus_dist['a'],
    #     'e': corpus_dist['e'],
    #     'i': corpus_dist['i'],
    #     'o': corpus_dist['o'],
    #     'u': corpus_dist['u'],
    #     't': corpus_dist['t'],
    #     'h': corpus_dist['h'],
    #     'k': corpus_dist['k'],
    #     'm': corpus_dist['m'],
    #     'p': corpus_dist['p'],
    #     'r': corpus_dist['r'],
    #     'w': corpus_dist['w'],
    #     'n': corpus_dist['n'],
    #     'ng': corpus_bi_gram_dist['ng'],
    #     'wh': corpus_bi_gram_dist['wh'],
    # }
    # Try find ng and wh.
    my_two_letter_morphemes = ['ng', 'wh']

def first_attempt(corpus_dist, cipher_dist, string):
    print(string)
    unigram_keys = dict()

    # assert len(corpus_dist) == len(cipher_dist)
    
    for unigram in corpus_dist:
        similarities = get_similarities(cipher_dist, corpus_dist[unigram])
        unigram_keys[similarities[0][0]] = unigram
        # print(unigram)
        # print(similarities)
    # for unigram in cipher_dist:
    #     similarities = get_similarities(corpus_dist, cipher_dist[unigram])
    #     # print(unigram)
    #     # print(similarities)
    #     # print(similarities[0][0])
    #     unigram_keys[unigram] = similarities[0][0]
    #     corpus_dist.pop(similarities[0][0])
    # print(unigram_keys.keys())
    decoded_text = ""
    for char in string:
        if char in unigram_keys.keys():
            if char.isupper():
                decoded_text += unigram_keys[char].upper()
            else:
                decoded_text += unigram_keys[char]
        else:
            decoded_text += char
    print(decoded_text)

def main():
    ciphers_path_list = ["./c1.txt", "./c2.txt"]
    corpus_path_list = glob(os.path.normpath("BCP_subset_Te_Reo_Maori") + "/*")
    # count_chars(ciphers_path_list)
    corpus_dist = calc_distribution(corpus_path_list, is_key=True)
    corpus_bi_gram_dist = calc_bigram_distribution(corpus_path_list, is_key=True)
    corpus_tri_gram_dist = calc_trigram_distribution(corpus_path_list, is_key=True)

    for cipher in ciphers_path_list:
        # Get text from cipher file
        with open(cipher, encoding='utf-8') as f:
            cipher_text = f.read().strip()
            cipher_dist = calc_distribution([cipher])
            cipher_bi_gram_dist = calc_bigram_distribution([cipher])
            cipher_tri_gram_dist = calc_trigram_distribution([cipher])
            
            first_attempt(corpus_dist, cipher_dist, cipher_text)
            print()
            second_attempt()



if __name__ == "__main__":
    main()
