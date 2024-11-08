from abc import ABC, abstractmethod

class BaseClass(ABC):

    @abstractmethod
    def contents(self):
        ...
        
    @abstractmethod
    def preprocess_all(self):
        ...

    @abstractmethod
    def augment_all(self):
        ...