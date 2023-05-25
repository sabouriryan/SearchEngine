import pickle
from nltk.stem import PorterStemmer
import time


def tokenize(query):
    words = query.split()
    stemmer = PorterStemmer()
    for word in words:
        word = word.strip()
        word = stemmer.stem(word)
    return words

def search(query, inverted_index):
    # Tokenize the query
    tokens = tokenize(query)

    # Initialize a dictionary to store relevance scores
    relevance_scores = {}

    # Retrieve relevant tuples and calculate relevance scores
    for token in tokens:
        if token in inverted_index:
            tuples = inverted_index[token]
            for tuple in tuples:
                url = tuple[1]
                tf_idf = tuple[2]
                # Assign relevance score based on tf-idf value (you can adjust the weight factor)
                relevance_scores[url] = relevance_scores.get(url, 0) + tf_idf * 1.0 # Adjust weight factor as needed

    # Rank the tuples based on relevance scores
    ranked_tuples = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)

    # Return the top-k results
    top_results = ranked_tuples[:5]
    return top_results


def main():
    index = {}
    with open('dictionary.pkl', 'rb') as f:
        index = pickle.load(f)

    while True:
        query = input("Search: ")
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


