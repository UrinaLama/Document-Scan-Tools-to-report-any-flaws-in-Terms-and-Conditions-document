import pickle
from script.clean_data import text_preprocessing

def get_classified_lines(lines):
    clean_lines = []
    for i in lines:
        clean_line = text_preprocessing(i)
        clean_lines.append(clean_line)
    vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))
    vectorized_texts = vectorizer.transform(clean_lines)
    LR =  pickle.load(open("model/logistic_regression.pkl", "rb"))
    predictions = LR.predict(vectorized_texts) 
    data = {"positive":[], "negative":[]}
    for i,line in enumerate(lines):
        if predictions[i] == 0:
            data["positive"].append(line)
        else:
            data["negative"].append(line)
    return data