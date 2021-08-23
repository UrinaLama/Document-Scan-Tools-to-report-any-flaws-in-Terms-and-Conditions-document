import string
import nltk
import spacy
import re 

nlp = spacy.load("en_core_web_sm")


def remove_nonwords(text):
    no_punctuation_text = ''.join([i for i in str(text) if i not in string.punctuation])
    return re.sub("[^A-Za-z ]\w+[^A-Za-z]*", ' ', no_punctuation_text).lower()

# Lemmatization and Removing stop words and non words
def text_preprocessing(text):
    text = remove_nonwords(text)
    tokenized_text = [token.lemma_ for token in nlp(text)]
    no_stopwords_list = [i.lower() for i in tokenized_text if i not in nlp.Defaults.stop_words]
    lemma_text = ' '.join(no_stopwords_list)
    return lemma_text