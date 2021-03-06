from random import randrange

from main.models.psychic import Psychic


class PsychicService:
    NAMES_FOR_PSYCHICS = [
        "Павел", "Василий", "Григорий", "Кирилл"
    ]

    DEFAULT_MIN_RANGE_NUMBER = 10
    DEFAULT_MAX_RANGE_NUMBER = 99

    FINE_VALUE = 10
    ENCOURAGEMENT_VALUE = 15

    RANGE_FOR_WIN = 0

    def summarizing(self, desired_value: int, psychics: list):
        self.mark_the_winners_psychic(desired_value, psychics)
        for psychic in psychics:
            if not psychic.is_won:
                psychic.score -= self.FINE_VALUE
            else:
                psychic.score += self.ENCOURAGEMENT_VALUE

        return psychics

    def mark_the_winners_psychic(self, desired_value: int, psychics: list):
        min_range_from_value = self.DEFAULT_MAX_RANGE_NUMBER
        index_best_psychics = None

        for index, psychic in enumerate(psychics):
            psychic.is_won = False
            if psychic.last_prediction is not None:
                buf = self._get_difference_between_numbers(desired_value, psychic.last_prediction)
                if buf <= self.RANGE_FOR_WIN and buf <= min_range_from_value:
                    min_range_from_value = buf
                    index_best_psychics = index
                    psychic.is_won = True

    def get_psychic_with_predictions(self, psychics: list):
        for psychic in psychics:
            random_number = self.get_prediction(self.DEFAULT_MIN_RANGE_NUMBER, self.DEFAULT_MAX_RANGE_NUMBER)
            psychic.last_prediction = random_number
            psychic.history += str(random_number) + " "
        return psychics

    @staticmethod
    def get_prediction(min_range: int = 0, max_range: int = 100):
        return randrange(min_range, max_range)

    def generate_psychics(self, number: int = 4):
        generated_psychics = []
        for _ in range(number):
            generated_psychics.append(
                Psychic(self._get_random_name())
            )

        return generated_psychics

    def _get_random_name(self):
        len_names = len(self.NAMES_FOR_PSYCHICS)
        number = randrange(0, len_names - 1)
        return self.NAMES_FOR_PSYCHICS[number]

    @staticmethod
    def _get_difference_between_numbers(first, second):
        return abs(first - second)

    def psychics_to_list_in_dict(self, psychics):
        psychics_in_dict = []
        for psychic in psychics:
            psychics_in_dict.append(psychic.to_dict())
        return psychics_in_dict

    def psychics_from_dict_to_list(self, dict_values):
        psychics = []
        for value in dict_values:
            psychics.append(Psychic.get_from_dict_to_class(value))
        return psychics

    def validate_desired_value(self, desired_value):
        try:
            desired_value = int(desired_value)
            if self.DEFAULT_MIN_RANGE_NUMBER <= desired_value <= self.DEFAULT_MAX_RANGE_NUMBER:
                return True
            return False
        except:
            return False
