import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class Preprocessor:

    def __init__(self, text):
        self.text = text

    def splitWords(self, data):
        if type(data) == str:
            words = data.split()
        else:
            words = np.array_str(data).split()
        return words

    def toLowerCase(self, data):
        return np.char.lower(data)

    def removeStopWords(self, data):
        words = self.splitWords(data)
        stop_words = set(stopwords.words('english'))
        new_text = ""
        for word in words:
            if word not in stop_words:
                new_text = new_text + " " + word
        return new_text

    def removeSymbols(self, data):
        symbols = ",!\"#$%&()*+-/:;<=>?@[\]^_`{|}~\n"
        for i in symbols:
            data = np.char.replace(data, i, ' ')
        return np.char.replace(data, "'", "")

    def removeSingleCharacters(self, data):
        words = self.splitWords(data)
        new_text = ""
        for w in words:
            if len(w) > 1:
                new_text = new_text + " " + w
        return new_text

    def lemmatize(self, data):
        words = self.splitWords(data)
        lemmatizer = WordNetLemmatizer()
        new_text = ""
        for word in words:
            new_text = new_text + " " + lemmatizer.lemmatize(word)
        return new_text

    def removeNonEnglish(self, data):
        english_vocab = set(w.lower() for w in nltk.corpus.words.words())
        words = self.splitWords(data)
        new_text = ""
        for word in words:
            if word in english_vocab:
                new_text = new_text + " " + word
        return new_text

    def preprocessData(self):
        data = self.toLowerCase(self.text)
        data = self.removeSymbols(data)
        data = self.removeSingleCharacters(data)
        data = self.removeStopWords(data)
        data = self.removeNonEnglish(data)
        data = self.lemmatize(data)
        return data
