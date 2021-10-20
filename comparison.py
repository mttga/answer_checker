import re
import json
from typing import List

import nltk
from nltk import edit_distance, jaccard_distance
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from num2words import num2words
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words

# Ensure all the resources are available
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('words')
lemmatizer = WordNetLemmatizer()
SW = set(stopwords.words('english')) #english stopwords
EW = set(words.words()) # english word
with open('am2br.json', 'r') as file: #american to britush dictionary
    am2br = json.load(file)


class Comparison:

    """
    The Comparison class facilitates the comparison 
    between the right answer and the user answer.

    It must be created with Comparison(right_answer, user_answer)
    and its main method is get_result, that returns Right or
    Wrong depending on the
    """
    
    def __init__(self, right_answer: str, user_answer: str):
        
        # preprocess right and user answer
        self.r_answer = self._preprocess_string(right_answer)
        self.u_answer  = self._preprocess_string(user_answer)
        self.r_lemmas = set([lemmatizer.lemmatize(w) for w in word_tokenize(self.r_answer) if lemmatizer.lemmatize(w) in EW])
        self.u_lemmas = set([lemmatizer.lemmatize(w) for w in word_tokenize(self.u_answer) if lemmatizer.lemmatize(w) in EW])
        
    def _preprocess_string(self, s: str) -> str:
        """
        Preprocess an entire string
        """
        s = re.sub('[^A-Za-z0-9\-]+', ' ', s) # remove puntuaction
        words = [self._preprocess_word(word) for word in word_tokenize(s) if word not in SW]
        return ' '.join(w for w in words) # recunstruct string


    def _preprocess_word(self, w:str) -> str:
        """ 
        Preprocess a single word 
        """
        if w in am2br.keys(): 
            w = am2br[w] # convert american to british
        try: 
            w = num2words(w) # Transform '2' to 'tho', '41' to 'forty-one', etc.
        except:
            pass
        return w.lower() 
    
    def _check_lemmas(self, thresehold=0.5) -> bool:
        """
        Check if the lemmas of the user answer present in the right answer
        are above a certain threshold
        """
        if len(self.r_lemmas)!=len(self.u_lemmas) or len(self.r_lemmas)+len(self.u_lemmas)==0:
            return True
        jaccard_similarity = 1-jaccard_distance(self.r_lemmas, self.u_lemmas)
        if jaccard_similarity > 0.8:
            return True
        else:
            return False
        
    def get_result(self) -> str:
        """
        Returns Right or Wrong depending on the comparison done
        """
        print(self.r_answer, self.u_answer,edit_distance(self.r_answer, self.u_answer))
        if edit_distance(self.r_answer, self.u_answer) <= 3:
            print(self.r_lemmas, self.u_lemmas)
            if self._check_lemmas():
                return 'Right'           
        return 'Wrong'