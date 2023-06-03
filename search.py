import pickle
from nltk.stem import PorterStemmer
import time
import os
import math


def tokenize(query):
    words = query.split()
    stemmed_words = []
    stemmer = PorterStemmer()
    for word in words:
        word = word.strip()
        stemmed_word = stemmer.stem(word)
        stemmed_words.append(stemmed_word)
    return stemmed_words

def search(query, inverted_index):
    # Tokenize the query
    tokens = tokenize(query)

    # Initialize a dictionary to store relevance scores
    # key is url, value is relevance score
    # we rank webpages based on relevance score
    # as of right now, the tf-idf score is the only thing factored in
    relevance_scores = {}

    # Retrieve relevant tuples and calculate relevance scores
    for token in tokens:
        if len(token) <= 2:
            continue
        if token in inverted_index:
            posts = inverted_index[token]
            for post in posts:
                url = post[1]
                tf = post[2]
                idf = math.log(55387 / len(posts))
                relevance_scores[url] = relevance_scores.get(url, 0) + (tf * idf) # Adjust weight factor as needed
                #relevance_scores[url] = relevance_scores.get(url, 0) + (tf)
    # Rank the tuples based on relevance scores
    ranked_pages = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)

    # Return the top 5 results
    results = ranked_pages[:5]
    return results

def merge_two_maps(map1, map2):
    for key, val in map2.items():
        if key not in map1:
            map1[key] = val
        else:
            # they exist in both, we need to add the list of tuples together
            map1[key] += map2[key]
    return map1

def merge_indexes():
    index_number = 1
    indexes = []
    file_path = "partial_index" + str(index_number) + ".pkl"
    while os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            partial_index = pickle.load(f)
            indexes.append(partial_index)
        index_number += 1
        file_path = "partial_index" + str(index_number) + ".pkl"
    # we have a list of dictionaries and we need to merge all of them
    full_index = {}
    for index in indexes:
        merge_two_maps(full_index, index)
    
    return full_index


def main():
    index = merge_indexes()
    while True:
        query = input("Search: ").lower()
        if query == "ss":
            break
        start = time.time()
        results = search(query, index)
        for result in results:
            print(result[0])
        end = time.time()
        print("Response time (in ms): ", (end - start) * 1000)

if __name__ == '__main__':
    main()


