import re
import json
import pandas as pd
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
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
SW = set(stopwords.words('english')) #english stopwords
EW = set(words.words()) # english word
with open('am2br.json', 'r') as file: #american to britush dictionary
    am2br = json.load(file)
case_memory = pd.read_csv('case_memory.csv')


class Comparison:

    """
    The Comparison class facilitates the comparison 
    between the right answer and the user answer.

    It must be created with Comparison(right_answer, user_answer)
    and its main method is get_result, that returns Right or
    Wrong depending on the
    """
    
    def __init__(self, right_answer: str, user_answer: str):

        #check in memory for equal cases
        memory_result = self._check_memory(right_answer, user_answer)
        if memory_result:
            self.result = memory_result
        else: 
            # preprocess right and user answer
            self.r_answer = self._preprocess_string(right_answer)
            self.u_answer = self._preprocess_string(user_answer)
            self.r_lemmas = set([lemmatizer.lemmatize(w) for w in word_tokenize(self.r_answer) if lemmatizer.lemmatize(w) in EW])
            self.u_lemmas = set([lemmatizer.lemmatize(w) for w in word_tokenize(self.u_answer) if lemmatizer.lemmatize(w) in EW])
            self.result   = self._compare()
        
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
            w = num2words(w) # Transform '2' to 'two', '41' to 'forty-one', etc.
        except:
            pass
        return w.lower() 
    
    def _check_lemmas(self, thresehold=0.8) -> bool:
        """
        Check if the lemmas of the user answer present in the right answer
        are above a certain threshold
        """
        if len(self.r_lemmas)!=len(self.u_lemmas) or len(self.r_lemmas)+len(self.u_lemmas)==0:
            return True
        jaccard_similarity = 1-jaccard_distance(self.r_lemmas, self.u_lemmas)
        if jaccard_similarity > thresehold:
            return True
        else:
            return False

    def _check_memory(self, r_a:str, u_a:str):
        result = case_memory.loc[((case_memory['right_answer'] == r_a) & (case_memory['user_answer'] == u_a)) | 
                            ((case_memory['right_answer'] == u_a) & (case_memory['user_answer'] == r_a))]['output']  
        if result.any():
            return result.mode()[0] # return the most frequent item if there is a multiple match
        else:
            return None # return None if there is no match
        
    def _compare(self) -> str:
        """
        Returns Right or Wrong depending on the comparison done
        """
        # check again in memory after the preprocessing
        memory_result = self._check_memory(self.r_answer, self.u_answer)
        if memory_result:
            return memory_result
        else:
            if edit_distance(self.r_answer, self.u_answer) <= 3:
                if self._check_lemmas():
                    return 'Right'           
            return 'Wrong'

    def get_result(self) -> str:
        return self.result