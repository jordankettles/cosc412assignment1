from glob import glob
import os
import sys

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
                    if bi_gram.isalpha():
                        if is_key:
                            for char in bi_gram:
                                if char not in "thkmprwngaeiou":
                                    continue
                        if bi_gram not in bi_gram_dict:
                            bi_gram_dict[bi_gram] = 1
                        else:
                            bi_gram_dict[bi_gram] += 1
    total_bi_grams = sum(bi_gram_dict.values())
    for bi_gram in bi_gram_dict:
        bi_gram_dict[bi_gram] /= total_bi_grams
    return bi_gram_dict

def get_similarities(encoded_dist, corpus_dist_value):
    return [(encoded_gram, abs(encoded_dist[encoded_gram] - corpus_dist_value)) for encoded_gram in encoded_dist]

def decode(corpus_dist, corpus_bi_gram_dist, cipher_dist, cipher_bi_gram_dist, string):
    bi_gram_keys = dict()
    unigram_keys = dict()
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

    # Search 'depth'
    k = 2

    for morpheme in my_two_letter_morphemes:
        
        morpheme_similarities = get_similarities(cipher_bi_gram_dist, corpus_bi_gram_dist[morpheme])
        # if they match and we feel good continue?
        for morpheme_similarity in morpheme_similarities[:k]:
            for letter in morpheme_similarity[0]:
                encoded_morpheme_guess = ""
                letter_similarities = get_similarities(cipher_dist, corpus_dist[letter])
                for letter_similarity in letter_similarities[:k]:
                    if letter_similarity[0] == letter:
                        encoded_morpheme_guess += letter_similarity[0]
                        print("{} matches {}".format(letter_similarity[0], letter))
                        continue

                
        # Now find the closest unigrams for each morpheme.
        # Matches n, g that matches ng.

    for encoded_unigram in cipher_dist:
        similarity = abs(cipher_dist[encoded_unigram] - corpus_dist['n'])
        if similarity < top_similarity:
            top_similarity = similarity
            top_encoded_unigram = encoded_unigram
        

    # then find n, w
    # then find the vowels.
    # then find the consonants.
    # decoded_text = ""
    # for c in c_dist:
    #     min_similarity = sys.maxsize
    #     decoded_char = ""
    #     for k in k_dist_sorted:
    #         similarity = min([abs(c_dist[c] - k_dist[k])])
    #         if similarity < min_similarity:
    #             min_similarity = similarity
    #             decoded_char = k
    #     if c not in bi_gram_key:
    #         bi_gram_key[c] = decoded_char

    # key = dict()
    # for c in bi_gram_key:
    #     for character in c:
    #         if character not in key:
    #             key[character] = bi_gram_key[c][0]

    # for char in string:
    #     if char in key.keys():
    #         if char.isupper():
    #             decoded_text += key[char].upper()
    #         else:
    #             decoded_text += key[char]
    #     else:
    #         decoded_text += char
    # print(decoded_text)

def main():
    ciphers_path_list = ["./c1.txt", "./c2.txt"]
    corpus_path_list = glob(os.path.normpath("BCP_subset_Te_Reo_Maori") + "/*")
    # count_chars(ciphers_path_list)
    corpus_dist = calc_distribution(corpus_path_list, is_key=True)
    corpus_bi_gram_dist = calc_bigram_distribution(corpus_path_list, is_key=True)

    for cipher in ciphers_path_list:
        # Get text from cipher file
        with open(cipher, encoding='utf-8') as f:
            cipher_text = f.read().strip()
            cipher_dist = calc_distribution([cipher])
            cipher_bi_gram_dist = calc_bigram_distribution([cipher])
            decode(corpus_dist, corpus_bi_gram_dist, cipher_dist, cipher_bi_gram_dist, cipher_text)
            print()



if __name__ == "__main__":
    main()
