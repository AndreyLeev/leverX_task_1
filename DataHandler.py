from abc import ABC, abstractmethod 


class DataHandler(ABC):
    @abstractmethod
    def load(self, filename):
        pass

    @abstractmethod
    def dump(self, data, filename):
        pass