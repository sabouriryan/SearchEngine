import json
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
from Posting import Posting
import os
import sys
import pickle

'''
we need number of documents, number of unique tokens, and size on disk
'''

inverted_index = {}
documents = 0
token_set = set()

# reads json obj into dictionary
def read_json(json_obj):
    global inverted_index
    global documents
    global token_set
    d = open(json_obj, 'r', encoding = 'utf-8-sig')
    json_dict = json.load(d)
    # parses, we can get only the text with get_text()
    soup = BeautifulSoup(json_dict["content"], 'html.parser')

    # find all the "strong" words, i.e. words in bold or in h1, h2, h3 tags
    # but how do we make sure these words arent counted again
    # think about for next MS, only need term frequency rn
    #tags = soup.find_all(['h1', 'h2', 'h3', 'strong'])
    text = soup.get_text()

    # we use regular expressions to extract all alphanumeric sequences
    tokens = re.findall(r'\w+', text)


    # once extracted, we use porter stemming to shrink the data set
    stemmed_tokens = []
    stemmer = PorterStemmer()
    for token in tokens:
        token_set.add(token)
        stemmed_tokens.append(stemmer.stem(token))

    #now, we can go through the set and count the frequency of each word
    frequencies = {}
    for token in stemmed_tokens:
        if token not in frequencies:
            frequencies[token] = 1
        else:
            frequencies[token] += 1
    

    '''
    This is how we are dealing with strong words. Read through all words 
    ignoring the tags first, then go back and read all tagd and add 0.5 to their
    frequency
    '''
    tags = soup.find_all(['h1', 'h2', 'h3', 'strong'])
    for tag in tags:
        token = tag.get_text()
        token = stemmer.stem(token)
        frequencies[token] += 0.5

    # now that we have our frequencies, we can create our postings
    # we will go through the dict, create postings for each word, and update our
    # inverted index
    #print(frequencies)
    for key, val in frequencies.items():
        post = Posting(key, json_dict["url"], val)
        post_tuple = post.convert_to_tuple()
        if key not in inverted_index:
            inverted_index[key] = [post_tuple]
        else:
            inverted_index[key].append(post_tuple)
    
    d.close()

    # thats all we need per json file


# uses os library to create a list of a file objects that we can iterate
def read_folder(folder_path):
    folder = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            filepath = os.path.join(folder_path, filename)
        else:
            continue
        if os.path.isfile(filepath):
            folder.append(filepath)
    return folder

# we need to get a list of folders from this function
def list_directories(dir_path):
    # Get a list of all files and directories in the given path
    files_and_dirs = os.listdir(dir_path)

    # Create an empty list to hold the directories
    directories = []

    # Loop over all files and directories
    for item in files_and_dirs:
        # Create a full path to the item
        full_path = os.path.join(dir_path, item)

        # Check if the item is a directory
        if os.path.isdir(full_path):
            # If it is, append it to the list of directories
            directories.append(full_path)

    # Return the list of directories
    return directories


def main():
    global documents
    global token_set
    global inverted_index
    folders = list_directories('DEV')
    for folder in folders:
        print("going folder by folder")
        cur_folder = read_folder(folder)
        for file in cur_folder:
            if not documents % 100:
                print("up by 100")
                print(len(token_set))
            documents += 1
        #print("read through")
            read_json(file)
    print(len(token_set), documents, sys.getsizeof(inverted_index))
    with open('dictionary.pkl', 'wb') as f:
        pickle.dump(inverted_index, f)

if __name__ == '__main__':
    main()


'''
We need to extract all the tokens from the json, store in dict with frequencies
and then we can make our postings and store everything in the inverted index dict

We also need to find a way to recognize when text is bold or in h1-h3 tags.
Marking them as more important shouldn't be too difficult, we can just count
each occurrence as double what we would otherwise

Therefore, we can just find all the words with those tags, count each occurrence 
normally using a dictionary, and then go through the entire page and count them again.
This way all the important words would've been counted twice
'''