import pickle
from nltk.stem import PorterStemmer


index = {}
with open('dictionary.pkl', 'rb') as f:
    index = pickle.load(f)

stemmer = PorterStemmer()
print(stemmer.stem("informatics"))
print(list(index.keys())[10:30])

query = input("Search: ")
words = query.split()
for word in words:
    word = word.strip()
    word = stemmer.stem(word)
    if len(word) <= 2:
        continue


