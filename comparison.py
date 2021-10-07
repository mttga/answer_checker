import re
from typing import List

import nltk
from nltk import edit_distance
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from word2number import w2n

nltk.download('stopwords')
stemmer = SnowballStemmer("english")
SW = set(stopwords.words('english'))

class Comparison:

    """
    The Comparison class facilitates the comparison 
    between the right answers and the user answer.

    It must be created with Comparison(right_answers, user_answer)
    and its main method is get_result, that returns Right or
    Wrong depending on the
    """
    
    def __init__(self, right_answers: str, user_answer: str):
        
        # preprocess right and user answers
        self.r_answers = self._preprocess(right_answers)
        self.u_answer  = self._preprocess(user_answer)
        
    def _preprocess(self, s: str) -> str:
        # tokenize and stem (for plural-singular) and remove stopwords
        stems = [stemmer.stem(word) for word in word_tokenize(s) if word not in SW]
        # transform word-numbers to digit and return a string
        s = ' '.join(self._numberfy(s) for s in stems)
        return s
    
    def _numberfy(self, s: str) -> str:
        """
        Transform 'two' to '2', 'three' to '3', etc.
        """
        try:
            return str(w2n.word_to_num(s))
        except:
            return s
    
    def _check_numbers(self, right_answer, user_answer) -> bool:
        """
        Check if the numbers on two strings are the same
        """
        right_numbers = re.findall(r'\d', right_answer)
        user_numbers  = re.findall(r'\d', user_answer)
        return right_numbers == user_numbers
        
    def get_result(self) -> str:
        """
        Returns Right or Wrong depending on the comparison done
        """
        if edit_distance(self.r_answers, self.u_answer) <= 1:
            if self._check_numbers(self.r_answers, self.u_answer):
                return 'Right'           
        return 'Wrong'