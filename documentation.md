# Benchmark answer-checker documentation

## The Comparison class

The main class of the program is the Comparison class. It can be found in the comparison.py script. This class allows us to compare the similarity of a query string with a target string. The main attribute of this class is "result", which is set to 'Right' when the query and the target strings are considered similar enough, and 'Wrong' when they are too different. The query and the target are saved as "right_answer" and "user_answer" attributes. Following is a description of the class methods:

- init: the class requires two arguments to be initialized: right_answer (string) and user_answer (string). When the class is initialized, it checks in the memory database if there is a case that corresponds to the query. If yes, the "result" attribute takes the value of the case in the database. If not, the two strings are processed and compared with the other class methods.
- preprocess_string: method that removes the punctuation and stopwords ('a', 'the', 'this', etc.) from a string. Every word of the string is preprocessed using the "preprocess_word" method
- preprocess_word: preprocess a single word by transforming an american-spelled word into a british-spelled word ("esthete" to "aesthete"), transforming the digit numbers into string numbers ("2" to "two"), and lowering ("ASPIRIN" to "aspirin")
- check_lemmas: method that checks if the lemmas (the lemma of "brothers" is "brother") of the query and the target are more or less the same. Jaccard similarity is used: if it's above a default threshold of 0.8, True is returned; otherwise, False is returned. The comparison is performed only if the two strings have the same number of lemmas 
- check_memory: checks if the query and target are present in the memory dataset; if at least one case is found, the most frequent comparison result is returned. Otherwise, None is returned.
- compare: compares the preprocessed strings and returns "Right" or "Wrong". Since the preprocessed strings are compared, it is checked again in the memory if a corresponding case is present. If not, the edit distance between the strings is computed using the nltk library. If it's minor then 3, the lemmas are checked through the check_lemmas function. If this one returns true, then compare returns Right.
- get_result: returns the value of the "result" attribute (Right or Wrong)


## Dependencies

In order to use the Comparison class, it is important that some dependencies are loaded in memory. In particular, we have two sets that depend on nltk files (C:\nltk_data, or /usr/local/share/nltk_data): 

- the list of english stopwords (SW)
- the list of valid english words (EW)

An object of the nltk class WordNetLemmatizer, which is used to lemmatize the single words, also must be loaded in memory. Finally, two files must be present in the same location of the comparison.py to be loaded correctly:

- am2br.json: a dictionary with american-to-english most recurring words
- case_memory.csv: a data structure with the query-target pairs that must be memorized, formed by three columns (right_answer, user_answer, output)


All the necessary dependencies are loaded when the script is called (```from comparison import Comparison```). 

**Important**: loading in memory these dependencies requires some time; in particular, instantiating a WordNetLemmatizer object can be slow. For a fast execution it is important that all these dependencies are correctly loaded, i.e. that they are not loaded every time a comparison request is performed. 

## How to use Comparison

The best way to use the class is to generate a Comparison object with two strings and then call the get_result function. 

```Python
from comparison import Comparison

right_answer = 'aspirine'
user_answer  = 'ASPERENE'
c = Comparison(right_answer, user_answer)
print(c.get_result()) # prints 'Right'
```

It is suggested to do "import Comparison" at the start of the application, and to instantiate a new Comparison object for every new request. 

A comparison class can be also used by running the main.py script and passing the right_answer and user_answer as parameters. 

``` 
python main.py --right answer aspirine --user_answer ASPERINE
#Right
```

However, in this case the dependencies are loaded in memory every time the script is runned. Therefore, this should not be the way to use the program.


## How to update the memorized cases

If new cases have to be learned, they should be added at the bottom of the case_memory.csv file. 