import numpy as np

import pandas as pd

# https://www.geeksforgeeks.org/how-to-calculate-cosine-similarity-in-python/
# https://www.w3schools.com/python/pandas/pandas_dataframes.asp

class Similarity:
        
    def cosine_similarity(self, word1, word2, model):
        if word1 == word2:
            cosine_similarity = 1
            return cosine_similarity
        elif model == "word2vec":
            file = "word2vec.txt"
        else:
            file = "speech2vec.txt"
        dictionary = word_vec_dict(file)
        vec1 = dictionary[word1]
        vec2 = dictionary[word2]
        dot_product = np.dot(vec1, vec2)
        magnitude1 = np.linalg.norm(vec1)
        magnitude2 = np.linalg.norm(vec2)
        magnitude_product = magnitude1 * magnitude2
        cosine_similarity = dot_product / magnitude_product
        return cosine_similarity
        
    def visualize_items(self, ID):
        """Visualizes all words produced by a participant under word2vec and 
        speech2vec"""
        dictionary = id_word_dict()
        words_by_ID = dictionary[ID]
        return words_by_ID
        #Unable to do plot t-SNE
    
    def pairwise_similarity(data):
        """Computes pairwise similarity between each consecutive word that the participant produces"""
        # Task 1: Do so for participant 1.
        dictionary = id_word_dict()
        with open ('word2vec.txt', 'r') as content:
            all_data = content.read()
            print(all_data)
        for ID in id_word_dict():
            words_by_ID = dictionary[ID]
            similarities = [2]
            word_pairs = [(words_by_ID[0])]
            for num in range(len(dictionary[ID])-1):
                if words_by_ID[num] in all_data and words_by_ID[num+1] in all_data:
                    x = Similarity()
                    sim = x.cosine_similarity(words_by_ID[num], words_by_ID[num+1], "word2vec")
                    similarities.append(sim)
                    pair = (words_by_ID[num], words_by_ID[num+1])
                    word_pairs.append(pair)
            data = {"pairs": word_pairs, "Similarity": similarities}
            print(pd.DataFrame(data))
    
def embedding_to_vec(file):
    """Convert each line in a word embedding file into a vector"""
    with open(file, "r") as content:
        content = content.readlines()
        vector_list = []
        for word in content[1:]:
            word = word.strip().split()[1:]
            #Convert each entry into float
            embedding = []
            for entry in word:
                entry = float(entry)
                embedding.append(entry)
            vector = np.array(embedding)
            vector_list.append(vector)
        #https://www.geeksforgeeks.org/how-to-create-a-vector-in-python-using-numpy/
        return vector_list

def word_vec_dict(file):
    """Create a dictionary that maps a word to its embedding represented by 
    vectors"""
    word_to_vect_dict = dict()
    vector_list = embedding_to_vec(file)
    # extract all the embedded words in the document
    with open(file, "r") as content:
        content = content.readlines()
        word_list = []
        for line in content[1:]:
            word = line.split()[0]
            word_list.append(word)
    for num in range(len(word_list)-1):
        word_to_vect_dict[word_list[num]] = vector_list[num]
    return word_to_vect_dict



def id_word_dict():
    """Creates a dictionary that maps IDs with all words that the person of 
    this ID produces"""
    with open("data-cochlear.txt", "r") as content:
        content = content.readlines()
    id_word_list = []
    dictionary = dict()
    for line in content:
        line = line.strip().split()
        id_word_list.append(line)
    all_ids = []
    for id_word in id_word_list:
        all_ids.append(id_word[0])
    all_ids = set(all_ids)
    for ID in all_ids:
        words_list = []
        for line in id_word_list:
            if line[0] == ID:
                words_list.append(line[1])
        dictionary[ID] = words_list
    return dictionary

