from torch.utils.data import Dataset, DataLoader
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nlpaug.augmenter.word as naw  # For augmentation
from typing import List
import os
from imports.baseclass import BaseClass

class TextDataSet(BaseClass):
    def __init__(self, file_path, num_augments=1):

        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    self.raw_texts = f.readlines()

        except FileNotFoundError as e:
            print(e)

        self.num_augments = num_augments

        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.augmenter = naw.SynonymAug(aug_src='wordnet')  # Augmentation using synonyms

    @property
    def contents(self):
        return self.raw_texts
    
    def _preprocess(self,text:str) ->str:
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        # Tokenize
        tokens = word_tokenize(text)
        # Remove stop words
        tokens = [word for word in tokens if word.lower() not in self.stop_words]
        # Lemmatize
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        return ' '.join(tokens)
    
    def preprocess_all(self)->List[str]:
        return [self._preprocess(text) for text in self.raw_texts]

    def augment(self, text:str) -> List[str]:
        return self.augmenter.augment(text)

    def augment_all(self) -> List[str]:

        augmented_texts = []
        for text in self.raw_texts:
            augmented_texts.append(text)
            for _ in range(self.num_augments):
                augmented_texts.extend(self.augment(text))

        # Limit the output if total_output is specified
        output_length = 3*len(self.raw_texts)
             
        return augmented_texts[:output_length]

    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, idx) -> List[str]:
        # Return the list of vocabulary-based token IDs
        return self.texts[idx]

