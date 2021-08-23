import string
import nltk
import re
import spacy

from bs4 import BeautifulSoup
import requests

import wordninja
from nltk.tokenize import word_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

from script.clean_data import text_preprocessing

good_privacy = []
with open("./data/good_privacy.txt", "r", encoding="utf8") as f:
    for line in f:
        text = text_preprocessing(line.rstrip().lower())
        good_privacy.append(text)

bad_privacy = []
with open("./data/bad_privacy.txt", "r",  encoding="utf8") as f:
    for line in f:
        text = text_preprocessing(line.rstrip().lower())
        bad_privacy.append(text)

all_privacy = good_privacy + bad_privacy

nlp = spacy.load("en_core_web_sm")

def remove_punctuation(text):
    no_punctuation_text = ''.join([i for i in str(text) if i not in string.punctuation])
    return no_punctuation_text.lower()

def remove_nonwords(str_):
    return re.sub("[^A-Za-z ]\w+[^A-Za-z]*", ' ', str_)

def text_preprocessing(text):
    text = remove_punctuation(text)
    text = remove_nonwords(text)
    tokenized_text = [token.lemma_ for token in nlp(text)]
    no_stopwords_list = [i.lower() for i in tokenized_text if i not in nlp.Defaults.stop_words]
    lemma_text = ' '.join(no_stopwords_list)
    return lemma_text

def get_raw_policies(a_tag, web_url):
    urls = []
    for i in a_tag:
        for term in ["privacy", "terms","conditions","policy", "legal"]:
            if term in i.text.lower():
                urls.append(i["href"])

    raw_policies = []

    for url in urls: 
        if url[0] == "/":
            url = web_url + url
        try:
            source = requests.get(url).text
            soup = BeautifulSoup(source, 'lxml')
        except:
            continue
        policies=soup.find('html')
        
        raw_policies.append(policies.text)

    return raw_policies

def clean_raw_policies(raw_policies):
    clean_words = []
    list_of_words = word_tokenize(". ".join(raw_policies))
    for word in list_of_words:
        if len(word) > 10:
            words = wordninja.split(word)
            clean_words.extend(words)
        clean_words.append(word)
    clean_text = " ".join(clean_words)
    remove_unwanted_punctuations_words = []
    for i,word in enumerate(word_tokenize(clean_text)):
        if "." in word:
            if len(word.strip()) > 1:
                word = remove_punctuation(word)
            if word == ".":
                if word_tokenize(clean_text)[i+1].strip()[0] == word_tokenize(clean_text)[i+1].lower()[0]:
                    word = " "
        remove_unwanted_punctuations_words.append(word.strip())
    clean_text = " ".join(remove_unwanted_punctuations_words)
    punkt_param = PunktParameters()
    tokenizer = PunktSentenceTokenizer(punkt_param)
    clean_policy = tokenizer.tokenize(clean_text)
    return clean_policy

def sim_sentences(clean_policy):
    sim_sentences = []
    for X_raw in clean_policy:
        X = text_preprocessing(X_raw)
        high_sim = 0
        sim_sentence = ""
        for Y in all_privacy:
            
            l1 =[];l2 =[]

            X_set = {w for w in word_tokenize(X)} 
            Y_set = {w for w in word_tokenize(Y)}

            # form a set containing keywords of both strings 
            rvector = X_set.union(Y_set) 
            for w in rvector:
                if w in X_set: l1.append(1) # create a vector
                else: l1.append(0)
                if w in Y_set: l2.append(1)
                else: l2.append(0)
            c = 0

            # cosine formula 
            for i in range(len(rvector)):
                    c+= l1[i]*l2[i]
            if float((sum(l1)*sum(l2))**0.5) != 0:
                cosine = c / float((sum(l1)*sum(l2))**0.5)
            else:
                cosine = 0
            
            if cosine > high_sim:
                high_sim = cosine
                sim_sentence = X_raw
                
        if high_sim > 0.35:
            sim_sentences.append(sim_sentence.strip())
    final_sentences = []
    for sim_sentence in sim_sentences:
        if "?" not in sim_sentence:
            final_sentences.append(sim_sentence)
    return final_sentences

def get_important_lines(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    a_tag = soup.find_all("a")
    raw_policies = get_raw_policies(a_tag, url)
    clean_policies = clean_raw_policies(raw_policies)
    final_policies = sim_sentences(clean_policies)
    return final_policies



