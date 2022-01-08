import json


class Psychic:
    def __init__(self, name: str, score: int = 0):
        self.name = name
        self.score = score
        self.last_prediction = None
        self.is_won = None
        self.history = ""

    def to_dict(self):
        my_dict = {"name": self.name, "score": self.score, "last_prediction": self.last_prediction,
                   "is_won": self.is_won, "history": self.history}
        return my_dict

    @staticmethod
    def get_from_dict_to_class(dict_value):
        psy = Psychic(dict_value["name"])
        psy.score = dict_value["score"]
        psy.last_prediction = dict_value["last_prediction"]
        psy.is_won = dict_value["is_won"]
        psy.history = dict_value["history"]
        return psy
